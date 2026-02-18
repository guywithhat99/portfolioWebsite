# st7789.py
"""
ST7789 display driver stub.

Replace this file with the real russhughes st7789 driver before running on hardware.
Download from: https://github.com/russhughes/st7789_mpy/releases
Copy the st7789.py for Raspberry Pi Pico from the release assets.
"""

class ST7789:
    def __init__(self, spi, width, height, dc, cs, reset=None, backlight=None, **kwargs):
        self.width = width
        self.height = height

    def init(self):
        pass

    def fill(self, color):
        pass

    def fill_rect(self, x, y, w, h, color):
        pass

    def pixel(self, x, y, color):
        pass

    def text(self, string, x, y, color):
        pass

    def blit_buffer(self, buffer, x, y, w, h):
        pass
