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
// Each melody is an array of {frequency, duration} pairs.
// Frequency 0 = rest (silence for that duration).

// Cheerful startup jingle
const int WAKE_TUNE[][2] = {
    {523, 150}, {523, 150}, {0, 50},
    {523, 150}, {0, 50}, {415, 150},
    {523, 200}, {659, 200}, {523, 200}
};
const int WAKE_TUNE_LEN = 9;

// Rising major-key joy
const int HAPPY_TUNE[][2] = {
    {523, 120}, {659, 120}, {784, 120},
    {880, 200}, {784, 120}, {880, 300}
};
const int HAPPY_TUNE_LEN = 6;

// Descending minor sadness
const int SAD_TUNE[][2] = {
    {440, 300}, {392, 300}, {349, 400}, {330, 500}
};
const int SAD_TUNE_LEN = 4;

// Triumphant fanfare
const int VICTORY_TUNE[][2] = {
    {523, 150}, {523, 150}, {523, 150},
    {659, 400}, {587, 150}, {523, 150},
    {587, 150}, {659, 200}, {523, 200}
};
const int VICTORY_TUNE_LEN = 9;

// Dramatic game over
const int DEATH_TUNE[][2] = {
    {294, 400}, {277, 400}, {262, 400}, {247, 600}
};
const int DEATH_TUNE_LEN = 4;
