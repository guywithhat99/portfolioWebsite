#include "game.h"
#include <Arduino.h>

// =============================================================================
// SECTION 4 — BUTTON MASH GAME
// =============================================================================
//
// Your job: count how many times a button is pressed within a time window.
//
// New concept — millis()
//   millis() returns the number of milliseconds since the Pico started.
//   You can use it to measure elapsed time without using delay():
//
//     unsigned long start = millis();
//     while (millis() - start < 3000) {
//         // this loop runs for exactly 3 seconds
//     }
//
//   This is called a non-blocking timer. Unlike delay(), the Pico can
//   still do other things inside the loop while waiting.
//
// Your task — implement buttonMash(int pin, int durationMs):
//
//   1. Record the start time:
//        unsigned long start = millis();
//
//   2. Loop until durationMs have passed:
//        while (millis() - start < durationMs) { ... }
//
//   3. Inside the loop, detect fresh presses (HIGH now, LOW last iteration):
//        bool btn = digitalRead(pin);
//        if (btn && !lastBtn) presses++;
//        lastBtn = btn;
//
//   4. Return the total press count.
//
// Once done:
//   - In tomogatchi.ino, add #include "game.h" (already there)
//   - Uncomment the green button handler in the loop() section
//
// =============================================================================

// === YOUR CODE HERE ===

// int buttonMash(int pin, int durationMs) {
//
// }


// =============================================================================
// FALLBACK (working solution — uncomment if stuck)
// =============================================================================
// int buttonMash(int pin, int durationMs) {
//     int presses = 0;
//     bool lastBtn = digitalRead(pin);
//     unsigned long start = millis();
//
//     while (millis() - start < (unsigned long)durationMs) {
//         bool btn = digitalRead(pin);
//         if (btn && !lastBtn) presses++;
//         lastBtn = btn;
//         delay(10);
//     }
//     return presses;
// }
