#include "Pet.h"
#include "buttons.h"
#include "sound.h"
#include "leds.h"
#include "game.h"

Pet pet;

// === PET SETTINGS — tweak these! ===
PetConfig config;

void setup() {
    // Customise your pet (try changing these values!)
    // config.decayRate      = 1;      // how much stats drop each tick
    // config.decayInterval  = 10000;  // ms between decay ticks (lower = harder)
    // config.feedAmount     = 20;     // how much food one press gives
    // config.drinkAmount    = 20;     // how much water one press gives
    // config.exerciseCap    = 30;     // max energy from one mash session
    // config.alertThreshold = 30;     // stat level that triggers alerts

    pet.begin(config);
    setupButtons();
    setupBuzzer();
    setupLeds();
    pet.enableDecay();
}

void loop() {
    static bool lastGreen = false;
    bool green = digitalRead(19);

    if (green && !lastGreen) {
        pet.say("MASH IT!");
        int presses = buttonMash(19, 3000);
        pet.exercise(presses);
    }

    lastGreen = green;
    readButtons(pet);
    pet.update();
    delay(50);
}
