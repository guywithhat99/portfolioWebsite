#include "sound.h"
#include <Arduino.h>

// =============================================================================
// SECTION 2 — BUZZER + MELODY
// =============================================================================
//
// Your job: make the pet produce sound.
//
// Pin: buzzer positive leg -> GP6
//
// Step 1 — setupBuzzer()
//   Configure the buzzer pin as an OUTPUT:
//     pinMode(6, OUTPUT);
//
// Step 2 — playTone(int freq, int duration)
//   Use the built-in tone() function:
//     tone(6, freq, duration);  // start the tone
//     delay(duration);          // wait for it to finish
//     noTone(6);                // stop
//
//   freq     = frequency in Hz  (440 = A4, 523 = C5, 880 = high A)
//   duration = how long in ms   (150 = short beep, 500 = half second)
//
// Step 3 — compose your WAKE_MELODY
//   A melody is an array of {frequency, duration} pairs.
//   Common note frequencies:
//     C5 = 523   D5 = 587   E5 = 659   F5 = 698
//     G5 = 784   A5 = 880   B5 = 988
//
//   Example:
//     int WAKE_MELODY[][2] = {
//         {523, 150},   // C5
//         {659, 150},   // E5
//         {784, 300},   // G5
//     };
//     const int WAKE_MELODY_LEN = 3;
//
// Step 4 — playMelody(int notes[][2], int len)
//   Loop over the notes array and call playTone() for each one.
//
// Once done, go to tomogatchi.ino and uncomment:
//   setupBuzzer();   in setup()
// Then wire playMelody(WAKE_MELODY, WAKE_MELODY_LEN) to a button in
// readButtons() inside buttons.cpp (replace pet.say() on red button).
// =============================================================================

const int PIN_BUZZER = 6;

// === YOUR CODE HERE ===

// void setupBuzzer() {
//
// }

// void playTone(int freq, int duration) {
//
// }

// int WAKE_MELODY[][2] = {
//     {523, 150},
//     {659, 150},
//     {784, 300},
// };
// const int WAKE_MELODY_LEN = 3;

// void playMelody(int notes[][2], int len) {
//
// }


// =============================================================================
// FALLBACK (working solution — uncomment if stuck)
// =============================================================================
// void setupBuzzer() {
//     pinMode(PIN_BUZZER, OUTPUT);
// }
//
// void playTone(int freq, int duration) {
//     tone(PIN_BUZZER, freq, duration);
//     delay(duration);
//     noTone(PIN_BUZZER);
// }
//
// int WAKE_MELODY[][2] = {
//     {523, 150},   // C5
//     {659, 150},   // E5
//     {784, 300},   // G5
// };
// const int WAKE_MELODY_LEN = 3;
//
// void playMelody(int notes[][2], int len) {
//     for (int i = 0; i < len; i++) {
//         playTone(notes[i][0], notes[i][1]);
//     }
// }
