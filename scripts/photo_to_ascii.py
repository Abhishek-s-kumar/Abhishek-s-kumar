#!/usr/bin/env python3
"""
photo_to_ascii.py
Convert a photo (assets/photo.jpg) into ASCII art lines.
Usage: python photo_to_ascii.py assets/photo.jpg --width 70
Outputs: scripts/ascii_output.txt (used by build_typing_svg.py)
"""
import sys
import argparse
from PIL import Image, ImageOps

# Dense -> sparse ramp, dark chars first (dark bg terminal look)
RAMP = "@%#*+=-:. "


def image_to_ascii(path: str, width: int = 70, contrast: float = 1.2) -> list[str]:
    img = Image.open(path).convert("L")
    img = ImageOps.autocontrast(img, cutoff=1)

    # character cells are ~2x taller than wide, correct aspect ratio
    aspect_correction = 0.55
    w, h = img.size
    new_h = int((width * h / w) * aspect_correction)
    img = img.resize((width, max(new_h, 1)))

    pixels = img.getdata()
    chars = []
    ramp_len = len(RAMP)
    for p in pixels:
        idx = min(ramp_len - 1, int((p / 255) * ramp_len))
        chars.append(RAMP[idx])

    lines = []
    for row in range(new_h):
        line = "".join(chars[row * width:(row + 1) * width])
        lines.append(line)
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photo", help="path to source photo")
    ap.add_argument("--width", type=int, default=70)
    ap.add_argument("--out", default="scripts/ascii_output.txt")
    args = ap.parse_args()

    lines = image_to_ascii(args.photo, args.width)
    with open(args.out, "w") as f:
        f.write("\n".join(lines))
    print(f"Wrote {len(lines)} lines -> {args.out}")


if __name__ == "__main__":
    main()
