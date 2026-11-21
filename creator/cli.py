"""Command line entry point: python -m creator.cli templates/editorial_portrait.yaml"""
import argparse
import json
from pathlib import Path

from .backends import get_backend
from .postprocess import collage, color_grade, thumbnail, upscale
from .prompts import expand, load_template


def main(argv=None):
    p = argparse.ArgumentParser(description="Batch-generate editorial images from a template")
    p.add_argument("template")
    p.add_argument("--backend", default="mock", choices=["mock", "diffusers"])
    p.add_argument("--out", default="output")
    p.add_argument("--grade", default="warm", choices=["warm", "cool", "film", "none"])
    p.add_argument("--upscale", type=float, default=1.0)
    p.add_argument("--limit", type=int, default=0, help="Generate at most N images")
    args = p.parse_args(argv)

    template = load_template(args.template)
    jobs = expand(template)
    if args.limit:
        jobs = jobs[: args.limit]

    out = Path(args.out) / template["name"]
    (out / "thumbs").mkdir(parents=True, exist_ok=True)
    backend = get_backend(args.backend)

    images, manifest = [], []
    for job in jobs:
        img = color_grade(backend.generate(job), args.grade)
        if args.upscale > 1:
            img = upscale(img, args.upscale)
        img.save(out / f"{job.name}.png")
        thumbnail(img).save(out / "thumbs" / f"{job.name}.jpg", quality=90)
        images.append(img)
        manifest.append({"file": f"{job.name}.png", "prompt": job.prompt,
                         "negative": job.negative, "seed": job.seed, **job.meta})
        print(f"saved {job.name}")

    collage(images).save(out / "collage.jpg", quality=90)
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"{len(images)} images -> {out}")


if __name__ == "__main__":
    main()
