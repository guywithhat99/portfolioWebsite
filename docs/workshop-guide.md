# Tomogatchi Workshop Guide

> Facilitator reference — each heading = one slide.
> Total time: ~2 hours

---

## Welcome to the Tomogatchi Workshop

- We're building a virtual pet on a Raspberry Pi Pico with 3 buttons, an LED, a buzzer, and a screen
- Your pet gets hungry, thirsty, and tired — keep it alive
- "Your pet starts alive but broken — one face, does nothing. You bring it to life piece by piece."

> **Facilitator note:** 5 min max. Show the finished device running.

---

## Why C++?

- Arduino C++ is real embedded — the same `pinMode`, `digitalRead`, `tone` patterns work on STM32, ESP32, AVR
- You're learning something that transfers directly to industry hardware work

> **Facilitator note:** 2 min.

---

## What Is a Raspberry Pi Pico?

- A microcontroller — no OS, no file system, bare metal
- Your compiled code IS the program — runs the moment it powers on
- `setup()` runs once, `loop()` runs forever

> **Facilitator note:** Show the physical Pico. Point out GPIO pins along the edges.

---

## Toolchain Setup

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

> **Facilitator note:** Ideally pre-installed on workshop laptops. Allow 10 min if not. Common issue: participants install the Arduino-Mbed Pico package instead of Earle Philhower — wrong one.

---

## Reading the Pinout

- GPIO = General Purpose Input/Output — each pin can be input or output
- Some pins have special functions: SPI for the display, PWM for audio
- We'll use: GP6, GP8-13, GP16-19, GP21-22

> **Facilitator note:** Hand out or display the pinout diagram.

---

## Breadboard Basics

- Holes in the same row are electrically connected
- The two rails down the sides are for power (3.3V) and ground (GND)
- **Rule of thumb:** If it doesn't work, check your wiring first.

> **Facilitator note:** Show a breadboard diagram. Demonstrate the row connection.

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

> **Facilitator note:** 20 min. Walk the room as participants wire up. Common pitfalls: buttons not seated fully, LED legs in wrong order, buzzer polarity reversed.

---

## Step 0 — Hello World

**Concept:** How Arduino sketches work — `setup()` runs once, `loop()` runs forever.

An Arduino sketch is a folder. All `.h`, `.cpp`, and `.ino` files inside it compile together — the IDE shows them as tabs. Three files are already provided: `Pet.h`, `Pet.cpp`, and `sprites.h`. These are the pet engine — you call their methods but don't need to edit them.

**Create** `tomogatchi.ino`:

```cpp
#include "Pet.h"

Pet pet;

void setup() {
    pet.begin();
}

void loop() {
    pet.update();
    delay(50);
}
```

Upload. Your pet's face appears on the display. Buttons do nothing yet.

> **Facilitator note:** 5 min. Most issues are port selection or needing BOOTSEL mode (hold BOOTSEL while plugging in).

---

## Step 1 — Teach It to Listen

**Concept:** Digital input with `pinMode` and `digitalRead`. Edge detection. Header/source file split.

**Key ideas:**
- `.h` file = declarations (tells the compiler "this function exists")
- `.cpp` file = definitions (the actual code)
- `#pragma once` = only include this file once
- `pinMode(pin, INPUT_PULLDOWN)` — configures a pin to read button presses. INPUT_PULLDOWN keeps the pin LOW until the button connects it to 3.3V
- `digitalRead(pin)` — returns HIGH (pressed) or LOW (not pressed)
- The "last state" trick — detect a fresh press, not a held button:
  ```cpp
  static bool lastRed = false;
  bool red = digitalRead(22);
  if (red && !lastRed) { /* fresh press! */ }
  lastRed = red;
  ```

**Create** `buttons.h`:

```cpp
#pragma once
#include "Pet.h"

void setupButtons();
void readButtons(Pet& pet);
```

**Create** `buttons.cpp`:

```cpp
#include <Arduino.h>
#include "buttons.h"

const int PIN_BTN_RED    = 22;
const int PIN_BTN_YELLOW = 21;
const int PIN_BTN_GREEN  = 19;

static bool lastRed = false, lastYellow = false, lastGreen = false;

void setupButtons() {
    pinMode(PIN_BTN_RED,    INPUT_PULLDOWN);
    pinMode(PIN_BTN_YELLOW, INPUT_PULLDOWN);
    pinMode(PIN_BTN_GREEN,  INPUT_PULLDOWN);
}

void readButtons(Pet& pet) {
    bool red    = digitalRead(PIN_BTN_RED);
    bool yellow = digitalRead(PIN_BTN_YELLOW);
    bool green  = digitalRead(PIN_BTN_GREEN);

    if (red && !lastRed)       pet.feed();
    if (yellow && !lastYellow) pet.drink();
    if (green && !lastGreen)   pet.say(pet.catchphrase());

    lastRed = red;
    lastYellow = yellow;
    lastGreen = green;
}
```

**Update** `tomogatchi.ino` — add the buttons include and calls:

```cpp
#include "Pet.h"
#include "buttons.h"

Pet pet;

void setup() {
    pet.begin();
    setupButtons();
}

void loop() {
    readButtons(pet);
    pet.update();
    delay(50);
}
```

**Checkpoint 1:** Press red — "Yum!", "So full!". Press yellow — "Refreshing!". Press green — mood phrase. Each button does something meaningful.

> **Facilitator note:** 20 min. Common mistake: forgetting INPUT_PULLDOWN (buttons fire randomly). `static` keyword persists between calls — explain briefly. INPUT_PULLDOWN is Pico-specific.

---

## Step 2 — Give It a Voice

**Concept:** `tone()` for sound, frequency = pitch, arrays, for-loops, composing a melody.

**Key ideas:**
- `tone(pin, freq, duration)` — generates a square wave at the given frequency
- `noTone(pin)` — stops the tone
- Frequency = pitch: 440Hz = A4, 523Hz = C5, higher number = higher pitch
- A melody is an array of {frequency, duration} pairs

**Frequency reference:**
| Note | Hz  |
|------|-----|
| C5   | 523 |
| D5   | 587 |
| E5   | 659 |
| F5   | 698 |
| G5   | 784 |
| A5   | 880 |
| B5   | 988 |

**Create** `sound.h`:

```cpp
#pragma once
#include "Pet.h"

void setupBuzzer();
void playTone(int freq, int duration);
void playMelody(const int notes[][2], int len);
void chirp(Mood m);

// Pre-made melodies
extern const int WAKE_TUNE[][2];
extern const int WAKE_TUNE_LEN;

extern const int HAPPY_TUNE[][2];
extern const int HAPPY_TUNE_LEN;

extern const int SAD_TUNE[][2];
extern const int SAD_TUNE_LEN;

extern const int VICTORY_TUNE[][2];
extern const int VICTORY_TUNE_LEN;

extern const int DEATH_TUNE[][2];
extern const int DEATH_TUNE_LEN;
```

**Create** `sound.cpp`:

```cpp
#include <Arduino.h>
#include "sound.h"

const int PIN_BUZZER = 6;

void setupBuzzer() {
    pinMode(PIN_BUZZER, OUTPUT);
}

void playTone(int freq, int duration) {
    if (freq > 0) {
        tone(PIN_BUZZER, freq, duration);
        delay(duration);
        noTone(PIN_BUZZER);
    } else {
        delay(duration);  // rest
    }
}

void playMelody(const int notes[][2], int len) {
    for (int i = 0; i < len; i++) {
        playTone(notes[i][0], notes[i][1]);
    }
}

void chirp(Mood m) {
    switch (m) {
        case Mood::HAPPY:
            playTone(880, 80);
            playTone(988, 80);
            break;
        case Mood::SAD:
            playTone(330, 200);
            playTone(262, 300);
            break;
        case Mood::DEAD:
            playTone(150, 400);
            break;
        default:
            playTone(523, 100);
            break;
    }
}

// Pre-made melodies — use these or compose your own!

const int WAKE_TUNE[][2] = {
    {523, 150}, {523, 150}, {0, 50},
    {523, 150}, {0, 50}, {415, 150},
    {523, 200}, {659, 200}, {523, 200}
};
const int WAKE_TUNE_LEN = 9;

const int HAPPY_TUNE[][2] = {
    {523, 120}, {659, 120}, {784, 120},
    {880, 200}, {784, 120}, {880, 300}
};
const int HAPPY_TUNE_LEN = 6;

const int SAD_TUNE[][2] = {
    {440, 300}, {392, 300}, {349, 400}, {330, 500}
};
const int SAD_TUNE_LEN = 4;

const int VICTORY_TUNE[][2] = {
    {523, 150}, {523, 150}, {523, 150},
    {659, 400}, {587, 150}, {523, 150},
    {587, 150}, {659, 200}, {523, 200}
};
const int VICTORY_TUNE_LEN = 9;

const int DEATH_TUNE[][2] = {
    {294, 400}, {277, 400}, {262, 400}, {247, 600}
};
const int DEATH_TUNE_LEN = 4;
```

**Update** `buttons.cpp` — add `#include "sound.h"` at the top, and add chirps after each button action:

```cpp
#include <Arduino.h>
#include "buttons.h"
#include "sound.h"

const int PIN_BTN_RED    = 22;
const int PIN_BTN_YELLOW = 21;
const int PIN_BTN_GREEN  = 19;

static bool lastRed = false, lastYellow = false, lastGreen = false;

void setupButtons() {
    pinMode(PIN_BTN_RED,    INPUT_PULLDOWN);
    pinMode(PIN_BTN_YELLOW, INPUT_PULLDOWN);
    pinMode(PIN_BTN_GREEN,  INPUT_PULLDOWN);
}

void readButtons(Pet& pet) {
    bool red    = digitalRead(PIN_BTN_RED);
    bool yellow = digitalRead(PIN_BTN_YELLOW);
    bool green  = digitalRead(PIN_BTN_GREEN);

    if (red && !lastRed) {
        pet.feed();
        chirp(pet.mood());
    }
    if (yellow && !lastYellow) {
        pet.drink();
        chirp(pet.mood());
    }
    if (green && !lastGreen) {
        pet.say(pet.catchphrase());
        chirp(pet.mood());
    }

    lastRed = red;
    lastYellow = yellow;
    lastGreen = green;
}
```

**Update** `tomogatchi.ino` — add `#include "sound.h"` and `setupBuzzer()`:

```cpp
#include "Pet.h"
#include "buttons.h"
#include "sound.h"

Pet pet;

void setup() {
    pet.begin();
    setupButtons();
    setupBuzzer();
}

void loop() {
    readButtons(pet);
    pet.update();
    delay(50);
}
```

**Checkpoint 2:** Press any button — hear a chirp that matches the pet's mood. Happy pet = bright rising chirp. Sad pet = low descending moan. Try changing frequencies in `chirp()` or composing your own melody!

> **Facilitator note:** 20 min. If buzzer is silent: check polarity. `tone()` blocks — intentional here. Encourage changing note values.

---

## Step 3 — Light It Up

**Concept:** `digitalWrite()` for output, RGB colour mixing, reading provided code.

**Key ideas:**
- `digitalWrite(pin, HIGH)` / `digitalWrite(pin, LOW)` — turn an output on or off
- RGB LED has 3 channels — mixing them makes colours:
  - (1,0,0) = red, (0,1,0) = green, (1,1,0) = yellow, (1,0,1) = magenta

**Create** `leds.h`:

```cpp
#pragma once

void setupLeds();
void setLed(int r, int g, int b);
bool playSimon();
```

**Create** `leds.cpp` — write `setupLeds` and `setLed` yourself:

```cpp
#include <Arduino.h>
#include "leds.h"
#include "sound.h"

const int PIN_LED_R = 16;
const int PIN_LED_G = 17;
const int PIN_LED_B = 18;

void setupLeds() {
    pinMode(PIN_LED_R, OUTPUT);
    pinMode(PIN_LED_G, OUTPUT);
    pinMode(PIN_LED_B, OUTPUT);
}

void setLed(int r, int g, int b) {
    digitalWrite(PIN_LED_R, r);
    digitalWrite(PIN_LED_G, g);
    digitalWrite(PIN_LED_B, b);
}
```

The Simon Says game is provided below. Copy it into `leds.cpp` after your `setLed` function. Read through it — it uses YOUR `setLed()` and `playTone()` to run a real game.

```cpp
bool playSimon() {
    const int SEQ_LEN = 3;

    int colours[3][3] = {
        {1, 0, 0},   // red
        {0, 1, 0},   // green
        {1, 1, 0},   // yellow
    };
    int buttons[3] = {22, 19, 21};    // red, green, yellow
    int tones[3]   = {440, 523, 659}; // A4, C5, E5

    int seq[SEQ_LEN];
    for (int i = 0; i < SEQ_LEN; i++) seq[i] = random(3);

    delay(500);
    for (int i = 0; i < SEQ_LEN; i++) {
        int c = seq[i];
        setLed(colours[c][0], colours[c][1], colours[c][2]);
        playTone(tones[c], 400);
        setLed(0, 0, 0);
        delay(200);
    }
    delay(300);

    for (int i = 0; i < SEQ_LEN; i++) {
        unsigned long start = millis();
        bool waiting = true;
        while (waiting && millis() - start < 5000) {
            for (int b = 0; b < 3; b++) {
                if (digitalRead(buttons[b])) {
                    setLed(colours[b][0], colours[b][1], colours[b][2]);
                    playTone(tones[b], 200);
                    setLed(0, 0, 0);
                    delay(100);
                    if (b != seq[i]) return false;
                    waiting = false;
                    break;
                }
            }
            delay(10);
        }
        if (waiting) return false;
    }

    for (int i = 0; i < 3; i++) {
        setLed(1, 1, 1);
        delay(100);
        setLed(0, 0, 0);
        delay(100);
    }
    return true;
}
```

**Update** `buttons.cpp` — add `#include "leds.h"` at the top. Replace the yellow button action and add mood LED glow:

```cpp
#include <Arduino.h>
#include "buttons.h"
#include "sound.h"
#include "leds.h"

const int PIN_BTN_RED    = 22;
const int PIN_BTN_YELLOW = 21;
const int PIN_BTN_GREEN  = 19;

static bool lastRed = false, lastYellow = false, lastGreen = false;

void setupButtons() {
    pinMode(PIN_BTN_RED,    INPUT_PULLDOWN);
    pinMode(PIN_BTN_YELLOW, INPUT_PULLDOWN);
    pinMode(PIN_BTN_GREEN,  INPUT_PULLDOWN);
}

void readButtons(Pet& pet) {
    bool red    = digitalRead(PIN_BTN_RED);
    bool yellow = digitalRead(PIN_BTN_YELLOW);
    bool green  = digitalRead(PIN_BTN_GREEN);

    if (red && !lastRed) {
        pet.feed();
        chirp(pet.mood());
    }

    if (yellow && !lastYellow) {
        bool won = playSimon();
        if (won) {
            pet.feed();
            playMelody(VICTORY_TUNE, VICTORY_TUNE_LEN);
        } else {
            pet.say("Nope...");
            playTone(200, 300);
        }
    }

    if (green && !lastGreen) {
        pet.say(pet.catchphrase());
        chirp(pet.mood());
    }

    // Mood LED glow after any press
    if ((red && !lastRed) || (yellow && !lastYellow) || (green && !lastGreen)) {
        switch (pet.mood()) {
            case Mood::HAPPY: setLed(0, 1, 0); break;
            case Mood::SAD:   setLed(1, 0, 0); break;
            case Mood::DEAD:  setLed(0, 0, 0); break;
            default:          setLed(1, 1, 0); break;
        }
    }

    lastRed = red;
    lastYellow = yellow;
    lastGreen = green;
}
```

**Update** `tomogatchi.ino` — add `#include "leds.h"` and `setupLeds()`:

```cpp
#include "Pet.h"
#include "buttons.h"
#include "sound.h"
#include "leds.h"

Pet pet;

void setup() {
    pet.begin();
    setupButtons();
    setupBuzzer();
    setupLeds();
}

void loop() {
    readButtons(pet);
    pet.update();
    delay(50);
}
```

**Checkpoint 3:** LED glows mood colour on every interaction. Yellow triggers Simon Says — LED flashes a colour sequence with tones, you press matching buttons. Win = pet fed + victory fanfare + white flash. Lose = sad buzz. Common issue: wrong colours means wrong pin wiring (GP16=R, GP17=G, GP18=B).

> **Facilitator note:** 20 min. RGB mixing is fun — encourage experimenting. The payoff: their `setLed()` and `playTone()` drive a real game.

---

## Step 4 — It Needs You

**Concept:** `millis()` for non-blocking timing, counters, assembling the full system.

**Key ideas:**
- `millis()` returns milliseconds since the Pico started
- Unlike `delay()`, it doesn't stop the program — you can check elapsed time while doing other things
- Pattern:
  ```cpp
  unsigned long start = millis();
  while (millis() - start < 3000) {
      // runs for 3 seconds
  }
  ```

**Create** `game.h`:

```cpp
#pragma once

int buttonMash(int pin, int durationMs);
```

**Create** `game.cpp`:

```cpp
#include <Arduino.h>
#include "game.h"

int buttonMash(int pin, int durationMs) {
    int presses = 0;
    bool lastBtn = digitalRead(pin);
    unsigned long start = millis();

    while (millis() - start < (unsigned long)durationMs) {
        bool btn = digitalRead(pin);
        if (btn && !lastBtn) presses++;
        lastBtn = btn;
        delay(10);
    }
    return presses;
}
```

Now the big moment — **update** `tomogatchi.ino` to wire everything together:

```cpp
#include "Pet.h"
#include "buttons.h"
#include "sound.h"
#include "leds.h"
#include "game.h"

Pet pet;

void setup() {
    pet.begin();
    setupButtons();
    setupBuzzer();
    setupLeds();
    pet.enableDecay();
}

void loop() {
    static bool lastGreen = false;
    bool green = digitalRead(19);

    if (green && !lastGreen) {
        pet.say("MASH IT!");
        int presses = buttonMash(19, 3000);
        pet.exercise(presses);
    }

    lastGreen = green;
    readButtons(pet);
    pet.update();
    delay(50);
}
```

Key change: `pet.enableDecay()` in setup makes the pet mortal. Stats now decay over time. The green button now triggers a 3-second mash window instead of just a catchphrase.

**Checkpoint 4:** Full tamagotchi running! Leave it alone 30 seconds — watch it get sad, start begging ("Don't forget me!"), LED flashes red. Mash green — "MASH IT!" appears, mash as fast as you can, energy goes up. Feed and water it to keep it alive.

> **Facilitator note:** 15 min. When `enableDecay()` runs, the game goes live — stats fall, pet gets sad, alerts fire. Leave it alone to demo. Then show recovery.

---

## Step 5 — Make It Yours

Ideas to try during free time:

**Tune your pet** — change config values in `tomogatchi.ino`:
```cpp
PetConfig config;
config.decayRate = 3;        // faster decay
config.decayInterval = 5000; // twice as fast
config.feedAmount = 10;      // less food per press
pet.begin(config);
```

**Compose a melody** — change the notes in `sound.cpp` or write new ones using the frequency table.

**Custom sprite** — draw at piskelapp.com, export PNG, convert:
```
python tools/convert.py face.png --header -o tomogatchi/mysprite.h
```

**Extend Simon** — change `SEQ_LEN` from 3 to 5 in `leds.cpp`.

**Secret combo** — all three buttons at once = full heal.

> **Facilitator note:** 20 min free time.

---

## Wrap Up

**What you built:** A complete interactive embedded device with display, buttons, LED, and buzzer.

**What you learned:**
- `pinMode`, `digitalRead`, `digitalWrite` — GPIO basics
- `tone()` — PWM audio and frequency
- RGB colour mixing
- `millis()` — non-blocking timing
- Header/source file split
- How hardware and software work together

Take it home. Keep your pet alive.

---

## Facilitator Quick Reference

| Problem | Cause | Fix |
|---------|-------|-----|
| Buttons fire randomly | Missing INPUT_PULLDOWN | Add to pinMode |
| Button never responds | Bad wiring | Check jumper wire |
| Buzzer silent | Reversed polarity | Swap + and - |
| Wrong LED colour | Wrong pin | GP16=R, GP17=G, GP18=B |
| Upload fails | Wrong port/board | Check Tools menu |
| No port showing | Pico not connected | Hold BOOTSEL, plug in |
| Wrong board | Arduino-Mbed package | Use Earle Philhower package |
