#include <Arduino.h>
#include "game.h"

int buttonMash(int pin, int durationMs) {
    int presses = 0;
    bool lastBtn = digitalRead(pin);
    unsigned long start = millis();

    while (millis() - start < (unsigned long)durationMs) {
        bool btn = digitalRead(pin);
        if (btn && !lastBtn) presses++;
        lastBtn = btn;
        delay(10);
    }
    return presses;
}
