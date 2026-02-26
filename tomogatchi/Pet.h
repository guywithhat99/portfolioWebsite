#pragma once
#include <Arduino.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7789.h>

// ── Mood ─────────────────────────────────────────────────────────────────────

enum class Mood { HAPPY, OKAY, SAD, DEAD };

// ── Pet ──────────────────────────────────────────────────────────────────────
//
// The virtual pet. Read this file to understand the API.
// Edit Pet.h or Pet.cpp is NOT part of the workshop tasks.
//
// Usage:
//   Pet pet;
//   pet.begin();          // call once in setup()
//   pet.update();         // call every loop iteration
//
// Actions (wire to buttons in tomogatchi.ino):
//   pet.feed();
//   pet.drink();
//   pet.exercise(boost);  // boost = button-mash count, capped at 30
//   pet.enableDecay();    // call once in Section 4 to start stat decay
//
// Workshop helpers (use in your button handlers):
//   pet.say(text)         // shows text on screen for 2 seconds
//   pet.catchphrase()     // returns a mood-appropriate phrase string
//
// State:
//   pet.mood()            // returns Mood enum: HAPPY, OKAY, SAD, DEAD
//   pet.needsAlert()      // true if any stat below alert threshold

class Pet {
public:
    Pet();
    void begin();
    void update();

    // ── Actions ──────────────────────────────────────────────────────────────
    void feed();
    void drink();
    void exercise(int boost);
    void enableDecay();

    // ── Workshop helpers ─────────────────────────────────────────────────────
    String catchphrase();
    void   say(String text);

    // ── State ────────────────────────────────────────────────────────────────
    Mood mood();
    bool needsAlert();

    // Public stat access (read-only by convention)
    int food;
    int water;
    int energy;

private:
    Adafruit_ST7789 _lcd;

    bool          _decayEnabled;
    bool          _backlightOn;
    Mood          _lastMood;
    String        _currentMsg;
    unsigned long _lastDecay;
    unsigned long _lastActivity;
    unsigned long _msgClearAt;
    unsigned long _lastAlert;

    Mood   _computeMood();
    void   _decayAll();
    void   _redraw();
    void   _drawSprite(Mood m);
    void   _drawIndicators();
    void   _showMessage(String msg);
    void   _clearTextZone();
    void   _triggerAlert();
};
