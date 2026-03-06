# Workshop v3 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rewrite all workshop files to match the v3 design — clean final code (no stubs/fallbacks), mood-reactive audio/visual feedback, pre-made melodies, PetConfig, and a ground-up workshop guide.

**Architecture:** The repo contains the finished working project. Pet.h/Pet.cpp is the smart engine with weak extern stubs so it compiles at every workshop step. Participant files (buttons, sound, leds, game, ino) are clean final code that the workshop guide teaches how to build from scratch.

**Tech Stack:** Arduino C++, arduino-pico board package, Adafruit ST7789 + GFX.

**Design doc:** `docs/plans/2026-02-27-workshop-v3-design.md`

---

## Task 1 — Rewrite Pet.h

**Files:**
- Modify: `tomogatchi/Pet.h`

**Steps:**

1. Add `PetConfig` struct before the `Pet` class:

```cpp
struct PetConfig {
    int decayRate      = 1;
    int decayInterval  = 10000;
    int feedAmount     = 20;
    int drinkAmount    = 20;
    int exerciseCap    = 30;
    int alertThreshold = 30;
};
```

2. Add `begin(PetConfig cfg)` overload to the public section.

3. Add `_drawText(String msg)` to the private section (currently missing from header but used in Pet.cpp).

4. Add `PetConfig _cfg` to the private member variables.

5. Keep the rest of Pet.h the same — all existing public API stays.

6. Commit: `feat: add PetConfig struct and begin() overload to Pet.h`

---

## Task 2 — Rewrite Pet.cpp

**Files:**
- Modify: `tomogatchi/Pet.cpp`

**Changes from current Pet.cpp:**

1. **Replace static constants with config-derived values.** Keep current static constants as the defaults, but use `_cfg` members where applicable:
   - `DECAY_RATE` → `_cfg.decayRate`
   - `DECAY_INTERVAL` → `_cfg.decayInterval`
   - `FEED_AMOUNT` → `_cfg.feedAmount` / `_cfg.drinkAmount`
   - `EXERCISE_MAX_BOOST` → `_cfg.exerciseCap`
   - `ALERT_THRESHOLD` → `_cfg.alertThreshold`

   Keep the non-configurable constants as static const (pin numbers, sprite dimensions, display layout, backlight timeout, msg duration, alert cooldown).

2. **Add weak extern stubs** at the top, replacing the current `extern` declarations:

```cpp
__attribute__((weak)) void playTone(int freq, int duration) { (void)freq; (void)duration; }
__attribute__((weak)) void setLed(int r, int g, int b) { (void)r; (void)g; (void)b; }
```

3. **Two begin() methods:**

```cpp
void Pet::begin() {
    PetConfig defaults;
    begin(defaults);
}

void Pet::begin(PetConfig cfg) {
    _cfg = cfg;
    // ... existing begin() body (pinMode, lcd init, etc.)
}
```

4. **Mood-specific messages in feed():**

```cpp
void Pet::feed() {
    food = min(STAT_MAX, food + _cfg.feedAmount);
    _lastActivity = millis();
    if (!_backlightOn) { digitalWrite(PIN_BL, HIGH); _backlightOn = true; }

    // Mood-specific response
    switch (_computeMood()) {
        case Mood::HAPPY: {
            const char* p[] = {"Yum!", "So full!", "Mmm!", "Delicious!"};
            _showMessage(p[random(4)]);
            break;
        }
        case Mood::SAD: {
            const char* p[] = {"Finally...", "Needed that", "More please..."};
            _showMessage(p[random(3)]);
            break;
        }
        case Mood::DEAD: {
            _showMessage("*munch*");
            break;
        }
        default: {
            const char* p[] = {"Thanks!", "Nom!", "Tasty!"};
            _showMessage(p[random(3)]);
            break;
        }
    }
    _redraw();
}
```

5. **Mood-specific messages in drink():**

```cpp
void Pet::drink() {
    water = min(STAT_MAX, water + _cfg.drinkAmount);
    _lastActivity = millis();
    if (!_backlightOn) { digitalWrite(PIN_BL, HIGH); _backlightOn = true; }

    switch (_computeMood()) {
        case Mood::HAPPY: {
            const char* p[] = {"Ahhh!", "Refreshing!", "Glug glug!", "Hydrated!"};
            _showMessage(p[random(4)]);
            break;
        }
        case Mood::SAD: {
            const char* p[] = {"So thirsty...", "Needed that...", "*sip*"};
            _showMessage(p[random(3)]);
            break;
        }
        case Mood::DEAD: {
            _showMessage("*slurp*");
            break;
        }
        default: {
            const char* p[] = {"Thanks!", "Glug!", "Nice!"};
            _showMessage(p[random(3)]);
            break;
        }
    }
    _redraw();
}
```

6. **Use `_cfg.exerciseCap` in exercise():**

```cpp
void Pet::exercise(int boost) {
    energy = min(STAT_MAX, energy + constrain(boost, 0, _cfg.exerciseCap));
    // ... rest stays the same
}
```

7. **Use `_cfg.alertThreshold` in needsAlert():**

```cpp
bool Pet::needsAlert() {
    return (food < _cfg.alertThreshold ||
            water < _cfg.alertThreshold ||
            energy < _cfg.alertThreshold);
}
```

8. **Use `_cfg.decayInterval` in update():**

```cpp
if (_decayEnabled && (now - _lastDecay >= (unsigned long)_cfg.decayInterval)) {
```

9. **Use `_cfg.decayRate` in _decayAll():**

```cpp
void Pet::_decayAll() {
    food   = max(STAT_MIN, food   - _cfg.decayRate);
    water  = max(STAT_MIN, water  - _cfg.decayRate);
    energy = max(STAT_MIN, energy - _cfg.decayRate);
}
```

10. Commit: `feat: rewrite Pet.cpp with PetConfig, mood messages, weak externs`

---

## Task 3 — Rewrite buttons.h and buttons.cpp

**Files:**
- Rewrite: `tomogatchi/buttons.h`
- Rewrite: `tomogatchi/buttons.cpp`

These are the **final working versions** — what the project looks like after a participant completes all steps. No stubs, no fallbacks, no TODO comments.

**buttons.h:**

```cpp
#pragma once
#include "Pet.h"

void setupButtons();
void readButtons(Pet& pet);
```

**buttons.cpp:**

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

    // Red — feed
    if (red && !lastRed) {
        pet.feed();
        chirp(pet.mood());
    }

    // Yellow — Simon Says
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

    // Green — talk / catchphrase
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

Note: This is the **final** version with all steps applied (sound, Simon, mood LED). The workshop guide teaches building this incrementally — Step 1 starts with just `pet.feed()`/`pet.drink()`/`pet.say()`, then Steps 2-3 layer on chirp/Simon/LED.

Commit: `feat: rewrite buttons.h/cpp as clean final code`

---

## Task 4 — Rewrite sound.h and sound.cpp

**Files:**
- Rewrite: `tomogatchi/sound.h`
- Rewrite: `tomogatchi/sound.cpp`

**sound.h:**

```cpp
#pragma once
#include "Pet.h"

void setupBuzzer();
void playTone(int freq, int duration);
void playMelody(const int notes[][2], int len);
void chirp(Mood m);

// --- Pre-made melodies (use these or compose your own!) ---

// Cheerful startup jingle
extern const int WAKE_TUNE[][2];
extern const int WAKE_TUNE_LEN;

// Rising major-key joy
extern const int HAPPY_TUNE[][2];
extern const int HAPPY_TUNE_LEN;

// Descending minor-key sadness
extern const int SAD_TUNE[][2];
extern const int SAD_TUNE_LEN;

// Triumphant fanfare — play after winning Simon Says
extern const int VICTORY_TUNE[][2];
extern const int VICTORY_TUNE_LEN;

// Dramatic game over
extern const int DEATH_TUNE[][2];
extern const int DEATH_TUNE_LEN;
```

**sound.cpp:**

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

// --- Pre-made melodies ------------------------------------------------

// Cheerful startup jingle (do-do-rest-do-rest-ti-do-mi-do)
const int WAKE_TUNE[][2] = {
    {523, 150}, {523, 150}, {0, 50},
    {523, 150}, {0, 50}, {415, 150},
    {523, 200}, {659, 200}, {523, 200}
};
const int WAKE_TUNE_LEN = 9;

// Rising major-key joy (C-E-G-A-G-A)
const int HAPPY_TUNE[][2] = {
    {523, 120}, {659, 120}, {784, 120},
    {880, 200}, {784, 120}, {880, 300}
};
const int HAPPY_TUNE_LEN = 6;

// Descending minor sadness (A-G-F-E held)
const int SAD_TUNE[][2] = {
    {440, 300}, {392, 300}, {349, 400}, {330, 500}
};
const int SAD_TUNE_LEN = 4;

// Triumphant fanfare (C-C-C-E-D-C-D-E-C)
const int VICTORY_TUNE[][2] = {
    {523, 150}, {523, 150}, {523, 150},
    {659, 400}, {587, 150}, {523, 150},
    {587, 150}, {659, 200}, {523, 200}
};
const int VICTORY_TUNE_LEN = 9;

// Dramatic game over (D4-C#4-C4-B3 slow)
const int DEATH_TUNE[][2] = {
    {294, 400}, {277, 400}, {262, 400}, {247, 600}
};
const int DEATH_TUNE_LEN = 4;
```

Commit: `feat: rewrite sound.h/cpp with melodies and mood chirps`

---

## Task 5 — Rewrite leds.h and leds.cpp

**Files:**
- Rewrite: `tomogatchi/leds.h`
- Rewrite: `tomogatchi/leds.cpp`

**leds.h:**

```cpp
#pragma once

void setupLeds();
void setLed(int r, int g, int b);
bool playSimon();
```

**leds.cpp:**

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

// --- Simon Says (provided — uses setLed and playTone) -----------------

bool playSimon() {
    const int SEQ_LEN = 3;

    int colours[3][3] = {
        {1, 0, 0},   // red
        {0, 1, 0},   // green
        {1, 1, 0},   // yellow
    };
    int buttons[3] = {22, 19, 21};       // red, green, yellow
    int tones[3]   = {440, 523, 659};    // A4, C5, E5

    int seq[SEQ_LEN];
    for (int i = 0; i < SEQ_LEN; i++) seq[i] = random(3);

    // Flash the sequence
    delay(500);
    for (int i = 0; i < SEQ_LEN; i++) {
        int c = seq[i];
        setLed(colours[c][0], colours[c][1], colours[c][2]);
        playTone(tones[c], 400);
        setLed(0, 0, 0);
        delay(200);
    }
    delay(300);

    // Read player input
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

    // Victory flash
    for (int i = 0; i < 3; i++) {
        setLed(1, 1, 1);
        delay(100);
        setLed(0, 0, 0);
        delay(100);
    }
    return true;
}
```

Commit: `feat: rewrite leds.h/cpp as clean final code`

---

## Task 6 — Rewrite game.h and game.cpp

**Files:**
- Rewrite: `tomogatchi/game.h`
- Rewrite: `tomogatchi/game.cpp`

**game.h:**

```cpp
#pragma once

int buttonMash(int pin, int durationMs);
```

**game.cpp:**

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

Commit: `feat: rewrite game.h/cpp as clean final code`

---

## Task 7 — Rewrite tomogatchi.ino

**Files:**
- Rewrite: `tomogatchi/tomogatchi.ino`

This is the **final working version** — what the sketch looks like when all steps are complete, including the Step 5 (Playground) PetConfig.

```cpp
#include "Pet.h"
#include "buttons.h"
#include "sound.h"
#include "leds.h"
#include "game.h"

Pet pet;

// === PET SETTINGS — tweak these! ===
PetConfig config;

void setup() {
    // Customise your pet (change these values!)
    // config.decayRate      = 1;      // how much stats drop each tick
    // config.decayInterval  = 10000;  // ms between decay ticks (lower = harder)
    // config.feedAmount     = 20;     // how much food one press gives
    // config.drinkAmount    = 20;     // how much water one press gives
    // config.exerciseCap    = 30;     // max energy from one mash session
    // config.alertThreshold = 30;     // stat level that triggers alerts

    pet.begin(config);
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

Commit: `feat: rewrite tomogatchi.ino as clean final code with PetConfig`

---

## Task 8 — Rewrite workshop guide

**Files:**
- Rewrite: `docs/workshop-guide.md`

The guide walks through building the project from scratch. Each heading is a slide. The guide shows what participants type — it references the final code but presents it incrementally.

**Structure:**

```
# Tomogatchi Workshop Guide

## Welcome
## Why C++?
## What Is a Raspberry Pi Pico?
## Toolchain Setup
## Reading the Pinout
## Breadboard Basics
## Wiring the Circuit

## Step 0 — Hello World
  - Create tomogatchi.ino (6 lines)
  - Upload, see pet face
  - Concept: setup() and loop()

## Step 1 — Teach It to Listen
  - Create buttons.h (declare setupButtons, readButtons)
  - Create buttons.cpp (implement with edge detection)
  - Red = pet.feed(), Yellow = pet.drink(), Green = pet.say(catchphrase)
  - Wire into .ino: setupButtons() in setup, readButtons(pet) in loop
  - Checkpoint: buttons make pet respond with mood messages
  - Concept: digitalRead, pinMode, INPUT_PULLDOWN, debounce, headers

## Step 2 — Give It a Voice
  - Create sound.h (declare setupBuzzer, playTone, playMelody, chirp)
  - Create sound.cpp (implement + pre-made melodies + chirp function)
  - Participants compose own melody OR use provided ones
  - Add chirp(pet.mood()) to button presses in buttons.cpp
  - Wire green to play WAKE_TUNE
  - Wire setupBuzzer() into .ino setup
  - Checkpoint: every press has mood-appropriate sound
  - Concept: tone(), frequency, arrays, for-loops

## Step 3 — Light It Up
  - Create leds.h (declare setupLeds, setLed, playSimon)
  - Create leds.cpp (implement setupLeds + setLed, Simon is provided)
  - Add mood LED glow to readButtons in buttons.cpp
  - Replace yellow button with Simon Says + victory/fail feedback
  - Wire setupLeds() into .ino setup
  - Checkpoint: mood colours + Simon Says game works
  - Concept: digitalWrite, RGB mixing, reading complex code

## Step 4 — It Needs You
  - Create game.h (declare buttonMash)
  - Create game.cpp (implement with millis timer)
  - Replace loop() in .ino with mash-aware version
  - Add pet.enableDecay() to setup — pet becomes mortal
  - Checkpoint: full tamagotchi with decay, alerts, mashing
  - Concept: millis(), non-blocking timers, full system assembly

## Step 5 — Make It Yours (Playground)
  - Introduce PetConfig: tweak decay, feed amounts, thresholds
  - Custom sprites: piskelapp.com + convert.py
  - Compose new melodies
  - Extend Simon sequence length
  - Secret button combos

## Wrap Up
## Facilitator Quick Reference (troubleshooting table)
```

The guide should:
- Show exact code to type at each step (copied from the final files, presented incrementally)
- Explain each concept briefly before the code
- Include facilitator notes for timing, common mistakes, and teaching tips
- Show the intermediate state of buttons.cpp at each step (Step 1 version, then Step 2 additions, then Step 3 additions)
- Include frequency reference table for melodies
- Reference the provided melodies by name

Commit: `docs: rewrite workshop guide for v3 ground-up build`

---

## Task 9 — Verify include chain and compilation

**Steps:**

1. Verify all `#include` chains resolve:
   - `tomogatchi.ino` includes Pet.h, buttons.h, sound.h, leds.h, game.h
   - `buttons.cpp` includes Arduino.h, buttons.h, sound.h, leds.h
   - `sound.cpp` includes Arduino.h, sound.h
   - `leds.cpp` includes Arduino.h, leds.h, sound.h
   - `game.cpp` includes Arduino.h, game.h
   - `Pet.cpp` includes Pet.h, sprites.h

2. Verify weak externs in Pet.cpp:
   - `playTone` and `setLed` are declared weak
   - When sound.cpp and leds.cpp are present, their strong definitions override

3. Verify the sketch compiles at each workshop step:
   - Step 0: only .ino + Pet.h/Pet.cpp/sprites.h → compiles (weak stubs cover missing functions)
   - Step 1: + buttons.h/buttons.cpp → compiles
   - Step 2: + sound.h/sound.cpp → compiles (playTone overrides weak)
   - Step 3: + leds.h/leds.cpp → compiles (setLed overrides weak)
   - Step 4: + game.h/game.cpp → compiles (full sketch)

4. Check that `playSimon()` correctly references button pins (22, 19, 21) matching the pin map.

5. Check melody array lengths match their `_LEN` constants.

6. Commit: `chore: verify v3 sketch compiles at all steps`

---

## Order of Execution

Tasks 1-2 (Pet engine) must come first — everything depends on Pet.h/Pet.cpp.

Tasks 3-7 (participant files + ino) can run in parallel after Tasks 1-2.

Task 8 (guide) can run in parallel with Tasks 3-7 but benefits from having final code to reference.

Task 9 (verification) must run last.

**Recommended order:** 1 → 2 → 3,4,5,6,7 (parallel) → 8 → 9
