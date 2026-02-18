# Tomogatchi Workshop — Design Document
**Date:** 2026-02-18
**Status:** Approved

---

## Overview

A Tamagotchi-style virtual pet built on a Raspberry Pi Pico running MicroPython, designed as a beginner workshop project. Participants wire a breadboard circuit and write the hardware interfacing code (buttons, buzzer, LED) while the game logic, display driver, and pet state machine are provided as readable boilerplate.

---

## Hardware

| Component | Detail |
|-----------|--------|
| Microcontroller | Raspberry Pi Pico |
| Display | 1.5" IPS TFT, 240×240px, ST7789 driver, SPI |
| Buttons | 3× GPIO buttons — red (GP22), yellow (GP21), green (GP19) |
| Buzzer | Piezoelectric, PWM on GP6 |
| LED | RGB LED — red (GP16), green (GP17), blue (GP18) |
| Power | Battery powered |

---

## File Structure

```
tomogatchi/
├── main.py               # Workshop file — participants edit this
├── tamagotchi.py         # Game logic boilerplate — provided, read-only
├── st7789.py             # ST7789 display driver — provided, read-only
├── images/
│   ├── happy.raw         # 120×120 RGB565 raw image — placeholder, draw in later
│   ├── okay.raw
│   ├── sad.raw
│   └── alert.raw         # Shown when a stat triggers a buzzer reminder
├── tools/
│   └── convert.py        # Host-side script: PNG → RGB565 raw (requires Pillow)
└── docs/
    ├── plans/
    │   └── 2026-02-18-tomogatchi-design.md
    ├── workshop-guide.md
    ├── participant-handout.md
    └── wiring-diagram.md
```

---

## Architecture

### Two-file split

**`main.py`** — the only file participants edit. Contains four clearly marked sections:

1. Imports and hardware setup (button `Pin` objects, buzzer `PWM`)
2. `set_led(r, g, b)` — participants implement
3. `play_tone(freq, duration_ms)` — participants implement
4. Game loop — provided, calls into `tamagotchi.py`, participants read but don't write

**`tamagotchi.py`** — all boilerplate. Participants can read it to understand how the pet works. Exposes a clean API:

```python
pet = Pet(lcd, play_tone, set_led)
pet.feed()        # called when red button pressed
pet.water()       # called when yellow button pressed
pet.exercise()    # called when green button pressed
pet.update()      # called every loop iteration — handles decay, alerts, redraw
```

Hardware objects configured by participants in `main.py` are passed into `Pet()` at construction, so the boilerplate never references hardware pins directly. Participant code is wired into the game without them needing to understand the full loop.

---

## Pet State Machine

### Stats

Three independent stats, each 0–100:

| Stat | Button | Action |
|------|--------|--------|
| Food | Red | `pet.feed()` — adds +20, capped at 100 |
| Water | Yellow | `pet.water()` — adds +20, capped at 100 |
| Energy | Green | `pet.exercise()` — adds +20, capped at 100 |

Stats decay over time at a fixed rate using `time.ticks_ms()` (time-based, not loop-based).

### Mood

Derived from stats on each `update()` call, not stored:

| Condition | Mood |
|-----------|------|
| All stats ≥ 60 | `happy` |
| Any stat < 40 | `sad` |
| Otherwise | `okay` |

### Alerts

When any stat drops below 30, the buzzer fires a short reminder tone and the `alert.raw` sprite is briefly shown. This is the pet's "check in" notification. LED flashes red during alert.

---

## Display Layout

Screen: 240×240px

```
┌────────────────────────┐
│                        │
│      [  sprite  ]      │  120×120px, centered, y-offset ~20px
│                        │
│   "You're doing great!"│  encouragement text, centered, ~40px band
│                        │
│  ● Food ● Water ● Move │  static colored circles + labels (red/yellow/green)
└────────────────────────┘
```

- **Sprite**: 120×120 RGB565 raw file, loaded from `images/` by mood name
- **Text zone**: Encouragement message shown for ~2 seconds after each button press, then cleared. Messages are randomly selected from a list per action. Rendered using the built-in text support in the russhughes ST7789 driver.
- **Button indicator row**: Three static filled circles (red, yellow, green) with labels "Food", "Water", "Move". Always visible. No dynamic state. Reminds participants which physical button does what.

### Sprite workflow

Sprites are designed externally (recommended: [Piskel](https://www.piskelapp.com), free, browser-based), exported as PNG, converted to 120×120 RGB565 raw using `tools/convert.py`, then copied to the Pico via Thonny. Placeholder `.raw` files (solid color blocks) are pre-loaded so the project runs immediately without finished art.

Extension activity for participants: design your own pet face.

---

## Power Saving

Battery-powered device. Power saving is implemented entirely in boilerplate:

| Technique | Detail |
|-----------|--------|
| `machine.lightsleep(ms)` | Used in place of `time.sleep_ms()` in main loop — Pico enters low-power state between iterations |
| Display backlight timeout | Backlight off after 30s of inactivity, restored on any button press |
| LED off when idle | RGB LED only active on button press or alert, not continuously |
| Conditional redraw | Display only redraws when pet state or message changes |

A comment in `tamagotchi.py` explains why `lightsleep` is used — teachable moment for participants who read the boilerplate.

---

## Participant Sections

All sections in `main.py` are marked with:

```python
# ============================================================
# === YOUR CODE HERE ==========================================
# ============================================================
```

With explanatory comments above each section describing:
- What the section does
- What concepts it uses (GPIO, PWM, etc.)
- What a correct implementation should produce
- A hint (not a solution)

### Section 1 — Button setup
Configure three `Pin` objects with `Pin.IN` and `Pin.PULL_DOWN`. Concepts: GPIO, input pins, pull-down resistors.

### Section 2 — LED helper
Implement `set_led(r, g, b)` using the three LED `Pin` objects. Concepts: digital output, functions.

### Section 3 — Buzzer helper
Implement `play_tone(freq, duration_ms)` using a `PWM` object. Concepts: PWM, frequency, duty cycle.

---

## Workshop Outline

Target audience: complete beginners, 1.5–2 hours.

| # | Section | Time |
|---|---------|------|
| 1 | Welcome & intro — what's a Pico, what's MicroPython, what we're building | 10 min |
| 2 | Hardware walkthrough — identify components, breadboard basics, pinout | 15 min |
| 3 | Wiring the circuit — guided step-by-step, facilitator demos first | 20 min |
| 4 | Checkpoint 1 — flash boilerplate, confirm display shows the pet | 5 min |
| 5 | Participant section: Buttons — explain GPIO + pull-downs, participants implement | 20 min |
| 6 | Checkpoint 2 — button presses print to console | 5 min |
| 7 | Participant section: Buzzer — explain PWM, participants implement `play_tone()` | 15 min |
| 8 | Checkpoint 3 — buzzer fires on button press | 5 min |
| 9 | Participant section: LED — explain `set_led()`, participants implement | 10 min |
| 10 | Final demo — full game running, feed/water/exercise the pet | 5 min |
| 11 | Wrap-up & extensions — custom sprites, new stats, decay rate tweaks | 5 min |

**Total: ~1h 55min**

### Common pitfalls

- Wrong pin numbers — always cross-reference the pinout diagram
- Floating inputs — forgetting `Pin.PULL_DOWN` causes random button triggers
- Buzzer polarity — piezo buzzers are directional, swap wires if silent
- Thonny not connecting — Pico may need to be re-flashed or port selected manually
- `lightsleep` blocks serial output — remind participants to disable it during debugging by commenting out the sleep line

---

## Deliverables Checklist

- [ ] `main.py` — stubbed participant file with instructional comments
- [ ] `tamagotchi.py` — complete boilerplate: pet state machine, display rendering, stat decay, alerts, power saving
- [ ] `st7789.py` — ST7789 driver
- [ ] `images/` — placeholder `.raw` files (solid color, 120×120)
- [ ] `tools/convert.py` — PNG to RGB565 conversion script
- [ ] `docs/workshop-guide.md` — slide-ready facilitator guide
- [ ] `docs/participant-handout.md` — pin reference, code hints, glossary
- [ ] `docs/wiring-diagram.md` — step-by-step breadboard wiring with pin table
