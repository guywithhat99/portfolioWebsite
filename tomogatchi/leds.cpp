#include "leds.h"
#include "sound.h"
#include <Arduino.h>

// =============================================================================
// SECTION 3 — RGB LED + SIMON SAYS
// =============================================================================
//
// Your job: control the RGB LED, then play Simon Says.
//
// Pins:
//   Red   channel -> GP16
//   Green channel -> GP17
//   Blue  channel -> GP18
//
// Step 1 — setupLeds()
//   Configure all three pins as OUTPUT:
//     pinMode(16, OUTPUT);
//     pinMode(17, OUTPUT);
//     pinMode(18, OUTPUT);
//
// Step 2 — setLed(int r, int g, int b)
//   Each argument is 0 (off) or 1 (on).
//   Use digitalWrite() to set each pin:
//     digitalWrite(16, r);
//     digitalWrite(17, g);
//     digitalWrite(18, b);
//
//   Try it:
//     setLed(1, 0, 0)  -> RED
//     setLed(0, 1, 0)  -> GREEN
//     setLed(1, 1, 0)  -> YELLOW (red + green mixed!)
//     setLed(1, 0, 1)  -> MAGENTA
//     setLed(0, 0, 0)  -> OFF
//
// Step 3 — wire Simon Says to the yellow button
//   playSimon() is already written below — it uses YOUR setLed() and
//   playTone() from sound.cpp. Both must be implemented first!
//
//   In buttons.cpp, add to readButtons():
//     if (yellow && !lastYellow) {
//         bool won = playSimon();
//         won ? pet.feed() : pet.say("Nope...");
//     }
//
// Once done, uncomment setupLeds() in tomogatchi.ino setup().
// =============================================================================

const int PIN_LED_R = 16;
const int PIN_LED_G = 17;
const int PIN_LED_B = 18;

// === YOUR CODE HERE ===

// void setupLeds() {
//
// }

// void setLed(int r, int g, int b) {
//
// }


// =============================================================================
// PROVIDED — Simon Says game
// Read this code — don't edit it.
// It uses setLed() and playTone() which YOU wrote in Sections 2 and 3.
// This is the payoff: your hardware code drives a real game.
// =============================================================================

bool playSimon() {
    const int SEQ_LEN = 3;

    // Three colours: index 0=red, 1=green, 2=yellow
    // Each row is {r, g, b}
    int colours[3][3] = {
        {1, 0, 0},   // red
        {0, 1, 0},   // green
        {1, 1, 0},   // yellow
    };
    int buttons[3] = {22, 21, 19};       // red, yellow, green pin numbers
    int tones[3]   = {440, 523, 659};    // A4, C5, E5

    // Generate a random sequence
    int seq[SEQ_LEN];
    for (int i = 0; i < SEQ_LEN; i++) {
        seq[i] = random(3);
    }

    // Flash the sequence to the player
    delay(500);
    for (int i = 0; i < SEQ_LEN; i++) {
        int c = seq[i];
        setLed(colours[c][0], colours[c][1], colours[c][2]);
        playTone(tones[c], 400);
        setLed(0, 0, 0);
        delay(200);
    }
    delay(300);

    // Read the player's input — 5-second window per step
    for (int i = 0; i < SEQ_LEN; i++) {
        unsigned long start = millis();
        bool waiting = true;
        while (waiting && millis() - start < 5000) {
            for (int b = 0; b < 3; b++) {
                if (digitalRead(buttons[b])) {
                    // Show feedback
                    setLed(colours[b][0], colours[b][1], colours[b][2]);
                    playTone(tones[b], 200);
                    setLed(0, 0, 0);
                    delay(100);
                    if (b != seq[i]) return false;   // wrong button
                    waiting = false;
                    break;
                }
            }
            delay(10);
        }
        if (waiting) return false;  // timeout
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


// =============================================================================
// FALLBACK — setupLeds + setLed (uncomment if stuck)
// =============================================================================
// void setupLeds() {
//     pinMode(PIN_LED_R, OUTPUT);
//     pinMode(PIN_LED_G, OUTPUT);
//     pinMode(PIN_LED_B, OUTPUT);
// }
//
// void setLed(int r, int g, int b) {
//     digitalWrite(PIN_LED_R, r);
//     digitalWrite(PIN_LED_G, g);
//     digitalWrite(PIN_LED_B, b);
// }
