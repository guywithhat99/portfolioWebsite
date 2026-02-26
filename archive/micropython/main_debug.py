# main_debug.py — Testing version with debug prints and no buzzer
# Upload this as main.py to the Pico for debugging

from machine import Pin, PWM
import time
import os

print("=" * 40)
print("TOMOGATCHI DEBUG MODE")
print("=" * 40)

# ── Check filesystem ─────────────────────────────────────────────────────────
print("\n[DEBUG] Checking filesystem...")
try:
    root_files = os.listdir("/")
    print(f"  Root /: {root_files}")
except:
    print("  ERROR: cannot list /")

try:
    img_files = os.listdir("/images")
    print(f"  /images/: {img_files}")
except:
    print("  /images/ NOT FOUND")

try:
    img_files = os.listdir("images")
    print(f"  images/ (relative): {img_files}")
except:
    print("  images/ (relative) NOT FOUND")

# Try to read one image file
for path in ("/images/happy.raw", "images/happy.raw", "/happy.raw", "happy.raw"):
    try:
        f = open(path, "rb")
        size = len(f.read())
        f.close()
        print(f"  FOUND: {path} ({size} bytes)")
    except:
        print(f"  NOT FOUND: {path}")

# ── Display init ─────────────────────────────────────────────────────────────
print("\n[DEBUG] Initializing display...")
try:
    from display import Display
    lcd = Display()
    print("  Display initialized OK")
except Exception as e:
    print(f"  Display FAILED: {e}")
    raise

print("[DEBUG] Filling screen black...")
lcd.fill(Display.BLACK)
print("  Done")

print("[DEBUG] Drawing test rectangle...")
lcd.fill_rect(50, 50, 140, 140, Display.RED)
print("  Red rectangle drawn")
time.sleep_ms(500)

print("[DEBUG] Drawing test text...")
lcd.fill(Display.BLACK)
lcd.text_centered("Hello!", 100, Display.WHITE, scale=3)
print("  Text drawn")
time.sleep_ms(1000)

print("[DEBUG] Drawing test circle...")
lcd.fill(Display.BLACK)
lcd.fill_circle(120, 120, 40, Display.GREEN)
print("  Circle drawn")
time.sleep_ms(500)

# ── Try loading a sprite ─────────────────────────────────────────────────────
print("\n[DEBUG] Testing sprite load...")
lcd.fill(Display.BLACK)
for mood in ("happy", "okay", "sad", "alert"):
    for path in (f"/images/{mood}.raw", f"images/{mood}.raw"):
        try:
            with open(path, "rb") as f:
                data = f.read()
            print(f"  {mood}: loaded from {path} ({len(data)} bytes)")
            if len(data) == 28800:
                lcd.sprite(data, 60, 20, 120, 120)
                lcd.text_centered(mood, 160, Display.WHITE, scale=2)
                time.sleep_ms(800)
                lcd.fill(Display.BLACK)
            else:
                print(f"  WARNING: expected 28800 bytes, got {len(data)}")
            break
        except OSError:
            pass
    else:
        print(f"  {mood}: NOT FOUND in any path")

# ── Buttons ──────────────────────────────────────────────────────────────────
print("\n[DEBUG] Setting up buttons...")
btn_red    = Pin(22, Pin.IN, Pin.PULL_DOWN)
btn_yellow = Pin(21, Pin.IN, Pin.PULL_DOWN)
btn_green  = Pin(19, Pin.IN, Pin.PULL_DOWN)
print("  Buttons configured")

print("[DEBUG] Testing buttons (press each one)...")
lcd.fill(Display.BLACK)
lcd.text_centered("Press buttons", 60, Display.WHITE, scale=2)
lcd.text_centered("to test", 90, Display.WHITE, scale=2)

for i in range(60):  # 3 seconds of button testing
    r = btn_red.value()
    y = btn_yellow.value()
    g = btn_green.value()
    if r or y or g:
        print(f"  Button: red={r} yellow={y} green={g}")
        if r:
            lcd.fill_rect(20, 180, 60, 40, Display.RED)
        if y:
            lcd.fill_rect(90, 180, 60, 40, Display.YELLOW)
        if g:
            lcd.fill_rect(160, 180, 60, 40, Display.GREEN)
    time.sleep_ms(50)

# ── LED ──────────────────────────────────────────────────────────────────────
print("\n[DEBUG] Setting up LED...")
led_r = Pin(16, Pin.OUT)
led_g = Pin(17, Pin.OUT)
led_b = Pin(18, Pin.OUT)

def set_led(r, g, b):
    led_r.value(r)
    led_g.value(g)
    led_b.value(b)

print("  Testing LED red...")
set_led(1, 0, 0)
time.sleep_ms(300)
print("  Testing LED green...")
set_led(0, 1, 0)
time.sleep_ms(300)
print("  Testing LED blue...")
set_led(0, 0, 1)
time.sleep_ms(300)
set_led(0, 0, 0)
print("  LED off")

# ── Buzzer (disabled) ────────────────────────────────────────────────────────
print("\n[DEBUG] Buzzer DISABLED for testing")
buzzer = PWM(Pin(6))
buzzer.duty_u16(0)  # make sure it's off

def play_tone(frequency, duration_ms):
    pass  # disabled

# ── Full pet test ────────────────────────────────────────────────────────────
print("\n[DEBUG] Creating Pet...")
try:
    from tamagotchi import Pet
    pet = Pet(play_tone, set_led)
    print("  Pet created OK")
except Exception as e:
    print(f"  Pet FAILED: {e}")
    import sys
    sys.print_exception(e)
    raise

print("[DEBUG] Pet stats: food={} water={} energy={} mood={}".format(
    pet.food, pet.water, pet.energy, pet.mood()))

print("\n[DEBUG] Entering main loop (watch console for button presses)")
print("  Red=feed  Yellow=water  Green=exercise\n")

last_red    = 0
last_yellow = 0
last_green  = 0
loop_count  = 0

while True:
    red    = btn_red.value()
    yellow = btn_yellow.value()
    green  = btn_green.value()

    if red and not last_red:
        print("[BUTTON] RED pressed -> feed()")
        pet.feed()
        print("  Stats: food={} water={} energy={} mood={}".format(
            pet.food, pet.water, pet.energy, pet.mood()))
    elif yellow and not last_yellow:
        print("[BUTTON] YELLOW pressed -> drink()")
        pet.drink()
        print("  Stats: food={} water={} energy={} mood={}".format(
            pet.food, pet.water, pet.energy, pet.mood()))
    elif green and not last_green:
        print("[BUTTON] GREEN pressed -> exercise()")
        pet.exercise()
        print("  Stats: food={} water={} energy={} mood={}".format(
            pet.food, pet.water, pet.energy, pet.mood()))

    last_red    = red
    last_yellow = yellow
    last_green  = green

    pet.update()

    # Print status every 5 seconds
    loop_count += 1
    if loop_count >= 100:
        loop_count = 0
        print("[LOOP] alive | food={} water={} energy={} mood={}".format(
            pet.food, pet.water, pet.energy, pet.mood()))

    time.sleep_ms(50)
