# Tomogatchi Workshop Guide

> Facilitator reference — structured for slide import.
> Each heading = one slide. Body text = slide bullets + speaker notes.
> Total time: ~2 hours

---

## Welcome to the Tomogatchi Workshop

**What we're building today:**
- A virtual pet that lives on a Raspberry Pi Pico microcontroller
- It gets hungry, thirsty, and tired — your job is to keep it happy
- Three buttons: feed it, water it, get it moving

**Your pet starts alive — but broken.**
It shows one face and does nothing else. You're going to bring it to life,
piece by piece, by wiring up each hardware system and writing the code to drive it.

**What you'll learn:**
- How to wire a circuit on a breadboard
- How to write C++ that talks directly to physical hardware
- How multi-file programs are structured
- How Arduino sketches work on real embedded hardware

> **Facilitator note:** 5 minutes max. Show the finished device running so
> participants know what they're working toward. Emphasise: "everything you
> see happening was written by someone in a workshop like this one."

---

## Why C++?

- Arduino C++ is the language of real embedded systems
- The same patterns you'll write today — `pinMode`, `digitalRead`, `tone` —
  work on STM32, ESP32, AVR, and almost every other microcontroller
- You're learning something that transfers directly to industry work
- MicroPython is great for scripting. C++ is great for hardware.

> **Facilitator note:** Keep this to 2 minutes. IEEE audience will appreciate
> the framing. Don't dwell — they're here to build.

---

## What Is a Raspberry Pi Pico?

- A microcontroller — a tiny computer designed to control hardware directly
- Runs C++ compiled with the Arduino toolchain
- No operating system, no file system, no screen of its own
- Your compiled code IS the program — it runs the moment it powers on
- Used in robotics, sensor networks, wearables, and this workshop

**Key difference from a regular computer:**
- No OS — your code has full control of every pin
- Code runs bare-metal directly on the RP2040 chip
- `setup()` runs once; `loop()` runs forever

> **Facilitator note:** Show the physical Pico. Point out the GPIO pins along
> the edges. Have the pinout diagram visible on screen.

---

## Toolchain Setup

**If not already installed:**

1. Download **Arduino IDE 2** from arduino.cc
2. Open Preferences, paste this URL into "Additional boards manager URLs":
   ```
   https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json
   ```
3. Open **Tools > Board > Boards Manager**, search "pico", install
   **"Raspberry Pi Pico/RP2040 by Earle Philhower"**
4. Open **Tools > Manage Libraries**, install:
   - `Adafruit ST7789`
   - `Adafruit GFX Library`

> **Facilitator note:** Ideally pre-installed on workshop laptops.
> If not, allow 10 minutes here. Common issue: participants install the
> official Arduino-Mbed Pico package instead of Earle Philhower — wrong one.

---

## How Arduino Sketches Work

- A sketch is a folder containing `.ino`, `.h`, and `.cpp` files
- **All files in the same folder are compiled together** — the IDE shows them as tabs
- `.h` = header file: declares functions so other files can call them
- `.cpp` = source file: defines (implements) the functions
- `.ino` = the main sketch: contains `setup()` and `loop()`

**Today's file structure:**
```
tomogatchi/
  tomogatchi.ino    <- your main sketch (you edit this)
  buttons.h/.cpp   <- Section 1 (you write this)
  sound.h/.cpp     <- Section 2 (you write this)
  leds.h/.cpp      <- Section 3 (you write this)
  Pet.h/.cpp       <- the pet engine (read-only, read it!)
  sprites.h        <- pixel art stored in flash memory
```

> **Facilitator note:** Click through the tabs in the IDE to show this live.
> Explain: "Pet.h is like a public API. You call its methods but you don't
> need to understand every line inside it — same as using any library."

---

## Reading the Pinout

- GPIO = General Purpose Input/Output
- Each numbered pin can be an input (read a button) or output (control an LED)
- Some pins have special functions: SPI for the display, PWM for audio
- We'll use: GP6, GP8-13, GP16-19, GP21-22

> **Facilitator note:** Hand out or display the pinout diagram.
> Walk through the pin table together. Participants do not need to
> memorise this — they'll refer to it during wiring.

---

## Breadboard Basics

- A breadboard lets you build circuits without soldering
- Holes in the same row are electrically connected
- The two rails down the sides are for power (red = 3.3V) and ground (blue = GND)
- Components and jumper wires plug straight in

**Rule of thumb:** If it doesn't work, check your wiring first.

> **Facilitator note:** Draw or show a breadboard diagram. Demonstrate
> plugging in a single wire and explain the row connection.
> Common mistake: plugging into the wrong row by one hole.

---

## Wiring the Circuit

Wire in this order. Check each section before moving on.

**Display (pre-wired if using a kit):**
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
| Buzzer | Pico Pin |
|--------|----------|
| +      | GP6      |
| -      | GND      |

**Buttons:**
| Button | Pico Pin | Other leg |
|--------|----------|-----------|
| Red    | GP22     | GND       |
| Yellow | GP21     | GND       |
| Green  | GP19     | GND       |

> **Facilitator note:** 20 minutes. Walk the room as participants wire up.
> Common pitfalls: buttons not seated fully, LED legs in wrong order,
> buzzer polarity reversed (swap + and - if silent).

---

## Checkpoint 0 - Pet Boots

**Upload the sketch:**
1. Open the `tomogatchi` folder in Arduino IDE
2. Connect your Pico via USB
3. Select **Tools > Board > Raspberry Pi Pico**
4. Select the correct port under **Tools > Port**
5. Click **Upload** (the right-arrow button)

**You should see:** Your pet's face appears on the display.
Pressing buttons does nothing. No sound. LED is off. That's correct for now.

> **Facilitator note:** 5 minutes. Most issues here are port selection or the
> Pico needing to be unplugged and replugged. If upload fails, try holding
> BOOTSEL while plugging in to force bootloader mode.

---

## Section 1 - Buttons + Catchphrases

**Files: `buttons.h` and `buttons.cpp`**

**New concepts:**
- `pinMode(pin, INPUT_PULLDOWN)` - configure a pin to read input
- `INPUT_PULLDOWN` keeps the pin at LOW until the button connects it to 3.3V
- `digitalRead(pin)` - returns HIGH (1) or LOW (0)
- The "last state" trick - detect a fresh press, not a held press

**Your tasks:**

In `buttons.h` - declare the functions:
```cpp
void setupButtons();
void readButtons(Pet& pet);
```

In `buttons.cpp` - implement them:
```cpp
void setupButtons() {
    pinMode(22, INPUT_PULLDOWN);
    pinMode(21, INPUT_PULLDOWN);
    pinMode(19, INPUT_PULLDOWN);
}

void readButtons(Pet& pet) {
    static bool lastRed = false, lastYellow = false, lastGreen = false;
    bool red    = digitalRead(22);
    bool yellow = digitalRead(21);
    bool green  = digitalRead(19);
    if (red    && !lastRed)    pet.say(pet.catchphrase());
    if (yellow && !lastYellow) pet.say(pet.catchphrase());
    if (green  && !lastGreen)  pet.say(pet.catchphrase());
    lastRed = red; lastYellow = yellow; lastGreen = green;
}
```

Then in `tomogatchi.ino` uncomment `setupButtons()` and `readButtons(pet)`.

> **Facilitator note:** 20 minutes including Checkpoint 1.
> Common mistake: forgetting `INPUT_PULLDOWN` - buttons fire randomly.
> The `static` keyword inside a function is new to many - explain it persists
> between calls. Note: INPUT_PULLDOWN is Pico-specific. Standard Arduino boards
> use INPUT_PULLUP with inverted logic (HIGH = not pressed).

---

## Checkpoint 1 - Pet Speaks

Press any button. Your pet shows a phrase on screen.

The phrase changes based on the pet's mood - try pressing when happy vs sad.

> **Facilitator note:** If a button always reads as pressed: short circuit or
> wrong pull mode. If it never responds: check wiring.

---

## Section 2 - Buzzer + Melody

**Files: `sound.h` and `sound.cpp`**

**New concepts:**
- `tone(pin, freq, duration)` - generates a square wave at the given frequency
- `noTone(pin)` - stops the tone
- Frequency = pitch: 440Hz = A4, 523Hz = C5, higher = higher pitch
- A 2D array to store a melody: `int notes[][2] = {{523, 150}, {659, 150}}`

**Your tasks:**

In `sound.h` - declare:
```cpp
void setupBuzzer();
void playTone(int freq, int duration);
void playMelody(int notes[][2], int len);
```

In `sound.cpp` - implement and compose your melody:
```cpp
void setupBuzzer() { pinMode(6, OUTPUT); }

void playTone(int freq, int duration) {
    tone(6, freq, duration);
    delay(duration);
    noTone(6);
}

int WAKE_MELODY[][2] = {{523,150},{659,150},{784,300}};
const int WAKE_MELODY_LEN = 3;

void playMelody(int notes[][2], int len) {
    for (int i = 0; i < len; i++)
        playTone(notes[i][0], notes[i][1]);
}
```

In `buttons.cpp`, update the red button to play the melody:
```cpp
if (red && !lastRed) {
    playMelody(WAKE_MELODY, WAKE_MELODY_LEN);
    pet.say(pet.catchphrase());
}
```

> **Facilitator note:** 15 minutes including Checkpoint 2.
> If buzzer is silent: check polarity (swap + and -).
> tone() blocks - this is intentional here, explain it.
> Encourage changing note values and listening.

---

## Checkpoint 2 - Pet Has a Voice

Press the red button. Melody plays, phrase shows.

Try changing the frequency values. What's the highest note you can hear?

---

## Section 3 - RGB LED + Simon Says

**Files: `leds.h` and `leds.cpp`**

**New concepts:**
- `digitalWrite(pin, HIGH/LOW)` - turn a digital output on or off
- RGB LED: three independent colour channels mixed together
- `random(n)` - returns a random integer from 0 to n-1

**Your tasks:**

In `leds.h` - declare:
```cpp
void setupLeds();
void setLed(int r, int g, int b);
bool playSimon();
```

In `leds.cpp` - implement setupLeds and setLed:
```cpp
void setupLeds() {
    pinMode(16, OUTPUT);
    pinMode(17, OUTPUT);
    pinMode(18, OUTPUT);
}

void setLed(int r, int g, int b) {
    digitalWrite(16, r);
    digitalWrite(17, g);
    digitalWrite(18, b);
}
```

`playSimon()` is already written in `leds.cpp` - read it, don't edit it.
It uses YOUR `setLed()` and `playTone()`.

In `buttons.cpp` add to the yellow button:
```cpp
if (yellow && !lastYellow) {
    bool won = playSimon();
    won ? pet.feed() : pet.say("Nope...");
}
```

> **Facilitator note:** 20 minutes including Checkpoint 3.
> RGB mixing is always fun - encourage setLed(1,1,0) yellow, setLed(1,0,1) magenta.
> Payoff moment: their setLed() and playTone() now drive a real game.
> Common issue: wrong colours - check GP16=Red, GP17=Green, GP18=Blue.

---

## Checkpoint 3 - Simon Says

Yellow button triggers Simon Says. LED flashes a 3-colour sequence.
Press the matching buttons in order.

Win: pet gets fed. Lose: "Nope..."

---

## Section 4 - Button Mash + Full Game

**File: `tomogatchi.ino`**

**New concepts:**
- `millis()` - milliseconds since the Pico started
- `millis() - start < 3000` - a non-blocking elapsed time check
- Counters: tracking button presses in a time window

**Your tasks:**

1. Uncomment `pet.enableDecay()` in `setup()` - stats now decay over time.
   The game is real.

2. Replace `loop()` with the button mash version from the comment block
   in `tomogatchi.ino`. Green button opens a 3-second mash window.
   The count is passed to `pet.exercise(presses)`.

> **Facilitator note:** 15 minutes. When they call enableDecay() the game goes
> live - stats start falling. Leave the pet alone for 30 seconds, watch it
> get sad. Then mash green and watch it recover.

---

## Checkpoint 4 - Full Game

Everything is live:
- Stats decay over time
- Red: feed | Yellow: water + Simon Says | Green: 3-second mash
- Happy / okay / sad / dead faces
- LED flashes red when attention is needed
- Melody plays on button press

Leave it alone. Watch it die. Bring it back.

---

## Extensions - Go Further

**Art:**
- Draw a 120x120 face at piskel.com
- Export as PNG, then: `python tools/convert.py face.png face.h --header --name MYFACE`
- Add `#include "face.h"` to sprites.h and use SPRITE_MYFACE in Pet.cpp

**Sound:**
- Compose a sad melody and switch melodies based on `pet.mood()`
- Try: `if (pet.mood() == Mood::SAD) playMelody(SAD_MELODY, SAD_LEN);`

**Game tuning:**
- Change `DECAY_RATE` or `DECAY_INTERVAL` in Pet.cpp
- Increase Simon sequence length from 3 to 5 in leds.cpp
- Add a secret button combo

> **Facilitator note:** ~30 minutes free time. Share the repo link.

---

## Wrap Up

**What you built:**
- A complete interactive embedded device with display, buttons, LED, and buzzer
- Hardware-interfacing code in Arduino C++
- A multi-file C++ program with headers, source files, and a state machine

**What you learned:**
- GPIO: `pinMode`, `digitalRead`, `digitalWrite`
- PWM audio: `tone()` and frequency
- RGB colour mixing
- `millis()` for elapsed time
- Header files and multi-file C++ compilation
- How hardware and software work together in real embedded systems

**Take it home.** Keep your pet alive.

---

## Facilitator Quick Reference

| Problem | Cause | Fix |
|---------|-------|-----|
| Buttons fire randomly | Missing INPUT_PULLDOWN | Add third arg to pinMode |
| Button never responds | Bad wiring | Check jumper from button to GP pin |
| Buzzer silent | Reversed polarity | Swap + and - |
| Wrong LED colour | Wrong pin order | GP16=R, GP17=G, GP18=B |
| Upload fails | Wrong port or board | Check Tools > Board and Tools > Port |
| Upload fails (no port) | Pico not in normal mode | Hold BOOTSEL, plug in, release |
| Wrong board warning | Arduino-Mbed package | Must use Earle Philhower package |
| tone() question | "Why does it freeze?" | Explain blocking is intentional here |
