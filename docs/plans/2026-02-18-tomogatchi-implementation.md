# Tomogatchi Workshop — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a complete Tamagotchi-style virtual pet workshop project for Raspberry Pi Pico with MicroPython, including participant stub code, boilerplate game logic, display/sprite system, and slide-ready workshop documentation.

**Architecture:** Two-file split — `main.py` is the workshop file participants edit (button setup, LED helper, buzzer helper); `tamagotchi.py` is read-only boilerplate containing the Pet state machine, display rendering, stat decay, and power saving. Hardware callables (`play_tone`, `set_led`) are injected into the Pet class at construction, so participant code drives the game without participants needing to understand the full loop.

**Tech Stack:** MicroPython on Raspberry Pi Pico, ST7789 1.5" 240×240 IPS TFT (russhughes driver), RGB565 raw image files, PWM buzzer, RGB LED, 3 GPIO buttons.

---

## Before You Start

Read the approved design doc at `docs/plans/2026-02-18-tomogatchi-design.md`. Understand the two-file split and the Pet API before writing any code.

Pin assignments:
- Buttons: red GP22, yellow GP21, green GP19 (all `PULL_DOWN`)
- LED: red GP16, green GP17, blue GP18
- Buzzer: PWM GP6
- Display SPI: SCK GP10, MOSI GP11, DC GP8, CS GP9
- Display backlight: GP13
- Display reset: GP12

---

## Task 1: Project Scaffolding

**Files:**
- Create: `main.py`
- Create: `tamagotchi.py`
- Create: `st7789.py`
- Create: `images/.gitkeep`
- Create: `tools/.gitkeep`
- Create: `tests/test_pet.py`

**Step 1: Create directory structure**

```bash
mkdir -p images tools tests docs/plans
```

**Step 2: Create empty stub files**

Create `main.py` with a single comment:
```python
# Tomogatchi Workshop — participant file
```

Create `tamagotchi.py` with a single comment:
```python
# Tomogatchi Workshop — boilerplate (read-only)
```

Create `tests/test_pet.py` with a single comment:
```python
# Pet state machine tests
```

**Step 3: Download the ST7789 driver**

Download the pre-compiled MicroPython ST7789 driver from the russhughes release for Raspberry Pi Pico:
https://github.com/russhughes/st7789_mpy

Copy the `st7789.py` file into the project root. This file is provided as-is — do not modify it.

**Step 4: Commit**

```bash
git add .
git commit -m "chore: scaffold project structure"
```

---

## Task 2: Placeholder Image Generator (`tools/convert.py`)

**Files:**
- Create: `tools/convert.py`
- Create: `tools/make_placeholders.py`

**Step 1: Write `tools/convert.py`**

This script runs on the host machine (not the Pico). Requires `pip install pillow`.

```python
#!/usr/bin/env python3
"""Convert a PNG image to RGB565 raw binary for use on the Pico display.

Usage: python tools/convert.py input.png output.raw [width] [height]
Default output size: 120x120
"""

import sys
from PIL import Image

def png_to_rgb565(input_path, output_path, width=120, height=120):
    img = Image.open(input_path).convert("RGB").resize((width, height))
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
    w = int(sys.argv[3]) if len(sys.argv) > 3 else 120
    h = int(sys.argv[4]) if len(sys.argv) > 4 else 120
    png_to_rgb565(sys.argv[1], sys.argv[2], w, h)
```

**Step 2: Write `tools/make_placeholders.py`**

Generates solid-color placeholder `.raw` files so the project runs before real art exists.

```python
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
```

**Step 3: Run the placeholder generator**

```bash
python tools/make_placeholders.py
```

Expected output:
```
Created images/happy.raw
Created images/okay.raw
Created images/sad.raw
Created images/alert.raw
```

Each file should be exactly 28,800 bytes (120 × 120 × 2).

```bash
ls -la images/
```

**Step 4: Commit**

```bash
git add tools/ images/
git commit -m "feat: add image conversion tools and placeholder sprites"
```

---

## Task 3: Pet State Machine — Core Logic + Tests

Write the Pet class logic first, with tests, before touching any display code. The Pet class is designed so all hardware calls are injected — this makes it testable on a host machine without MicroPython.

**Files:**
- Modify: `tamagotchi.py`
- Modify: `tests/test_pet.py`

**Step 1: Write the failing tests**

```python
# tests/test_pet.py
"""
Tests for Pet state machine logic.
Run on host: python -m pytest tests/test_pet.py -v

These tests use a mock Pet that replaces hardware-dependent code,
testing only the pure stat/mood logic.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tests.mock_pet import MockPet


class TestStats:
    def test_initial_stats_are_full(self):
        pet = MockPet()
        assert pet.food == 100
        assert pet.water == 100
        assert pet.energy == 100

    def test_feed_increases_food(self):
        pet = MockPet()
        pet.food = 50
        pet.feed()
        assert pet.food == 70

    def test_feed_caps_at_100(self):
        pet = MockPet()
        pet.food = 95
        pet.feed()
        assert pet.food == 100

    def test_water_increases_water(self):
        pet = MockPet()
        pet.water = 40
        pet.water_pet()
        assert pet.water == 60

    def test_exercise_increases_energy(self):
        pet = MockPet()
        pet.energy = 30
        pet.exercise()
        assert pet.energy == 50

    def test_stats_floor_at_zero(self):
        pet = MockPet()
        pet.food = 5
        pet._decay_stat("food", 10)
        assert pet.food == 0


class TestMood:
    def test_all_high_is_happy(self):
        pet = MockPet()
        pet.food = 80
        pet.water = 80
        pet.energy = 80
        assert pet.mood() == "happy"

    def test_any_below_40_is_sad(self):
        pet = MockPet()
        pet.food = 35
        pet.water = 80
        pet.energy = 80
        assert pet.mood() == "sad"

    def test_mixed_is_okay(self):
        pet = MockPet()
        pet.food = 50
        pet.water = 50
        pet.energy = 50
        assert pet.mood() == "okay"

    def test_boundary_exactly_60_is_happy(self):
        pet = MockPet()
        pet.food = 60
        pet.water = 60
        pet.energy = 60
        assert pet.mood() == "happy"

    def test_boundary_exactly_40_is_okay_not_sad(self):
        pet = MockPet()
        pet.food = 40
        pet.water = 80
        pet.energy = 80
        assert pet.mood() == "okay"


class TestAlerts:
    def test_alert_fires_when_stat_below_30(self):
        pet = MockPet()
        pet.food = 25
        assert pet.needs_alert() is True

    def test_no_alert_when_all_stats_ok(self):
        pet = MockPet()
        pet.food = 50
        pet.water = 50
        pet.energy = 50
        assert pet.needs_alert() is False
```

**Step 2: Create `tests/mock_pet.py`**

This is a host-testable version of the Pet logic with no MicroPython dependencies:

```python
# tests/mock_pet.py
"""Host-testable Pet logic for unit tests. No MicroPython dependencies."""


class MockPet:
    STAT_MAX = 100
    STAT_MIN = 0
    HAPPY_THRESHOLD = 60
    SAD_THRESHOLD = 40
    ALERT_THRESHOLD = 30
    FEED_AMOUNT = 20

    def __init__(self):
        self.food = 100
        self.water = 100
        self.energy = 100

    def feed(self):
        self.food = min(self.STAT_MAX, self.food + self.FEED_AMOUNT)

    def water_pet(self):
        self.water = min(self.STAT_MAX, self.water + self.FEED_AMOUNT)

    def exercise(self):
        self.energy = min(self.STAT_MAX, self.energy + self.FEED_AMOUNT)

    def _decay_stat(self, stat_name, amount):
        current = getattr(self, stat_name)
        setattr(self, stat_name, max(self.STAT_MIN, current - amount))

    def mood(self):
        if self.food >= self.HAPPY_THRESHOLD and \
           self.water >= self.HAPPY_THRESHOLD and \
           self.energy >= self.HAPPY_THRESHOLD:
            return "happy"
        if self.food < self.SAD_THRESHOLD or \
           self.water < self.SAD_THRESHOLD or \
           self.energy < self.SAD_THRESHOLD:
            return "sad"
        return "okay"

    def needs_alert(self):
        return (self.food < self.ALERT_THRESHOLD or
                self.water < self.ALERT_THRESHOLD or
                self.energy < self.ALERT_THRESHOLD)
```

**Step 3: Run tests to verify they fail**

```bash
python -m pytest tests/test_pet.py -v
```

Expected: all tests fail with `ModuleNotFoundError` — good, the logic doesn't exist yet.

**Step 4: Write `tamagotchi.py` Pet class core logic**

```python
# tamagotchi.py
"""
Tomogatchi Workshop — boilerplate (read-only)

This file contains the pet state machine, display rendering, stat decay,
alert system, and power saving logic. You don't need to modify this file —
but reading it is encouraged!
"""

import time
import urandom
import machine
import st7789

# ── Constants ────────────────────────────────────────────────────────────────

STAT_MAX        = 100
STAT_MIN        = 0
HAPPY_THRESHOLD = 60   # all stats must be at or above this to be happy
SAD_THRESHOLD   = 40   # any stat below this triggers sad mood
ALERT_THRESHOLD = 30   # any stat below this triggers buzzer alert
FEED_AMOUNT     = 20   # how much each button press adds to a stat
DECAY_RATE      = 1    # stat points lost per DECAY_INTERVAL_MS
DECAY_INTERVAL  = 10000  # ms between each decay tick (10 seconds)
BACKLIGHT_TIMEOUT = 30000  # ms of inactivity before backlight turns off

# Alert tone
ALERT_FREQ      = 880   # Hz
ALERT_DURATION  = 150   # ms

# Display
LCD_WIDTH  = 240
LCD_HEIGHT = 240
SPRITE_W   = 120
SPRITE_H   = 120
SPRITE_X   = (LCD_WIDTH - SPRITE_W) // 2   # centered
SPRITE_Y   = 20

# Text zone (below sprite)
TEXT_Y     = SPRITE_Y + SPRITE_H + 10
TEXT_COLOR = 0xFFFF  # white

# Button indicator row
INDICATOR_Y    = LCD_HEIGHT - 30
INDICATOR_R    = 8     # circle radius in pixels
INDICATOR_POSITIONS = [40, 120, 200]  # x centres for red, yellow, green
INDICATOR_COLORS    = [0xF800, 0xFFE0, 0x07E0]  # red, yellow, green (RGB565)
INDICATOR_LABELS    = ["Food", "Water", "Move"]

# Colors
BLACK = 0x0000
WHITE = 0xFFFF

# Encouragement messages per action
MESSAGES = {
    "feed":     ["Yum!", "So tasty!", "Delicious!", "Thanks!", "More please!"],
    "water":    ["Refreshing!", "So hydrated!", "Ahh!", "Thanks!", "Splish splash!"],
    "exercise": ["Go go go!", "Feeling fit!", "Wahoo!", "So strong!", "Keep it up!"],
    "alert":    ["Hey...", "I'm hungry...", "Don't forget me!", "Hellooo?"],
}


# ── Display helpers ───────────────────────────────────────────────────────────

def _init_lcd():
    spi = machine.SPI(1, baudrate=50_000_000, polarity=0, phase=0,
                      sck=machine.Pin(10), mosi=machine.Pin(11))
    dc  = machine.Pin(8,  machine.Pin.OUT)
    cs  = machine.Pin(9,  machine.Pin.OUT)
    rst = machine.Pin(12, machine.Pin.OUT)
    bl  = machine.Pin(13, machine.Pin.OUT)
    bl.value(1)
    lcd = st7789.ST7789(spi, LCD_WIDTH, LCD_HEIGHT,
                        dc=dc, cs=cs, reset=rst)
    lcd.init()
    return lcd, bl


def _load_sprite(mood):
    """Load a 120×120 RGB565 raw image from the images/ directory."""
    path = f"images/{mood}.raw"
    try:
        with open(path, "rb") as f:
            return f.read()
    except OSError:
        # Fallback: solid grey block if file missing
        return bytes([0x84, 0x10] * (SPRITE_W * SPRITE_H))


def _draw_circle(lcd, cx, cy, r, color):
    """Draw a filled circle using the midpoint algorithm."""
    for y in range(-r, r + 1):
        for x in range(-r, r + 1):
            if x * x + y * y <= r * r:
                lcd.pixel(cx + x, cy + y, color)


# ── Pet class ─────────────────────────────────────────────────────────────────

class Pet:
    """
    The virtual pet. Receives play_tone and set_led as callables so
    participant-written hardware code drives the game.

    Usage:
        pet = Pet(play_tone, set_led)
        pet.feed()      # red button
        pet.water()     # yellow button
        pet.exercise()  # green button
        pet.update()    # call every loop iteration
    """

    def __init__(self, play_tone, set_led):
        self._play_tone = play_tone
        self._set_led   = set_led
        self._lcd, self._bl = _init_lcd()

        # Stats
        self.food   = STAT_MAX
        self.water  = STAT_MAX
        self.energy = STAT_MAX

        # Internal timing
        self._last_decay    = time.ticks_ms()
        self._last_activity = time.ticks_ms()
        self._msg_clear_at  = 0
        self._backlight_on  = True
        self._last_mood     = None
        self._current_msg   = ""

        # Draw initial screen
        self._lcd.fill(BLACK)
        self._draw_indicators()
        self._redraw()

    # ── Public API ───────────────────────────────────────────────────────────

    def feed(self):
        self.food = min(STAT_MAX, self.food + FEED_AMOUNT)
        self._on_action("feed")

    def water(self):
        self.water = min(STAT_MAX, self.water + FEED_AMOUNT)
        self._on_action("water")

    def exercise(self):
        self.energy = min(STAT_MAX, self.energy + FEED_AMOUNT)
        self._on_action("exercise")

    def update(self):
        """Call every loop iteration. Handles decay, alerts, and redraw."""
        now = time.ticks_ms()

        # Stat decay
        if time.ticks_diff(now, self._last_decay) >= DECAY_INTERVAL:
            self._decay_all()
            self._last_decay = now

        # Clear message after 2 seconds
        if self._current_msg and time.ticks_diff(now, self._msg_clear_at) >= 0:
            self._current_msg = ""
            self._clear_text_zone()

        # Backlight timeout (power saving)
        if self._backlight_on:
            if time.ticks_diff(now, self._last_activity) >= BACKLIGHT_TIMEOUT:
                self._bl.value(0)
                self._backlight_on = False

        # Redraw if mood changed
        new_mood = self.mood()
        if new_mood != self._last_mood:
            self._redraw()

        # Alert if any stat is critical
        if self.needs_alert():
            self._trigger_alert()

    # ── Stat logic ───────────────────────────────────────────────────────────

    def mood(self):
        if (self.food  >= HAPPY_THRESHOLD and
            self.water >= HAPPY_THRESHOLD and
            self.energy >= HAPPY_THRESHOLD):
            return "happy"
        if (self.food  < SAD_THRESHOLD or
            self.water < SAD_THRESHOLD or
            self.energy < SAD_THRESHOLD):
            return "sad"
        return "okay"

    def needs_alert(self):
        return (self.food  < ALERT_THRESHOLD or
                self.water < ALERT_THRESHOLD or
                self.energy < ALERT_THRESHOLD)

    def _decay_all(self):
        self.food   = max(STAT_MIN, self.food   - DECAY_RATE)
        self.water  = max(STAT_MIN, self.water  - DECAY_RATE)
        self.energy = max(STAT_MIN, self.energy - DECAY_RATE)

    # ── Private helpers ──────────────────────────────────────────────────────

    def _on_action(self, action):
        """Shared logic for all button actions."""
        self._last_activity = time.ticks_ms()
        if not self._backlight_on:
            self._bl.value(1)
            self._backlight_on = True
        msg = MESSAGES[action][urandom.randint(0, len(MESSAGES[action]) - 1)]
        self._show_message(msg)
        self._redraw()

    def _trigger_alert(self):
        msg = MESSAGES["alert"][urandom.randint(0, len(MESSAGES["alert"]) - 1)]
        self._show_message(msg)
        self._play_tone(ALERT_FREQ, ALERT_DURATION)
        # Brief red LED flash
        self._set_led(1, 0, 0)
        time.sleep_ms(200)
        self._set_led(0, 0, 0)
        self._redraw_sprite("alert")

    def _redraw(self):
        mood = self.mood()
        self._last_mood = mood
        self._redraw_sprite(mood)
        if self._current_msg:
            self._draw_text(self._current_msg)

    def _redraw_sprite(self, name):
        data = _load_sprite(name)
        self._lcd.blit_buffer(data, SPRITE_X, SPRITE_Y, SPRITE_W, SPRITE_H)

    def _draw_indicators(self):
        """Draw the static button indicator row. Called once at init."""
        for i, (x, color, label) in enumerate(
                zip(INDICATOR_POSITIONS, INDICATOR_COLORS, INDICATOR_LABELS)):
            _draw_circle(self._lcd, x, INDICATOR_Y, INDICATOR_R, color)
            # Centre label text under circle
            lx = x - len(label) * 4  # rough centering for 8px-wide chars
            self._lcd.text(label, lx, INDICATOR_Y + INDICATOR_R + 4, WHITE)

    def _show_message(self, msg):
        self._current_msg = msg
        self._msg_clear_at = time.ticks_ms() + 2000
        self._draw_text(msg)

    def _draw_text(self, msg):
        self._clear_text_zone()
        x = max(0, (LCD_WIDTH - len(msg) * 8) // 2)  # rough centre
        self._lcd.text(msg, x, TEXT_Y, TEXT_COLOR)

    def _clear_text_zone(self):
        self._lcd.fill_rect(0, TEXT_Y, LCD_WIDTH, 20, BLACK)
```

**Step 5: Run tests**

```bash
python -m pytest tests/test_pet.py -v
```

Expected: all tests PASS. Fix any failures before continuing.

**Step 6: Commit**

```bash
git add tamagotchi.py tests/
git commit -m "feat: add Pet state machine with passing tests"
```

---

## Task 4: `main.py` — Boilerplate Game Loop + Participant Stubs

**Files:**
- Modify: `main.py`

**Step 1: Write `main.py`**

```python
# =============================================================================
# TOMOGATCHI WORKSHOP — main.py
# =============================================================================
#
# Welcome! This is YOUR file. Everything in the sections marked
# "=== YOUR CODE HERE ===" is for you to complete.
#
# The rest of the project is in tamagotchi.py — you don't need to edit it,
# but you're encouraged to read it and see how it all fits together.
#
# Workshop sections:
#   1. Button setup     — configure three input pins
#   2. LED helper       — control the RGB LED
#   3. Buzzer helper    — play tones with the piezo buzzer
#
# The game loop at the bottom is provided — once your three sections
# are complete, the full game will run.
# =============================================================================

from machine import Pin, PWM
import time
import machine
from tamagotchi import Pet


# =============================================================================
# SECTION 1: BUTTON SETUP
# =============================================================================
# The three buttons connect to GPIO pins on the Pico.
# Each button needs to be configured as an INPUT with a pull-down resistor.
# A pull-down resistor ensures the pin reads 0 when the button is NOT pressed,
# and 1 when it IS pressed.
#
# Use:  Pin(<number>, Pin.IN, Pin.PULL_DOWN)
#
# Pin numbers:
#   Red button    → GP22
#   Yellow button → GP21
#   Green button  → GP19
#
# HINT: Look at how btn_red is used in the game loop below — each button
# is read with .value(), which returns 0 or 1.
# =============================================================================

# === YOUR CODE HERE ===

# btn_red    = ...
# btn_yellow = ...
# btn_green  = ...


# =============================================================================
# SECTION 2: LED HELPER
# =============================================================================
# The RGB LED has three separate colour pins — one for red, one for green,
# one for blue. Setting a pin HIGH (1) turns that colour on.
#
# The three LED pins are already set up for you below.
# Your job is to complete the set_led() function so it sets each pin
# to the value passed in (0 for off, 1 for on).
#
# HINT: Use led_r.value(r) — and do the same for green and blue.
# =============================================================================

led_r = Pin(16, Pin.OUT)
led_g = Pin(17, Pin.OUT)
led_b = Pin(18, Pin.OUT)


def set_led(r, g, b):
    """Set the RGB LED colour. Each channel is 0 (off) or 1 (on)."""
    # === YOUR CODE HERE ===
    pass


# =============================================================================
# SECTION 3: BUZZER HELPER
# =============================================================================
# The piezoelectric buzzer is controlled with PWM (Pulse Width Modulation).
# PWM rapidly switches the pin on and off — the speed (frequency) determines
# the pitch, and the duty cycle determines the volume.
#
# The buzzer pin is already set up for you below.
# Your job is to complete the play_tone() function:
#   1. Set the frequency:   buzzer.freq(frequency)
#   2. Turn it on (50%):    buzzer.duty_u16(32768)
#   3. Wait:                time.sleep_ms(duration_ms)
#   4. Turn it off:         buzzer.duty_u16(0)
#
# HINT: duty_u16 sets the duty cycle from 0 (off) to 65535 (full on).
#       32768 is exactly 50% — a good middle ground for the buzzer.
# =============================================================================

buzzer = PWM(Pin(6))


def play_tone(frequency, duration_ms):
    """Play a tone at the given frequency (Hz) for duration_ms milliseconds."""
    # === YOUR CODE HERE ===
    pass


# =============================================================================
# GAME LOOP (provided — read, don't edit)
# =============================================================================
# This sets up the pet and runs the main loop.
# The pet receives your set_led and play_tone functions — once you've
# completed the sections above, your code will drive the game.
#
# Button debounce: we track the last button state to avoid registering
# a single press multiple times.
# =============================================================================

print("Starting Tomogatchi...")
pet = Pet(play_tone, set_led)

last_red    = 0
last_yellow = 0
last_green  = 0

while True:
    red    = btn_red.value()
    yellow = btn_yellow.value()
    green  = btn_green.value()

    if red and not last_red:
        pet.feed()
    elif yellow and not last_yellow:
        pet.water()
    elif green and not last_green:
        pet.exercise()

    last_red    = red
    last_yellow = yellow
    last_green  = green

    pet.update()
    machine.lightsleep(50)  # low-power wait between loop iterations
```

**Step 2: Manual verification**

Load `main.py` and `tamagotchi.py` onto the Pico via Thonny. The boilerplate sections should run; participant sections (`pass`) will do nothing yet. Verify:
- Display initialises and shows the pet sprite (placeholder colour block)
- Button indicator row (coloured circles) appears at the bottom
- No crashes on startup

**Step 3: Commit**

```bash
git add main.py
git commit -m "feat: add main.py with participant stubs and game loop"
```

---

## Task 5: Workshop Documentation — `workshop-guide.md`

**Files:**
- Create: `docs/workshop-guide.md`

Write the guide structured so each `##` heading = one slide. Body text = slide content + facilitator notes. Include speaker notes under each section as a `> **Facilitator note:**` blockquote.

```markdown
# Tomogatchi Workshop Guide

> Facilitator reference — structured for slide import.
> Each heading = one slide. Body text = slide bullets + speaker notes.
> Total time: ~1h 55min

---

## Welcome to the Tomogatchi Workshop

**What we're building today:**
- A virtual pet that lives on a tiny computer called a Raspberry Pi Pico
- It gets hungry, thirsty, and tired — your job is to keep it happy
- Three buttons: feed it, water it, get it moving

**What you'll learn:**
- How to wire a circuit on a breadboard
- How to write code that talks to physical hardware
- How MicroPython runs on a microcontroller

> **Facilitator note:** Keep this brief. 5 minutes max. Show the finished device running so participants know what they're working toward.

---

## What Is a Raspberry Pi Pico?

- A microcontroller — a tiny computer designed to control hardware
- Runs MicroPython: Python that talks directly to pins and sensors
- No screen, no keyboard — just code and components
- Used in everything from robots to weather stations to this workshop

**Key difference from a regular computer:**
- No operating system
- Code runs directly on the chip
- Your Python code IS the program

> **Facilitator note:** Show the physical Pico. Point out the GPIO pins along the edges. Have the pinout diagram visible on screen.

---

## Reading the Pinout

- GPIO = General Purpose Input/Output
- Each numbered pin can be an input (read a button) or output (control an LED)
- Some pins are special: power (3V3, GND), SPI, PWM
- We'll use: GP6, GP8–13, GP16–19, GP21–22

> **Facilitator note:** Hand out the participant-handout.md (or display it). Walk through the pin table together. Participants do not need to memorise this — they'll refer to it during wiring.

---

## Breadboard Basics

- A breadboard lets you build circuits without soldering
- Holes in the same row are electrically connected
- The two rails down the sides are for power (red = 3.3V) and ground (blue = GND)
- Components and jumper wires plug straight in

**Rule of thumb:** If it doesn't work, check your wiring first.

> **Facilitator note:** Draw or show a breadboard diagram. Demonstrate plugging in a single wire and explain the row connection. Common mistake: plugging into the wrong row by one hole.

---

## Wiring the Circuit — Step by Step

Wire in this order. Check each section before moving on.

**Display (already wired if using a pre-wired kit):**
| Signal | Pico Pin |
|--------|----------|
| SCK    | GP10     |
| MOSI   | GP11     |
| DC     | GP8      |
| CS     | GP9      |
| RST    | GP12     |
| BL     | GP13     |
| VCC    | 3V3      |
| GND    | GND      |

**RGB LED:**
| LED pin | Pico Pin |
|---------|----------|
| Red     | GP16     |
| Green   | GP17     |
| Blue    | GP18     |
| GND     | GND      |

**Buzzer:**
| Buzzer pin | Pico Pin |
|------------|----------|
| +          | GP6      |
| –          | GND      |

**Buttons (one at a time):**
| Button | Pico Pin |
|--------|----------|
| Red    | GP22     |
| Yellow | GP21     |
| Green  | GP19     |

Other button leg → GND

> **Facilitator note:** 20 minutes. Walk the room as participants wire up. Common pitfalls: buttons not seated fully, LED legs in wrong order, buzzer polarity reversed (swap + and – if silent). Have spare components ready.

---

## Checkpoint 1 — Display Test

**Flash the project files onto your Pico:**
1. Open Thonny
2. Connect your Pico via USB
3. Select "MicroPython (Raspberry Pi Pico)" in the bottom-right
4. Open `main.py` — press the green Run button

**You should see:** The pet appears on screen (a coloured block for now — the art comes later!)

If you see an error — check the wiring for the display pins first.

> **Facilitator note:** 5 minutes. Help anyone who can't connect — most issues are Thonny port selection or the Pico needing to be unplugged and replugged.

---

## Section 1: Button Setup

**What you're doing:** Telling the Pico which pins have buttons connected, and how to read them.

**New concept — pull-down resistor:**
- Without it, an unconnected input pin "floats" and reads random values
- `Pin.PULL_DOWN` keeps the pin at 0 until the button pulls it to 3.3V
- Result: pin reads 0 when button is NOT pressed, 1 when it IS pressed

**Your task:** In `main.py`, find Section 1 and create three Pin objects:
```python
btn_red    = Pin(22, Pin.IN, Pin.PULL_DOWN)
btn_yellow = Pin(21, Pin.IN, Pin.PULL_DOWN)
btn_green  = Pin(19, Pin.IN, Pin.PULL_DOWN)
```

> **Facilitator note:** 20 minutes including Checkpoint 2. Explain PULL_DOWN first, then let participants write. Walk the room. Common mistake: forgetting `Pin.PULL_DOWN` — the buttons will appear to press randomly.

---

## Checkpoint 2 — Button Test

Add this to the bottom of `main.py` temporarily (below your Pin setup):

```python
while True:
    print(btn_red.value(), btn_yellow.value(), btn_green.value())
    time.sleep_ms(100)
```

Open the Thonny console. Press each button — you should see a 1 appear for each button you hold.

Remove the test loop before continuing.

> **Facilitator note:** If a button reads 1 all the time without being pressed — check for a short circuit or missing PULL_DOWN. If it never reads 1 — check the wiring.

---

## Section 2: Buzzer

**What you're doing:** Making the Pico play a tone through the piezoelectric buzzer.

**New concept — PWM (Pulse Width Modulation):**
- PWM switches a pin on and off very rapidly
- The frequency controls the pitch (faster = higher note)
- The duty cycle controls how long each pulse is "on" vs "off"
- `duty_u16(32768)` = 50% duty cycle — a good default for buzzers

**Your task:** Complete `play_tone(frequency, duration_ms)`:
```python
def play_tone(frequency, duration_ms):
    buzzer.freq(frequency)
    buzzer.duty_u16(32768)
    time.sleep_ms(duration_ms)
    buzzer.duty_u16(0)
```

> **Facilitator note:** 15 minutes including Checkpoint 3. If the buzzer makes no sound — check polarity (swap + and –). If it makes a constant tone — `duty_u16(0)` is probably missing.

---

## Checkpoint 3 — Buzzer Test

Add this temporarily below your `play_tone` function:

```python
play_tone(440, 300)  # play A4 for 300ms
```

You should hear a short beep. Try changing the frequency — higher numbers = higher pitch.

Remove the test line before continuing.

---

## Section 3: LED

**What you're doing:** Controlling the RGB LED to show colours.

**Concept:** The RGB LED has three independent colour channels — red, green, blue. Setting a pin HIGH (1) turns that colour on. Combine channels to mix colours.

**Your task:** Complete `set_led(r, g, b)`:
```python
def set_led(r, g, b):
    led_r.value(r)
    led_g.value(g)
    led_b.value(b)
```

Try it: `set_led(1, 0, 0)` = red, `set_led(0, 1, 0)` = green, `set_led(1, 1, 0)` = yellow.

> **Facilitator note:** 10 minutes. This is the quickest section — most participants will finish early. Encourage them to test colours. If the LED is dim or wrong colour — check the pin assignments.

---

## Final Demo — Your Pet Is Alive!

Run the full project. Your pet should now:
- Show its face on screen
- React when you press each button
- Display an encouragement message
- Play a tone and flash the LED
- Get hungry and sad if you ignore it
- Buzz to remind you when it needs attention

**The coloured circles at the bottom** show which button does what — red for food, yellow for water, green for exercise.

> **Facilitator note:** 5 minutes. Let participants play! Walk around and congratulate everyone. If anything isn't working — quick triage: is the error in the console? Is it a wiring issue or a code issue?

---

## Extensions — Go Further

Finished early? Try these:

- **Design your own sprite:** Use [piskel.com](https://www.piskelapp.com) to draw a 120×120 pet face. Export as PNG, run `python tools/convert.py face.png happy.raw`, copy to your Pico.
- **Change the decay rate:** In `tamagotchi.py`, find `DECAY_RATE` and `DECAY_INTERVAL` — make your pet needier or more independent.
- **Add a new mood:** Add a fourth mood state (e.g. `"excited"`) with its own image and trigger condition.
- **Adjust encouragement messages:** Find the `MESSAGES` dictionary in `tamagotchi.py` and customise what your pet says.

> **Facilitator note:** 5 minutes. Not everyone will get here — that's fine. Share the repo link so they can continue at home.

---

## Wrap Up

**What you built:**
- A complete interactive device with a display, buttons, LED, and buzzer
- Hardware-interfacing code in MicroPython
- A running state machine that manages your pet's mood over time

**What you learned:**
- GPIO input/output
- Pull-down resistors
- PWM for audio
- How hardware and code work together

**Take it home!** The device is yours. Keep your pet alive.
```

**Step 2: Commit**

```bash
git add docs/workshop-guide.md
git commit -m "docs: add slide-ready workshop facilitator guide"
```

---

## Task 6: Workshop Documentation — `participant-handout.md` + `wiring-diagram.md`

**Files:**
- Create: `docs/participant-handout.md`
- Create: `docs/wiring-diagram.md`

**Step 1: Write `docs/participant-handout.md`**

```markdown
# Tomogatchi Workshop — Participant Reference

Keep this handy while you work.

---

## Pin Reference

| Component     | Signal  | Pico GPIO |
|---------------|---------|-----------|
| Display       | SCK     | GP10      |
| Display       | MOSI    | GP11      |
| Display       | DC      | GP8       |
| Display       | CS      | GP9       |
| Display       | RST     | GP12      |
| Display       | BL      | GP13      |
| LED           | Red     | GP16      |
| LED           | Green   | GP17      |
| LED           | Blue    | GP18      |
| Button        | Red     | GP22      |
| Button        | Yellow  | GP21      |
| Button        | Green   | GP19      |
| Buzzer        | +       | GP6       |

All GND pins connect to any GND on the Pico.
All power (VCC) pins connect to 3V3 on the Pico.

---

## MicroPython Quick Reference

```python
# Digital input with pull-down
pin = Pin(22, Pin.IN, Pin.PULL_DOWN)
pin.value()         # returns 0 or 1

# Digital output
pin = Pin(16, Pin.OUT)
pin.value(1)        # HIGH
pin.value(0)        # LOW

# PWM
pwm = PWM(Pin(6))
pwm.freq(440)           # set frequency in Hz
pwm.duty_u16(32768)     # 50% duty cycle (on)
pwm.duty_u16(0)         # off

# Delay
time.sleep_ms(100)      # wait 100 milliseconds
```

---

## Your Code Sections

| Section | What you write | Where |
|---------|---------------|-------|
| 1 — Buttons | Three `Pin` objects | Below the Section 1 comment |
| 2 — LED | Body of `set_led(r, g, b)` | Replace the `pass` |
| 3 — Buzzer | Body of `play_tone(freq, ms)` | Replace the `pass` |

---

## Glossary

**GPIO** — General Purpose Input/Output. The numbered pins on the Pico that can be inputs or outputs.

**Pull-down resistor** — Keeps a pin at 0V when nothing is connected, so floating inputs don't cause random reads.

**PWM** — Pulse Width Modulation. Rapidly switching a pin on and off to control things like motor speed or buzzer pitch.

**Duty cycle** — The fraction of time a PWM signal is "on". 50% means on half the time.

**RGB565** — A way of storing colours in 2 bytes: 5 bits red, 6 bits green, 5 bits blue.

**MicroPython** — A version of Python that runs directly on microcontrollers without an operating system.

---

## Extension: Make Your Own Sprite

1. Go to [piskel.com](https://www.piskelapp.com) — free, no account needed
2. Create a new sprite, set canvas to 120×120
3. Draw your pet face
4. Export as PNG
5. On your laptop, run: `python tools/convert.py yourface.png images/happy.raw`
6. Copy `images/happy.raw` to your Pico via Thonny
7. Rerun the project — your face appears!
```

**Step 2: Write `docs/wiring-diagram.md`**

```markdown
# Tomogatchi — Wiring Diagram

Wire components in this order. Test after each section.

---

## Pico Orientation

Place the Pico at the top of the breadboard with the USB port facing up.
The left column of pins is the left rail, the right column is the right rail.

---

## Step 1: Power Rails

Connect Pico 3V3 (pin 36) → breadboard red power rail (+).
Connect Pico GND (pin 38) → breadboard blue power rail (–).

---

## Step 2: Display

The display has 8 pins. Connect each to the Pico:

| Display label | Wire to  |
|---------------|----------|
| GND           | GND rail |
| VCC           | 3V3 rail |
| SCL (clock)   | GP10     |
| SDA (data)    | GP11     |
| RES (reset)   | GP12     |
| DC            | GP8      |
| CS            | GP9      |
| BLK (backlight)| GP13   |

---

## Step 3: RGB LED

The RGB LED has 4 legs. The longest leg is GND (common cathode).

| Leg      | Wire to  |
|----------|----------|
| Red (R)  | GP16     |
| GND (longest) | GND rail |
| Green (G)| GP17     |
| Blue (B) | GP18     |

> **Note:** If colours appear wrong, the legs may be in a different order — check your LED's datasheet.

---

## Step 4: Buzzer

The buzzer has a + and – marking on the top.

| Buzzer | Wire to |
|--------|---------|
| +      | GP6     |
| –      | GND rail|

> **Note:** If the buzzer makes no sound, swap the + and – wires.

---

## Step 5: Buttons

Each button straddles the centre gap of the breadboard.
One leg connects to the Pico GPIO, the other to GND.

| Button | GPIO leg | GND leg |
|--------|----------|---------|
| Red    | GP22     | GND rail|
| Yellow | GP21     | GND rail|
| Green  | GP19     | GND rail|

> **Note:** The pull-down resistor is configured in software (`Pin.PULL_DOWN`) — no physical resistor needed.

---

## Wiring Checklist

- [ ] 3V3 → red power rail
- [ ] GND → blue power rail
- [ ] All 8 display pins connected
- [ ] RGB LED — correct leg order, GND to rail
- [ ] Buzzer — + to GP6, – to GND
- [ ] Red button — GP22 + GND
- [ ] Yellow button — GP21 + GND
- [ ] Green button — GP19 + GND
```

**Step 3: Commit**

```bash
git add docs/participant-handout.md docs/wiring-diagram.md
git commit -m "docs: add participant handout and wiring diagram"
```

---

## Task 7: Final Integration Check

**Step 1: Verify file structure**

```bash
find . -not -path './.git/*' | sort
```

Expected:
```
./images/alert.raw
./images/happy.raw
./images/okay.raw
./images/sad.raw
./main.py
./tamagotchi.py
./st7789.py
./tools/convert.py
./tools/make_placeholders.py
./tests/mock_pet.py
./tests/test_pet.py
./docs/plans/2026-02-18-tomogatchi-design.md
./docs/plans/2026-02-18-tomogatchi-implementation.md
./docs/workshop-guide.md
./docs/participant-handout.md
./docs/wiring-diagram.md
```

**Step 2: Run full test suite**

```bash
python -m pytest tests/ -v
```

Expected: all tests PASS.

**Step 3: Load onto Pico and verify manually**

Files to copy to Pico via Thonny:
- `main.py`
- `tamagotchi.py`
- `st7789.py`
- `images/` (all four .raw files)

Verify checklist:
- [ ] Display shows pet sprite on boot
- [ ] Coloured circles appear in the bottom row
- [ ] Pressing red button shows a message and plays a tone (once Section 3 complete)
- [ ] Backlight turns off after 30 seconds of inactivity
- [ ] Backlight wakes on button press
- [ ] Stat decay occurs over time
- [ ] Pet face changes from happy → okay → sad as stats fall
- [ ] Buzzer alert fires when a stat drops below 30

**Step 4: Final commit**

```bash
git add .
git commit -m "feat: complete tomogatchi workshop project"
```

---

## Deliverables Summary

| File | Status |
|------|--------|
| `main.py` | Participant file with stubs |
| `tamagotchi.py` | Full boilerplate |
| `st7789.py` | Display driver |
| `images/*.raw` | Placeholder sprites |
| `tools/convert.py` | PNG→raw converter |
| `tools/make_placeholders.py` | Placeholder generator |
| `tests/test_pet.py` | Pet logic tests |
| `tests/mock_pet.py` | Host-testable Pet mock |
| `docs/workshop-guide.md` | Slide-ready facilitator guide |
| `docs/participant-handout.md` | Pin ref + glossary |
| `docs/wiring-diagram.md` | Step-by-step wiring |
