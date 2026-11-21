"""Post-processing: upscale, colour grading, collage layout."""
from PIL import Image, ImageEnhance, ImageOps


def upscale(img: Image.Image, factor: float = 2.0) -> Image.Image:
    w, h = img.size
    return img.resize((int(w * factor), int(h * factor)), Image.LANCZOS)


GRADES = {
    "warm": {"tint": (255, 200, 150), "amount": 0.12, "contrast": 1.05, "saturation": 0.95},
    "cool": {"tint": (150, 190, 255), "amount": 0.10, "contrast": 1.05, "saturation": 0.90},
    "film": {"tint": (240, 220, 190), "amount": 0.08, "contrast": 0.92, "saturation": 0.85},
    "none": None,
}


def color_grade(img: Image.Image, style: str = "warm") -> Image.Image:
    g = GRADES[style]
    if g is None:
        return img
    tinted = Image.blend(img, Image.new("RGB", img.size, g["tint"]), g["amount"])
    tinted = ImageEnhance.Contrast(tinted).enhance(g["contrast"])
    return ImageEnhance.Color(tinted).enhance(g["saturation"])


def collage(images: list[Image.Image], cols: int = 2, cell_width: int = 540,
            gap: int = 12, bg=(255, 255, 255)) -> Image.Image:
    """Grid of images, each fitted to the same cell size."""
    if not images:
        raise ValueError("No images for collage")
    ratio = images[0].height / images[0].width
    cell = (cell_width, int(cell_width * ratio))
    rows = -(-len(images) // cols)
    sheet = Image.new("RGB", (cols * cell[0] + (cols + 1) * gap,
                              rows * cell[1] + (rows + 1) * gap), bg)
    for i, img in enumerate(images):
        r, c = divmod(i, cols)
        sheet.paste(ImageOps.fit(img, cell, Image.LANCZOS),
                    (gap + c * (cell[0] + gap), gap + r * (cell[1] + gap)))
    return sheet


def thumbnail(img: Image.Image, size=(400, 400)) -> Image.Image:
    return ImageOps.fit(img, size, Image.LANCZOS)
