// =============================================================================
// TOMOGATCHI WORKSHOP
// =============================================================================
//
// Your pet is alive — but barely. It shows one face and does nothing else.
// Work through each section to bring it to life.
//
// Files you will write (open each tab above):
//   buttons.h / buttons.cpp  — Section 1: wire up buttons, make the pet speak
//   sound.h   / sound.cpp    — Section 2: add sound and compose a melody
//   leds.h    / leds.cpp     — Section 3: add the RGB LED, play Simon Says
//   tomogatchi.ino           — Section 4: enable decay, add button mash (this file)
//
// Files to READ but NOT edit:
//   Pet.h / Pet.cpp          — the pet engine (read it, it's interesting!)
//   sprites.h                — sprite pixel data stored in flash memory
//
// Pet API quick reference:
//   pet.say(text)            — show text on screen for 2 seconds
//   pet.catchphrase()        — returns a phrase based on the pet's mood
//   pet.feed()               — increase food stat
//   pet.drink()              — increase water stat
//   pet.exercise(boost)      — increase energy by boost (max 30)
//   pet.enableDecay()        — start stat decay (call once in Section 4)
//   pet.mood()               — returns Mood::HAPPY, OKAY, SAD, or DEAD
// =============================================================================

#include "buttons.h"
#include "sound.h"
#include "leds.h"
#include "Pet.h"

Pet pet;

void setup() {
    pet.begin();

    // Section 1: uncomment when you've written setupButtons()
    // setupButtons();

    // Section 2: uncomment when you've written setupBuzzer()
    // setupBuzzer();

    // Section 3: uncomment when you've written setupLeds()
    // setupLeds();

    // Section 4: uncomment to enable stat decay and start the real game
    // pet.enableDecay();
}

void loop() {
    // Section 1: uncomment when you've written readButtons()
    // readButtons(pet);

    pet.update();
    delay(50);
}


// =============================================================================
// SECTION 4 — BUTTON MASH
// =============================================================================
// When you reach Section 4, replace the loop() above with this one.
// It adds a 3-second button mash window for the green button.
//
// New concepts: millis(), elapsed time, counters
//
// void loop() {
//     static bool lastGreen = false;
//     bool green = digitalRead(19);
//
//     // --- Button mash (green button) ---
//     if (green && !lastGreen) {
//         int presses = 0;
//         unsigned long start = millis();
//         bool prevBtn = true;
//
//         pet.say("MASH IT!");
//
//         while (millis() - start < 3000) {
//             bool btn = digitalRead(19);
//             if (btn && !prevBtn) presses++;
//             prevBtn = btn;
//             pet.update();
//             delay(10);
//         }
//         pet.exercise(presses);
//     }
//
//     lastGreen = green;
//     readButtons(pet);
//     pet.update();
//     delay(50);
// }


// =============================================================================
// FALLBACK — full working sketch (uncomment everything below if stuck)
// =============================================================================
// void setup() {
//     pet.begin();
//     setupButtons();
//     setupBuzzer();
//     setupLeds();
//     pet.enableDecay();
// }
//
// void loop() {
//     static bool lastGreen = false;
//     bool green = digitalRead(19);
//
//     if (green && !lastGreen) {
//         int presses = 0;
//         unsigned long start = millis();
//         bool prevBtn = true;
//         pet.say("MASH IT!");
//         while (millis() - start < 3000) {
//             bool btn = digitalRead(19);
//             if (btn && !prevBtn) presses++;
//             prevBtn = btn;
//             pet.update();
//             delay(10);
//         }
//         pet.exercise(presses);
//     }
//
//     lastGreen = green;
//     readButtons(pet);
//     pet.update();
//     delay(50);
// }
