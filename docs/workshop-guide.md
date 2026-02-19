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

- **Design your own sprite:** Use [piskel.com](https://www.piskelapp.com) to draw a 120x120 pet face. Export as PNG, run `python tools/convert.py face.png happy.raw`, copy to your Pico.
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
