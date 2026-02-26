# display.py
"""
ST7789 240x240 display driver for Raspberry Pi Pico.

Raw SPI driver with drawing primitives — no external dependencies,
works with stock MicroPython firmware.

Usage:
    from display import Display
    lcd = Display()
    lcd.fill(lcd.BLACK)
    lcd.text("Hello!", 10, 10, lcd.WHITE, scale=2)
    lcd.fill_circle(120, 120, 30, lcd.RED)
"""

from machine import Pin, SPI
import time


# ── 5x7 Bitmap Font ─────────────────────────────────────────────────────────
# Standard ASCII printable characters (32–126). Each character is 5 bytes,
# one per column, LSB = top row. 1 pixel gap between characters.

FONT = (
    b'\x00\x00\x00\x00\x00'  # 32  (space)
    b'\x00\x00\x5F\x00\x00'  # 33  !
    b'\x00\x07\x00\x07\x00'  # 34  "
    b'\x14\x7F\x14\x7F\x14'  # 35  #
    b'\x24\x2A\x7F\x2A\x12'  # 36  $
    b'\x23\x13\x08\x64\x62'  # 37  %
    b'\x36\x49\x55\x22\x50'  # 38  &
    b'\x00\x05\x03\x00\x00'  # 39  '
    b'\x00\x1C\x22\x41\x00'  # 40  (
    b'\x00\x41\x22\x1C\x00'  # 41  )
    b'\x14\x08\x3E\x08\x14'  # 42  *
    b'\x08\x08\x3E\x08\x08'  # 43  +
    b'\x00\x50\x30\x00\x00'  # 44  ,
    b'\x08\x08\x08\x08\x08'  # 45  -
    b'\x00\x60\x60\x00\x00'  # 46  .
    b'\x20\x10\x08\x04\x02'  # 47  /
    b'\x3E\x51\x49\x45\x3E'  # 48  0
    b'\x00\x42\x7F\x40\x00'  # 49  1
    b'\x42\x61\x51\x49\x46'  # 50  2
    b'\x21\x41\x45\x4B\x31'  # 51  3
    b'\x18\x14\x12\x7F\x10'  # 52  4
    b'\x27\x45\x45\x45\x39'  # 53  5
    b'\x3C\x4A\x49\x49\x30'  # 54  6
    b'\x01\x71\x09\x05\x03'  # 55  7
    b'\x36\x49\x49\x49\x36'  # 56  8
    b'\x06\x49\x49\x29\x1E'  # 57  9
    b'\x00\x36\x36\x00\x00'  # 58  :
    b'\x00\x56\x36\x00\x00'  # 59  ;
    b'\x08\x14\x22\x41\x00'  # 60  <
    b'\x14\x14\x14\x14\x14'  # 61  =
    b'\x00\x41\x22\x14\x08'  # 62  >
    b'\x02\x01\x51\x09\x06'  # 63  ?
    b'\x3E\x41\x5D\x55\x1E'  # 64  @
    b'\x7E\x11\x11\x11\x7E'  # 65  A
    b'\x7F\x49\x49\x49\x36'  # 66  B
    b'\x3E\x41\x41\x41\x22'  # 67  C
    b'\x7F\x41\x41\x22\x1C'  # 68  D
    b'\x7F\x49\x49\x49\x41'  # 69  E
    b'\x7F\x09\x09\x09\x01'  # 70  F
    b'\x3E\x41\x49\x49\x7A'  # 71  G
    b'\x7F\x08\x08\x08\x7F'  # 72  H
    b'\x00\x41\x7F\x41\x00'  # 73  I
    b'\x20\x40\x41\x3F\x01'  # 74  J
    b'\x7F\x08\x14\x22\x41'  # 75  K
    b'\x7F\x40\x40\x40\x40'  # 76  L
    b'\x7F\x02\x0C\x02\x7F'  # 77  M
    b'\x7F\x04\x08\x10\x7F'  # 78  N
    b'\x3E\x41\x41\x41\x3E'  # 79  O
    b'\x7F\x09\x09\x09\x06'  # 80  P
    b'\x3E\x41\x51\x21\x5E'  # 81  Q
    b'\x7F\x09\x19\x29\x46'  # 82  R
    b'\x46\x49\x49\x49\x31'  # 83  S
    b'\x01\x01\x7F\x01\x01'  # 84  T
    b'\x3F\x40\x40\x40\x3F'  # 85  U
    b'\x1F\x20\x40\x20\x1F'  # 86  V
    b'\x3F\x40\x38\x40\x3F'  # 87  W
    b'\x63\x14\x08\x14\x63'  # 88  X
    b'\x07\x08\x70\x08\x07'  # 89  Y
    b'\x61\x51\x49\x45\x43'  # 90  Z
    b'\x00\x7F\x41\x41\x00'  # 91  [
    b'\x02\x04\x08\x10\x20'  # 92  backslash
    b'\x00\x41\x41\x7F\x00'  # 93  ]
    b'\x04\x02\x01\x02\x04'  # 94  ^
    b'\x40\x40\x40\x40\x40'  # 95  _
    b'\x00\x01\x02\x04\x00'  # 96  `
    b'\x20\x54\x54\x54\x78'  # 97  a
    b'\x7F\x48\x44\x44\x38'  # 98  b
    b'\x38\x44\x44\x44\x20'  # 99  c
    b'\x38\x44\x44\x48\x7F'  # 100 d
    b'\x38\x54\x54\x54\x18'  # 101 e
    b'\x08\x7E\x09\x01\x02'  # 102 f
    b'\x0C\x52\x52\x52\x3E'  # 103 g
    b'\x7F\x08\x04\x04\x78'  # 104 h
    b'\x00\x44\x7D\x40\x00'  # 105 i
    b'\x20\x40\x44\x3D\x00'  # 106 j
    b'\x7F\x10\x28\x44\x00'  # 107 k
    b'\x00\x41\x7F\x40\x00'  # 108 l
    b'\x7C\x04\x18\x04\x78'  # 109 m
    b'\x7C\x08\x04\x04\x78'  # 110 n
    b'\x38\x44\x44\x44\x38'  # 111 o
    b'\x7C\x14\x14\x14\x08'  # 112 p
    b'\x08\x14\x14\x18\x7C'  # 113 q
    b'\x7C\x08\x04\x04\x08'  # 114 r
    b'\x48\x54\x54\x54\x20'  # 115 s
    b'\x04\x3F\x44\x40\x20'  # 116 t
    b'\x3C\x40\x40\x20\x7C'  # 117 u
    b'\x1C\x20\x40\x20\x1C'  # 118 v
    b'\x3C\x40\x30\x40\x3C'  # 119 w
    b'\x44\x28\x10\x28\x44'  # 120 x
    b'\x0C\x50\x50\x50\x3C'  # 121 y
    b'\x44\x64\x54\x4C\x44'  # 122 z
    b'\x00\x08\x36\x41\x00'  # 123 {
    b'\x00\x00\x7F\x00\x00'  # 124 |
    b'\x00\x41\x36\x08\x00'  # 125 }
    b'\x10\x08\x08\x10\x08'  # 126 ~
)


class Display:
    """ST7789 240x240 IPS TFT display driver over SPI."""

    # Preset colors (RGB565)
    BLACK   = 0x0000
    WHITE   = 0xFFFF
    RED     = 0xF800
    GREEN   = 0x07E0
    BLUE    = 0x001F
    YELLOW  = 0xFFE0
    CYAN    = 0x07FF
    MAGENTA = 0xF81F
    ORANGE  = 0xFC00

    WIDTH  = 240
    HEIGHT = 240

    def __init__(self, sck=10, mosi=11, dc=8, cs=9, rst=12, bl=13,
                 baudrate=50_000_000):
        self._spi = SPI(1, baudrate=baudrate, polarity=0, phase=0,
                        sck=Pin(sck), mosi=Pin(mosi))
        self._dc  = Pin(dc, Pin.OUT)
        self._cs  = Pin(cs, Pin.OUT)
        self._rst = Pin(rst, Pin.OUT)
        self._bl  = Pin(bl, Pin.OUT)

        self._init_display()

    # ── Initialization ───────────────────────────────────────────────────────

    def _init_display(self):
        # Hardware reset
        self._rst.value(0)
        time.sleep_ms(100)
        self._rst.value(1)
        time.sleep_ms(100)

        # Software init
        self._cmd(0x01)              # Software reset
        time.sleep_ms(150)
        self._cmd(0x11)              # Sleep out
        time.sleep_ms(120)
        self._cmd(0x36); self._data(0x00)   # MADCTL: no rotation
        self._cmd(0x3A); self._data(0x55)   # COLMOD: 16-bit RGB565
        self._cmd(0x21)              # Display inversion on (needed for IPS)
        self._cmd(0x29)              # Display on
        time.sleep_ms(120)

        # Backlight on
        self._bl.value(1)

    # ── Low-level SPI ────────────────────────────────────────────────────────

    def _cmd(self, c):
        self._cs.value(0)
        self._dc.value(0)
        self._spi.write(bytes([c]))
        self._cs.value(1)

    def _data(self, d):
        self._cs.value(0)
        self._dc.value(1)
        if isinstance(d, int):
            self._spi.write(bytes([d]))
        else:
            self._spi.write(d)
        self._cs.value(1)

    def _set_window(self, x, y, w, h):
        """Set the drawing region for subsequent pixel writes."""
        x1 = x + w - 1
        y1 = y + h - 1
        self._cmd(0x2A)  # Column address set
        self._data(bytes([x >> 8, x & 0xFF, x1 >> 8, x1 & 0xFF]))
        self._cmd(0x2B)  # Row address set
        self._data(bytes([y >> 8, y & 0xFF, y1 >> 8, y1 & 0xFF]))
        self._cmd(0x2C)  # Memory write

    def _write_pixels(self, data):
        """Write raw pixel data (bytes) to the current window."""
        self._cs.value(0)
        self._dc.value(1)
        self._spi.write(data)
        self._cs.value(1)

    # ── Backlight ────────────────────────────────────────────────────────────

    def backlight(self, on):
        """Turn the display backlight on (True) or off (False)."""
        self._bl.value(1 if on else 0)

    # ── Color helper ─────────────────────────────────────────────────────────

    @staticmethod
    def color(r, g, b):
        """Convert 8-bit RGB to 16-bit RGB565."""
        return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

    # ── Screen ───────────────────────────────────────────────────────────────

    def fill(self, color):
        """Fill the entire screen with a single color."""
        self._set_window(0, 0, self.WIDTH, self.HEIGHT)
        hi = color >> 8
        lo = color & 0xFF
        row = bytes([hi, lo] * self.WIDTH)
        self._cs.value(0)
        self._dc.value(1)
        for _ in range(self.HEIGHT):
            self._spi.write(row)
        self._cs.value(1)

    # ── Pixel ────────────────────────────────────────────────────────────────

    def pixel(self, x, y, color):
        """Draw a single pixel."""
        if 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT:
            self._set_window(x, y, 1, 1)
            self._write_pixels(bytes([color >> 8, color & 0xFF]))

    # ── Rectangles ───────────────────────────────────────────────────────────

    def fill_rect(self, x, y, w, h, color):
        """Draw a filled rectangle."""
        # Clip to screen bounds
        if x < 0:
            w += x; x = 0
        if y < 0:
            h += y; y = 0
        if x + w > self.WIDTH:
            w = self.WIDTH - x
        if y + h > self.HEIGHT:
            h = self.HEIGHT - y
        if w <= 0 or h <= 0:
            return

        self._set_window(x, y, w, h)
        hi = color >> 8
        lo = color & 0xFF
        row = bytes([hi, lo] * w)
        self._cs.value(0)
        self._dc.value(1)
        for _ in range(h):
            self._spi.write(row)
        self._cs.value(1)

    def rect(self, x, y, w, h, color):
        """Draw a rectangle outline."""
        self.hline(x, y, w, color)
        self.hline(x, y + h - 1, w, color)
        self.vline(x, y, h, color)
        self.vline(x + w - 1, y, h, color)

    # ── Lines ────────────────────────────────────────────────────────────────

    def hline(self, x, y, w, color):
        """Draw a fast horizontal line."""
        self.fill_rect(x, y, w, 1, color)

    def vline(self, x, y, h, color):
        """Draw a fast vertical line."""
        self.fill_rect(x, y, 1, h, color)

    def line(self, x0, y0, x1, y1, color):
        """Draw a line between two points (Bresenham's algorithm)."""
        # Fast paths for horizontal and vertical lines
        if y0 == y1:
            if x0 > x1:
                x0, x1 = x1, x0
            self.hline(x0, y0, x1 - x0 + 1, color)
            return
        if x0 == x1:
            if y0 > y1:
                y0, y1 = y1, y0
            self.vline(x0, y0, y1 - y0 + 1, color)
            return

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            self.pixel(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    # ── Circles ──────────────────────────────────────────────────────────────

    def circle(self, cx, cy, r, color):
        """Draw a circle outline (midpoint algorithm)."""
        x = r
        y = 0
        err = 1 - r
        while x >= y:
            self.pixel(cx + x, cy + y, color)
            self.pixel(cx + y, cy + x, color)
            self.pixel(cx - y, cy + x, color)
            self.pixel(cx - x, cy + y, color)
            self.pixel(cx - x, cy - y, color)
            self.pixel(cx - y, cy - x, color)
            self.pixel(cx + y, cy - x, color)
            self.pixel(cx + x, cy - y, color)
            y += 1
            if err < 0:
                err += 2 * y + 1
            else:
                x -= 1
                err += 2 * (y - x) + 1

    def fill_circle(self, cx, cy, r, color):
        """Draw a filled circle using horizontal line fills."""
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            self.hline(cx - dx, cy + dy, 2 * dx + 1, color)

    # ── Sprites ──────────────────────────────────────────────────────────────

    def sprite(self, data, x, y, w, h):
        """Draw a sprite from raw RGB565 data.

        Args:
            data: bytes/bytearray of RGB565 pixel data (2 bytes per pixel,
                  big-endian, row-major order).
            x, y: top-left corner on screen.
            w, h: width and height in pixels.
        """
        self._set_window(x, y, w, h)
        self._write_pixels(data)

    # ── Text ─────────────────────────────────────────────────────────────────

    def text(self, string, x, y, color, scale=1, bg=None):
        """Draw a text string using the built-in 5x7 bitmap font.

        Args:
            string: the text to draw.
            x, y:   top-left position.
            color:  text color (RGB565).
            scale:  integer scale factor (1 = 5x7, 2 = 10x14, etc.).
            bg:     background color (RGB565), or None for transparent.
        """
        cursor_x = x
        for ch in string:
            code = ord(ch)
            if code < 32 or code > 126:
                code = 63  # '?' for unsupported characters
            offset = (code - 32) * 5

            if bg is not None:
                # Fast path: draw character as a filled block
                self._draw_char_opaque(offset, cursor_x, y, color, bg, scale)
            else:
                # Transparent: only draw foreground pixels
                self._draw_char_transparent(offset, cursor_x, y, color, scale)

            cursor_x += 6 * scale  # 5 columns + 1 gap

    def _draw_char_opaque(self, offset, x, y, fg, bg, scale):
        """Draw a character with both foreground and background pixels."""
        w = 6 * scale  # 5 columns + 1 gap column
        h = 8 * scale
        # Clip check
        if x + w > self.WIDTH or y + h > self.HEIGHT:
            return
        self._set_window(x, y, w, h)
        buf = bytearray(w * h * 2)
        fg_hi = fg >> 8
        fg_lo = fg & 0xFF
        bg_hi = bg >> 8
        bg_lo = bg & 0xFF
        idx = 0
        for row in range(8):
            for col in range(6):
                if col < 5:
                    bit = (FONT[offset + col] >> row) & 1
                else:
                    bit = 0  # gap column
                hi = fg_hi if bit else bg_hi
                lo = fg_lo if bit else bg_lo
                for _ in range(scale):
                    buf[idx] = hi
                    buf[idx + 1] = lo
                    idx += 2
            # Repeat row for scale
            row_bytes = w * 2
            for _ in range(scale - 1):
                buf[idx:idx + row_bytes] = buf[idx - row_bytes:idx]
                idx += row_bytes
        self._write_pixels(buf)

    def _draw_char_transparent(self, offset, x, y, color, scale):
        """Draw a character, only drawing foreground pixels."""
        for col in range(5):
            column_data = FONT[offset + col]
            for row in range(8):
                if (column_data >> row) & 1:
                    if scale == 1:
                        self.pixel(x + col, y + row, color)
                    else:
                        self.fill_rect(x + col * scale, y + row * scale,
                                       scale, scale, color)

    def text_width(self, string, scale=1):
        """Calculate the pixel width of a string."""
        if not string:
            return 0
        return len(string) * 6 * scale - scale  # no trailing gap

    def text_centered(self, string, y, color, scale=1, bg=None):
        """Draw text horizontally centered on screen."""
        w = self.text_width(string, scale)
        x = max(0, (self.WIDTH - w) // 2)
        self.text(string, x, y, color, scale=scale, bg=bg)
