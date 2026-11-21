#!/usr/bin/env python3
"""The Catalogue Photo of an Impossible Gadget.

Writes one catalogue photograph to /output/entry.png: a solar-powered
flashlight (LUMEN SOLAR SL-1) photographed as a hero studio product shot,
with exactly one accessory -- a small potted sunflower.

The hero photograph is generated in-session and shipped as
assets/product.png. This program loads it, fits it to the gate limits
(at most 1024x1024 px, at most 1,048,576 bytes), draws only the smallest
catalogue furniture (a thin rule and a model line along the bottom edge,
never an explanation of the joke), and writes /output/entry.png
deterministically.
"""

import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSET = HERE / "assets" / "product.png"
OUT_PATH = Path(os.environ.get("MAKEFUN_OUTPUT", "/output/entry.png"))

MAX_SIDE = 1024
MAX_BYTES = 1_048_576


def load_font(size: int):
    """Best-effort clean sans font; fall back to PIL's built-in bitmap."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def fit_image(img: Image.Image) -> Image.Image:
    """Convert to RGB and fit inside MAX_SIDE x MAX_SIDE, never upscaling."""
    img = img.convert("RGB")
    if img.width > MAX_SIDE or img.height > MAX_SIDE:
        img = img.resize((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
    return img


def draw_catalogue_furniture(img: Image.Image) -> Image.Image:
    """Subtle bottom-edge catalogue furniture: a hairline rule and the
    model line, in a quiet grey, set into the photo's own margin so the
    product stays the hero. No caption, no explanation of the joke."""
    draw = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    font = load_font(22)
    label = "LUMEN SOLAR  ·  SL-1"
    bbox = draw.textbbox((0, 0), label, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (w - text_w) // 2
    y = h - text_h - 18
    # Hairline rule just above the model line.
    draw.line([(w // 2 - 90, y - 10), (w // 2 + 90, y - 10)],
              fill=(120, 120, 120, 255), width=1)
    draw.text((x, y), label, font=font, fill=(110, 110, 110, 255))
    return img


def encode(img: Image.Image, out_path: Path) -> tuple[str, int]:
    """Write the image deterministically under the byte cap.

    Prefer PNG; fall back to JPEG quality steps (still accepted by the
    gate, which takes a whole PNG or JPEG) and then a smaller side.
    Returns (format, bytes written).
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # PNG first: lossless, keeps the studio photograph crisp.
    img.save(out_path, format="PNG", optimize=True)
    size = out_path.stat().st_size
    if size <= MAX_BYTES:
        return "PNG", size
    for quality in (88, 82, 75):
        img.save(out_path, format="JPEG", quality=quality, optimize=True)
        size = out_path.stat().st_size
        if size <= MAX_BYTES:
            return "JPEG", size
    small = img.resize((896, 896), Image.LANCZOS)
    small.save(out_path, format="JPEG", quality=82, optimize=True)
    return "JPEG", out_path.stat().st_size


def verify(out_path: Path) -> tuple[bool, str]:
    """Re-open the written file and confirm the gate limits hold."""
    with Image.open(out_path) as im:
        im.verify()
    with Image.open(out_path) as im:
        w, h = im.size
        fmt = im.format
    size = out_path.stat().st_size
    ok = (w <= MAX_SIDE and h <= MAX_SIDE and size <= MAX_BYTES
          and fmt in ("PNG", "JPEG"))
    return ok, f"{fmt} {w}x{h} {size} bytes"


def main() -> int:
    if not ASSET.exists():
        print(f"missing asset: {ASSET}", file=sys.stderr)
        return 1
    with Image.open(ASSET) as src:
        img = fit_image(src)
    img = draw_catalogue_furniture(img)
    fmt, size = encode(img, OUT_PATH)
    print(f"wrote {OUT_PATH} ({fmt}, {img.size[0]}x{img.size[1]}, "
          f"{size} bytes)")
    if size > MAX_BYTES:
        print("error: output exceeds 1,048,576 bytes", file=sys.stderr)
        return 1
    ok, detail = verify(OUT_PATH)
    print(f"verify: {detail} -> {'OK' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
