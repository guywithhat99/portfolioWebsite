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

    if (red && !lastRed) {
        pet.feed();
        chirp(pet.mood());
    }

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
