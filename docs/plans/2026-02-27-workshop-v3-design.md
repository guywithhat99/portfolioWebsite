# Tomogatchi Workshop v3 — Design

**Date:** 2026-02-27
**Status:** Draft
**Supersedes:** `2026-02-26-workshop-v2-arduino-design.md`

---

## Vision

The workshop builds a tamagotchi from scratch, step by step. Each step
teaches one embedded concept and ends with an immediate, delightful
payoff on the device. The pet feels emotionally responsive — it chirps
happily when happy, moans when sad, flashes colours, plays real melodies,
and guilt-trips you when neglected.

**Audience:** People with some coding experience (Python, JS, etc.) but
new to C++ and hardware.

**Approach:**
- Participants start with only the engine files (Pet.h, Pet.cpp, sprites.h)
- They create every other file from scratch, typing real code
- The workshop guide walks through each step chronologically
- The repo contains the finished working project (the "answer key")
- Complex engine/display code is smart and encapsulated; participant code is simple

---

## Narrative Arc

| Step | The pet goes from... | ...to |
|------|---------------------|-------|
| 0 | Nothing | A face staring at you silently |
| 1 | Silent | Reacts when you press buttons — phrases, feeding, watering |
| 2 | Mute | Has a voice — mood chirps, melodies, jingles |
| 3 | Dark | Glows mood colours, plays Simon Says with light and sound |
| 4 | Immortal | Mortal — stats decay, alerts fire, the full tamagotchi |

The escalation: still image → responsive → musical → luminous → alive and needy.

---

## Project Structure (final state)

```
tomogatchi/
  tomogatchi.ino      <- main sketch, setup/loop, game wiring     [PARTICIPANT]
  buttons.h           <- button declarations                       [PARTICIPANT]
  buttons.cpp         <- button input + edge detection             [PARTICIPANT]
  sound.h             <- audio declarations + melody data          [PARTICIPANT]
  sound.cpp           <- buzzer control + chirp + melodies         [PARTICIPANT]
  leds.h              <- LED declarations                          [PARTICIPANT]
  leds.cpp            <- RGB LED + Simon Says (provided)           [PARTICIPANT + PROVIDED]
  game.h              <- mash game declaration                     [PARTICIPANT]
  game.cpp            <- button mash with millis()                 [PARTICIPANT]
  Pet.h               <- Pet class header                          [PROVIDED read-only]
  Pet.cpp             <- Pet engine implementation                 [PROVIDED read-only]
  sprites.h           <- PROGMEM sprite data                       [PROVIDED read-only]
```

**Starting point for participants:** Only Pet.h, Pet.cpp, and sprites.h
exist. Everything else is created during the workshop.

---

## Pin Map

| Component     | Signal | GPIO |
|---------------|--------|------|
| Display       | SCK    | GP10 |
| Display       | MOSI   | GP11 |
| Display       | DC     | GP8  |
| Display       | CS     | GP9  |
| Display       | RST    | GP12 |
| Display       | BL     | GP13 |
| RGB LED       | Red    | GP16 |
| RGB LED       | Green  | GP17 |
| RGB LED       | Blue   | GP18 |
| Buzzer        | +      | GP6  |
| Button Red    |        | GP22 |
| Button Yellow |        | GP21 |
| Button Green  |        | GP19 |

---

## Step 0 — "Hello World"

**Create:** `tomogatchi.ino`

**Concept:** How an Arduino sketch works — `setup()` runs once, `loop()`
runs forever.

**What they type:**
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

**Checkpoint:** Upload. Pet face appears on screen. Staring. Silent.
Nothing else happens. That's correct.

---

## Step 1 — "Teach it to listen"

**Create:** `buttons.h`, `buttons.cpp`. Wire into `tomogatchi.ino`.

**Concept:** `pinMode(pin, INPUT_PULLDOWN)`, `digitalRead()`, edge
detection ("last state" trick), header/source file split, pass-by-reference.

**buttons.h declares:**
```cpp
void setupButtons();
void readButtons(Pet& pet);
```

**buttons.cpp implements:**
- `setupButtons()` — configure GP22, GP21, GP19 as `INPUT_PULLDOWN`
- `readButtons(Pet& pet)` — detect fresh presses using static last-state variables:
  - Red button → `pet.feed()` (pet says something like "Yum!" automatically)
  - Yellow button → `pet.drink()` (pet says "Refreshing!" etc.)
  - Green button → `pet.say(pet.catchphrase())` (mood-dependent phrase)

**Wire into .ino:**
- `setupButtons()` in `setup()`
- `readButtons(pet)` in `loop()`

**Checkpoint:** Press red — pet says "Yum!" or "So full!". Press yellow —
"Ahhh!" or "Refreshing!". Press green — mood phrase. Each button
immediately feels like interacting with a creature.

**Key design:** Each button does something *meaningful* from the start.
Feeding and watering actually change stats. The pet reacts with
mood-appropriate messages (handled inside Pet.cpp).

---

## Step 2 — "Give it a voice"

**Create:** `sound.h`, `sound.cpp`. Wire into buttons.

**Concept:** `tone()`, `noTone()`, frequency = pitch, 2D arrays,
for-loops, composing melodies.

**sound.h declares:**
```cpp
void setupBuzzer();
void playTone(int freq, int duration);
void playMelody(const int notes[][2], int len);
```

**sound.cpp implements:**
- `setupBuzzer()` — `pinMode(6, OUTPUT)`
- `playTone(freq, duration)` — `tone()` + `delay()` + `noTone()`
- `playMelody(notes, len)` — loop calling `playTone` for each note

**Pre-made melodies** (provided as constants in sound.h/cpp):
```cpp
// Participants can use these or compose their own
const int HAPPY_TUNE[][2] = {
    {523,120},{659,120},{784,120},{880,200},  // C-E-G-A rising joy
    {784,120},{880,300}                        // G-A resolve
};

const int SAD_TUNE[][2] = {
    {440,300},{392,300},{349,400},             // A-G-F descending
    {330,500}                                  // E long hold
};

const int WAKE_TUNE[][2] = {                  // Cheerful startup
    {523,150},{523,150},{0,50},
    {523,150},{0,50},{415,150},{523,200},
    {659,200},{523,200}
};

const int VICTORY_TUNE[][2] = {               // Triumphant fanfare
    {523,150},{523,150},{523,150},
    {659,400},{587,150},{523,150},
    {587,150},{659,200},{523,200}
};

const int DEATH_TUNE[][2] = {                 // Dramatic game over
    {294,400},{277,400},{262,400},
    {247,600}
};
```

**Mood chirp function** (participants write this):
```cpp
void chirp(Mood m) {
    switch(m) {
        case Mood::HAPPY: playTone(880,80); playTone(988,80); break;
        case Mood::SAD:   playTone(330,200); playTone(262,300); break;
        case Mood::DEAD:  playTone(150,400); break;
        default:          playTone(523,100); break;
    }
}
```

**Wire into buttons:**
- Add `chirp(pet.mood())` to each button press in `readButtons()`
- Wire green button to play `WAKE_TUNE` via `playMelody()`
- Add `setupBuzzer()` to `.ino` setup

**Checkpoint:** Every button press now has sound that matches the pet's
mood. Happy pet = bright rising chirp. Sad pet = low descending moan.
Green button plays a jingle. The pet has a voice and it expresses emotion.

---

## Step 3 — "Light it up"

**Create:** `leds.h`, `leds.cpp`. Wire Simon Says to yellow button.

**Concept:** `digitalWrite()` for output, RGB colour mixing, reading
and using provided code.

**leds.h declares:**
```cpp
void setupLeds();
void setLed(int r, int g, int b);
bool playSimon();   // provided — uses setLed() and playTone()
```

**leds.cpp — participants write:**
- `setupLeds()` — three `pinMode(pin, OUTPUT)` calls
- `setLed(r, g, b)` — three `digitalWrite()` calls

**leds.cpp — provided (read, don't write):**
- `playSimon()` — the full Simon Says game. Uses the participant's
  `setLed()` and `playTone()`. This is the payoff: their code drives
  a real game.

**Mood LED glow** — participants add to `readButtons()`:
```cpp
// After handling button, show mood colour
switch(pet.mood()) {
    case Mood::HAPPY: setLed(0,1,0); break;  // green
    case Mood::SAD:   setLed(1,0,0); break;  // red
    case Mood::DEAD:  setLed(0,0,0); break;  // off
    default:          setLed(1,1,0); break;  // yellow
}
```

**Wire Simon to yellow:**
- Replace `pet.drink()` on yellow with:
  ```cpp
  bool won = playSimon();
  if (won) {
      pet.feed();
      playMelody(VICTORY_TUNE, VICTORY_TUNE_LEN);
  } else {
      pet.say("Nope...");
      playTone(200, 300);
  }
  ```

**Wire into .ino:** Add `setupLeds()` to `setup()`.

**Checkpoint:** LED glows the pet's mood colour on every interaction.
Yellow button triggers Simon Says — LED flashes colours with tones,
you match the sequence. Win = pet fed + victory fanfare + green flash.
Lose = sad buzz + red flash. Full sensory game.

---

## Step 4 — "It needs you"

**Create:** `game.h`, `game.cpp`. Update `loop()` in `.ino`.
Call `pet.enableDecay()`.

**Concept:** `millis()`, non-blocking timers, counters, assembling
a complete system.

**game.h declares:**
```cpp
int buttonMash(int pin, int durationMs);
```

**game.cpp implements:**
- `buttonMash(pin, durationMs)` — count presses in a time window
  using `millis()` and edge detection

**Wire into .ino:**
- Green button opens a 3-second mash window
- Count passed to `pet.exercise(presses)`
- Call `pet.enableDecay()` in `setup()` — **the moment of truth**

**The experience of decay:**
The instant `enableDecay()` runs, the pet becomes mortal:
- Stats drop every 10 seconds
- Pet's face changes as mood shifts
- LED shifts from green to yellow to red
- Below threshold: pet calls out — "Hey...", "Don't forget me!" —
  with alert tones and red LED flashes
- At zero: death face, death melody, LED off
- Press buttons frantically → pet recovers, happy chirp, green glow

**Checkpoint:** Full tamagotchi running. Leave it alone — watch it
get sad, start begging, eventually die. Mash buttons — bring it back.
Every interaction has sound, light, and personality.

---

## Step 5 (Playground) — "Make it yours"

**Concept:** Configuration, experimentation, ownership.

**PetConfig struct** — introduced here, not before:
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

**pet.begin() overload:**
```cpp
pet.begin();              // defaults (used in steps 0-4)
pet.begin(config);        // custom (playground)
```

Participants define their config in `.ino`:
```cpp
PetConfig config;
config.decayRate = 3;        // aggressive decay
config.decayInterval = 5000; // twice as fast
config.feedAmount = 10;      // less food per press
pet.begin(config);
```

**Other playground ideas:**
- Compose new melodies — swap WAKE_TUNE for their own composition
- Draw a custom sprite at piskelapp.com, convert with `tools/convert.py`
- Extend Simon to 5-step sequences
- Add a secret button combo (all three buttons = full heal + special melody)
- Add mood-specific melodies (sad melody when sad, happy when happy)
- Increase mash duration or change which button triggers it

---

## Pet Engine Design (Pet.h / Pet.cpp)

The engine is the "smart" code. Participants never edit it but can
read it. It should be clean, well-commented, and handle all the
complex display/timing/state logic.

### Key behaviours:

**Mood-specific messages:**
- `feed()` shows: "Yum!", "So full!", "Mmm!" (happy) / "Finally...", "Needed that" (sad)
- `drink()` shows: "Ahhh!", "Refreshing!", "Glug!" (happy) / "So thirsty..." (sad)
- `exercise()` shows: "Nice work!", "Pumped!", "Energy!"
- `catchphrase()` returns mood-appropriate phrases for general interaction

**Alert system:**
- When any stat < alert threshold, fires every 15 seconds:
  - Shows alert message ("Hey...", "Don't forget me!", "Hellooo?")
  - Plays alert tone via `playTone()` (extern from sound.cpp)
  - Flashes LED red via `setLed()` (extern from leds.cpp)
- Alert messages get more desperate as stats drop lower

**Display management:**
- Sprite redraws on mood change (happy/okay/sad/dead faces)
- Text messages shown for 2 seconds then cleared
- Stat indicators at bottom of screen (coloured dots for food/water/energy)
- Backlight dims after 30s inactivity, wakes on button press

**Extern declarations:**
Pet.cpp uses `extern void playTone()` and `extern void setLed()`.
Before participants implement those functions (Steps 2-3), the linker
needs stubs. Two approaches:
1. Pet.cpp has weak default implementations that do nothing
2. The .ino file has empty stubs that get replaced when sound.cpp/leds.cpp are created

**Recommended: weak defaults** — cleaner, participants never see them:
```cpp
__attribute__((weak)) void playTone(int, int) {}
__attribute__((weak)) void setLed(int, int, int) {}
```

This means the sketch compiles at every step without errors, and
the real implementations silently replace the stubs when created.

### PetConfig (Step 5 addition):

```cpp
struct PetConfig {
    int decayRate;
    int decayInterval;
    int feedAmount;
    int drinkAmount;
    int exerciseCap;
    int alertThreshold;
};
```

`Pet::begin()` uses hardcoded defaults.
`Pet::begin(PetConfig)` uses the provided config.
Both call the same internal init logic.

---

## Pre-made Melodies

Stored in `sound.h` (declarations) and `sound.cpp` (data).
All are `const int[][2]` arrays of `{frequency, duration}` pairs.
A frequency of 0 means a rest (silence for that duration).

| Name | Character | Notes |
|------|-----------|-------|
| `HAPPY_TUNE` | Bright rising joy | ~6 notes, major key, quick |
| `SAD_TUNE` | Melancholy descending | ~4 notes, minor key, slow |
| `WAKE_TUNE` | Cheerful startup jingle | ~8 notes, recognizable bounce |
| `VICTORY_TUNE` | Triumphant fanfare | ~8 notes, bold and resolved |
| `DEATH_TUNE` | Dramatic game over | ~4 notes, very low, very slow |
| `ALERT_TUNE` | Urgent attention beep | ~3 notes, short and sharp |

Participants use these with `playMelody(HAPPY_TUNE, HAPPY_TUNE_LEN)`.
They're encouraged to modify them or compose new ones.

---

## Toolchain

| Tool | Version | Notes |
|------|---------|-------|
| Arduino IDE | 2.x | Free, cross-platform |
| arduino-pico | latest | Earle Philhower, Board Manager |
| Adafruit ST7789 | latest | Library Manager |
| Adafruit GFX | latest | Pulled in by ST7789 |

Board Manager URL:
```
https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json
```

---

## Timing Estimate

| Step | Time |
|------|------|
| Intro + wiring | 20 min |
| Step 0: Hello World | 5 min |
| Step 1: Buttons | 20 min |
| Step 2: Sound + melodies | 20 min |
| Step 3: LEDs + Simon | 20 min |
| Step 4: Mash + decay | 15 min |
| Step 5: Playground | 20 min |
| **Total** | **~2 hrs** |

---

## Open Questions

1. **Melody licensing** — Are note sequences from recognizable tunes
   (Mario, Zelda) OK for a workshop, or should we stick to originals?
2. **Dead sprite** — still need actual pixel art for the dead face
3. **Weak extern stubs** — `__attribute__((weak))` is GCC-specific.
   Works on arduino-pico (GCC-based). Confirm no issues.
