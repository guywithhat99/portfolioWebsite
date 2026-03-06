from machine import Pin, SPI
import time

# Faster SPI - try 40MHz
spi = SPI(1, baudrate=40000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11))
dc = Pin(8, Pin.OUT)
cs = Pin(9, Pin.OUT)
rst = Pin(12, Pin.OUT)
bl = Pin(13, Pin.OUT)

bl.value(1)

def cmd(c):
    cs.value(0)
    dc.value(0)
    spi.write(bytes([c]))
    cs.value(1)

def data(d):
    cs.value(0)
    dc.value(1)
    if isinstance(d, int):
        spi.write(bytes([d]))
    else:
        spi.write(d)
    cs.value(1)

# Reset
rst.value(0)
time.sleep_ms(100)
rst.value(1)
time.sleep_ms(100)

# Init
cmd(0x01); time.sleep_ms(150)
cmd(0x11); time.sleep_ms(120)
cmd(0x36); data(0x00)
cmd(0x3A); data(0x55)
cmd(0x21)
cmd(0x29); time.sleep_ms(120)

def fill(color):
    cmd(0x2A); data(bytes([0x00, 0x00, 0x00, 0xEF]))
    cmd(0x2B); data(bytes([0x00, 0x00, 0x00, 0xEF]))
    cmd(0x2C)
    
    hi = color >> 8
    lo = color & 0xFF
    row = bytes([hi, lo] * 240)
    
    cs.value(0)
    dc.value(1)
    for _ in range(240):
        spi.write(row)
    cs.value(1)

# Test - should be much faster now!
fill(0xF800)  # Red
time.sleep(1)
fill(0x07E0)  # Green
time.sleep(1)
fill(0x001F)  # Blue

print("Done!")