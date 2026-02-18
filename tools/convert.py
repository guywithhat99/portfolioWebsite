#!/usr/bin/env python3
"""Convert a PNG image to RGB565 raw binary for use on the Pico display.

Usage: python tools/convert.py input.png output.raw [width] [height]
Default output size: 120x120
"""

import sys
from PIL import Image

def png_to_rgb565(input_path, output_path, width=120, height=120):
    img = Image.open(input_path).convert("RGB").resize(
        (width, height), Image.Resampling.NEAREST
    )
    buf = bytearray()
    for r, g, b in img.getdata():
        color = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
        buf.append(color >> 8)
        buf.append(color & 0xFF)
    with open(output_path, "wb") as f:
        f.write(buf)
    print(f"Saved {len(buf)} bytes to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    try:
        w = int(sys.argv[3]) if len(sys.argv) > 3 else 120
        h = int(sys.argv[4]) if len(sys.argv) > 4 else 120
    except ValueError:
        print("Error: width and height must be integers.")
        sys.exit(1)
    try:
        png_to_rgb565(sys.argv[1], sys.argv[2], w, h)
    except FileNotFoundError:
        print(f"Error: input file not found: {sys.argv[1]}")
        sys.exit(1)
