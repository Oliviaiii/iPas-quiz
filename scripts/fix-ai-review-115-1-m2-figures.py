"""Guarded figure repair from independent AI review, 115-1 中級第二科 Q2 and Q8.

Both formula figures were imported without their PDF soft mask (SMask), so the
stored PNGs are a single solid black rectangle and the site shows a black box
instead of the formula. This script recomposites each embedded image with its
alpha mask over white, at the same pixel dimensions already recorded in
questions.json, so no bank metadata changes.

Guards: the official PDF must be present, each target file must still be the
exact solid-black file recorded below, and each recovered image must be
non-uniform before it is written.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pymupdf
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "tmp" / "pdfs" / "aiap-115-intermediate-1-big-data.pdf"
IMAGES = ROOT / "public" / "images" / "questions"

# (page index, image xref, smask xref, output file, expected sha256 of the broken file, size)
TARGETS = [
    (0, 32, 33, "aiap-115-intermediate-1-big-data-p01-1.png",
     "efd01e7cd37f83fa7760f33518174b7fc2f74bab09b89b50f7cf86a3ab85ab59", (135, 68)),
    (1, 36, 37, "aiap-115-intermediate-1-big-data-p02-1.png",
     "40e991367ed3bc7b25be79a49d7da05911d95e93a2a72f7b4c17218b0d3e3fd4", (152, 70)),
]


def main() -> None:
    if not PDF.exists():
        raise RuntimeError(f"Official PDF not found: {PDF}")
    document = pymupdf.open(PDF)

    for page_index, xref, smask, name, digest, size in TARGETS:
        path = IMAGES / name
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise RuntimeError(f"Guard failed: {name} is not the recorded broken file")
        with Image.open(path) as broken:
            colours = broken.convert("RGB").getcolors(maxcolors=8)
        if not colours or len(colours) != 1:
            raise RuntimeError(f"Guard failed: {name} is not a solid-colour placeholder")

        page = document[page_index]
        if not any(image[0] == xref for image in page.get_images(full=True)):
            raise RuntimeError(f"Guard failed: xref {xref} not on PDF page {page_index + 1}")

        base = pymupdf.Pixmap(document, xref)
        mask = pymupdf.Pixmap(document, smask)
        if (base.width, base.height) != size or (mask.width, mask.height) != size:
            raise RuntimeError(f"Guard failed: {name} unexpected embedded size")

        colour = Image.frombytes(
            "RGBA" if base.n == 4 else "RGB", (base.width, base.height), base.samples
        ).convert("RGB")
        alpha = Image.frombytes("L", (mask.width, mask.height), mask.samples)
        flattened = Image.new("RGB", colour.size, (255, 255, 255))
        flattened.paste(colour, mask=alpha)

        recovered = flattened.getcolors(maxcolors=65536)
        if not recovered or len(recovered) < 2:
            raise RuntimeError(f"Guard failed: recovered {name} is still uniform")
        flattened.save(path, format="PNG", optimize=True)
        print(f"repaired {name} ({flattened.width}x{flattened.height}, {len(recovered)} colours)")


if __name__ == "__main__":
    main()
