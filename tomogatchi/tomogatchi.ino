// =============================================================================
// TOMOGATCHI WORKSHOP
// =============================================================================
//
// Your pet is alive -- but barely. It shows one face and does nothing else.
// Work through each section to bring it to life.
//
// Files you will write (open each tab above):
//   buttons.h / buttons.cpp  -- Section 1: wire up buttons, make the pet speak
//   sound.h   / sound.cpp    -- Section 2: add sound and compose a melody
//   leds.h    / leds.cpp     -- Section 3: add the RGB LED, play Simon Says
//   game.h    / game.cpp     -- Section 4: write the button mash game
//   tomogatchi.ino           -- Section 4: wire mash into the game loop (this file)
//
// Files to READ but NOT edit:
//   Pet.h / Pet.cpp          -- the pet engine (read it, it's interesting!)
//   sprites.h                -- sprite pixel data stored in flash memory
//
// Pet API quick reference:
//   pet.say(text)            -- show text on screen for 2 seconds
//   pet.catchphrase()        -- returns a phrase based on the pet's mood
//   pet.feed()               -- increase food stat
//   pet.drink()              -- increase water stat
//   pet.exercise(boost)      -- increase energy by boost (max 30)
//   pet.enableDecay()        -- start stat decay (call once in Section 4)
//   pet.mood()               -- returns Mood::HAPPY, OKAY, SAD, or DEAD
// =============================================================================

#include "buttons.h"
#include "sound.h"
#include "leds.h"
#include "game.h"
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
// SECTION 4 -- WIRE IN THE BUTTON MASH
// =============================================================================
// Once you've written buttonMash() in game.cpp, replace loop() above
// with this version. It calls your function and passes the result to
// pet.exercise().
//
// Your task here: fill in the two blanks marked ??? below.
//   - What pin is the green button on?
//   - How long should the mash window last (in ms)?
//
// void loop() {
//     static bool lastGreen = false;
//     bool green = digitalRead(19);
//
//     if (green && !lastGreen) {
//         pet.say("MASH IT!");
//         int presses = buttonMash(???, ???);   // <- fill these in
//         pet.exercise(presses);
//     }
//
//     lastGreen = green;
//     readButtons(pet);
//     pet.update();
//     delay(50);
// }


// =============================================================================
// FALLBACK -- full working sketch (uncomment if stuck)
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
//         pet.say("MASH IT!");
//         int presses = buttonMash(19, 3000);
//         pet.exercise(presses);
//     }
//
//     lastGreen = green;
//     readButtons(pet);
//     pet.update();
//     delay(50);
// }
