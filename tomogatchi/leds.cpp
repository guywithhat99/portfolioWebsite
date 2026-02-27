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

// --- Simon Says (provided — uses your setLed and playTone) ------------

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

    // Read player input — 5-second window per step
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
