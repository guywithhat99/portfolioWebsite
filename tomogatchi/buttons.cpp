#include "buttons.h"

// =============================================================================
// SECTION 1 — BUTTONS + CATCHPHRASES
// =============================================================================
//
// Your job: wire up the three buttons and make the pet speak.
//
// Pin numbers:
//   Red button    -> GP22
//   Yellow button -> GP21
//   Green button  -> GP19
//
// Step 1 — setupButtons()
//   Configure each pin as an INPUT with a pull-down resistor:
//     pinMode(22, INPUT_PULLDOWN);
//
//   INPUT_PULLDOWN keeps the pin at LOW (0) when the button is not pressed.
//   When the button IS pressed, it connects the pin to 3.3V -> reads HIGH (1).
//
// Step 2 — readButtons(Pet& pet)
//   Read each button with digitalRead(pin).
//   On a fresh press (HIGH now, was LOW last loop), call:
//     pet.say(pet.catchphrase());
//
//   The "last state" trick prevents one press registering many times:
//     static bool lastRed = false;
//     bool red = digitalRead(22);
//     if (red && !lastRed) { /* fresh press */ }
//     lastRed = red;
//
// Once done, go to tomogatchi.ino and uncomment:
//   setupButtons();   in setup()
//   readButtons(pet); in loop()
// =============================================================================

const int PIN_BTN_RED    = 22;
const int PIN_BTN_YELLOW = 21;
const int PIN_BTN_GREEN  = 19;

// === YOUR CODE HERE ===

// void setupButtons() {
//
// }

// void readButtons(Pet& pet) {
//
// }


// =============================================================================
// FALLBACK (working solution — uncomment if stuck)
// =============================================================================
// static bool lastRed = false, lastYellow = false, lastGreen = false;
//
// void setupButtons() {
//     pinMode(PIN_BTN_RED,    INPUT_PULLDOWN);
//     pinMode(PIN_BTN_YELLOW, INPUT_PULLDOWN);
//     pinMode(PIN_BTN_GREEN,  INPUT_PULLDOWN);
// }
//
// void readButtons(Pet& pet) {
//     bool red    = digitalRead(PIN_BTN_RED);
//     bool yellow = digitalRead(PIN_BTN_YELLOW);
//     bool green  = digitalRead(PIN_BTN_GREEN);
//
//     if (red    && !lastRed)    pet.say(pet.catchphrase());
//     if (yellow && !lastYellow) pet.say(pet.catchphrase());
//     if (green  && !lastGreen)  pet.say(pet.catchphrase());
//
//     lastRed = red; lastYellow = yellow; lastGreen = green;
// }
