from machine import Pin, SPI, PWM
import time

# ========== DISPLAY SETUP ==========
spi = SPI(1, baudrate=50000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11))
dc = Pin(8, Pin.OUT)
cs = Pin(9, Pin.OUT)

# ========== RGB LED SETUP ==========
led_r = Pin(16, Pin.OUT)
led_g = Pin(17, Pin.OUT)
led_b = Pin(18, Pin.OUT)

# ========== BUTTON SETUP ==========
btn_red = Pin(22, Pin.IN, Pin.PULL_DOWN)
btn_yellow = Pin(21, Pin.IN, Pin.PULL_DOWN)
btn_green = Pin(19, Pin.IN, Pin.PULL_DOWN)

# ========== BUZZER SETUP ==========
buzzer = PWM(Pin(6))

# ========== NOTE FREQUENCIES ==========
NOTE_C = 523   # C5
NOTE_E = 659   # E5
NOTE_G = 784   # G5
NOTE_A = 440   # A4
NOTE_B = 988   # B5

# ========== BUZZER FUNCTIONS ==========
def play_tone(frequency, duration_ms):
    buzzer.freq(frequency)
    buzzer.duty_u16(32768)  # 50% duty cycle
    time.sleep_ms(duration_ms)
    buzzer.duty_u16(0)  # Turn off

def play_arpeggio(notes, note_duration=150):
    """Play an arpeggio while button is held"""
    for note in notes:
        buzzer.freq(note)
        buzzer.duty_u16(32768)
        time.sleep_ms(note_duration)
        buzzer.duty_u16(0)
        time.sleep_ms(20)  # Small gap between notes

# Arpeggio patterns
C_MAJOR = [NOTE_C, NOTE_E, NOTE_G, NOTE_E]  # C-E-G-E
E_MINOR = [NOTE_E, NOTE_G, NOTE_B, NOTE_G]  # E-G-B-G
A_MINOR = [NOTE_A, NOTE_C, NOTE_E, NOTE_C]  # A-C-E-C

# ========== DISPLAY FUNCTIONS ==========
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

def init_display():
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

# ========== LED FUNCTION ==========
def set_led(r, g, b):
    led_r.value(r)
    led_g.value(g)
    led_b.value(b)

# ========== COLORS (RGB565) ==========
RED    = 0xF000
YELLOW = 0xFF00
GREEN  = 0x0F00
BLACK  = 0x0000

# ========== MAIN PROGRAM ==========
print("Initializing display...")
init_display()
fill(BLACK)
set_led(0, 0, 0)

print("Ready! Hold buttons to play arpeggios:")
print("  GP22 = Red (C major)")
print("  GP21 = Yellow (E minor)")
print("  GP19 = Green (A minor)")

while True:
    if btn_red.value() == 1:
        print("RED - C Major!")
        fill(RED)
        set_led(1, 0, 0)
        play_arpeggio(C_MAJOR)
        
    elif btn_yellow.value() == 1:
        print("YELLOW - E Minor!")
        fill(YELLOW)
        set_led(1, 0.8, 0)
        play_arpeggio(E_MINOR)
        
    elif btn_green.value() == 1:
        print("GREEN - A Minor!")
        fill(GREEN)
        set_led(0, 1, 0)
        play_arpeggio(A_MINOR)
    
    else:
        # Turn off buzzer when no button pressed
        buzzer.duty_u16(0)
        
    time.sleep_ms(10)