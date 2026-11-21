"""Image generation backends."""
import random

from PIL import Image, ImageDraw

from .prompts import Job


class MockBackend:
    """Draws a placeholder image so the pipeline can be tested without a GPU."""

    def generate(self, job: Job) -> Image.Image:
        rng = random.Random(job.seed + hash(job.prompt) % 10_000)
        top = tuple(rng.randint(60, 200) for _ in range(3))
        bottom = tuple(rng.randint(20, 120) for _ in range(3))
        img = Image.new("RGB", (job.width, job.height))
        draw = ImageDraw.Draw(img)
        for y in range(job.height):
            t = y / job.height
            draw.line([(0, y), (job.width, y)],
                      fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))
        draw.text((24, 24), job.name, fill=(255, 255, 255))
        return img


class DiffusersBackend:
    """Stable Diffusion XL via Hugging Face diffusers (needs a CUDA GPU).

    The built-in safety checker stays enabled where the pipeline provides one.
    """

    def __init__(self, model: str = "stabilityai/stable-diffusion-xl-base-1.0"):
        import torch
        from diffusers import StableDiffusionXLPipeline

        self.torch = torch
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            model, torch_dtype=torch.float16, variant="fp16", use_safetensors=True
        ).to("cuda")

    def generate(self, job: Job) -> Image.Image:
        gen = self.torch.Generator("cuda").manual_seed(job.seed)
        return self.pipe(
            prompt=job.prompt,
            negative_prompt=job.negative,
            width=job.width,
            height=job.height,
            num_inference_steps=job.steps,
            guidance_scale=job.guidance,
            generator=gen,
        ).images[0]


def get_backend(name: str):
    if name == "mock":
        return MockBackend()
    if name == "diffusers":
        return DiffusersBackend()
    raise ValueError(f"Unknown backend: {name}")
