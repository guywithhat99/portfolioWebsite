#!/usr/bin/env python3
"""Generate solid-color 120x120 RGB565 placeholder images.

Usage: python tools/make_placeholders.py
Output: images/happy.raw, okay.raw, sad.raw, alert.raw
"""

import os

def solid_rgb565(r, g, b, width=120, height=120):
    color = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    pixel = bytes([color >> 8, color & 0xFF])
    return pixel * (width * height)

placeholders = {
    "happy": (80, 200, 80),    # green
    "okay":  (200, 200, 80),   # yellow
    "sad":   (80, 80, 200),    # blue
    "alert": (200, 80, 80),    # red
}

os.makedirs("images", exist_ok=True)
for name, (r, g, b) in placeholders.items():
    path = f"images/{name}.raw"
    with open(path, "wb") as f:
        f.write(solid_rgb565(r, g, b))
    print(f"Created {path}")
