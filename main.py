# =============================================================================
# TOMOGATCHI WORKSHOP — main.py
# =============================================================================
#
# Welcome! This is YOUR file. Everything in the sections marked
# "=== YOUR CODE HERE ===" is for you to complete.
#
# The rest of the project is in tamagotchi.py — you don't need to edit it,
# but you're encouraged to read it and see how it all fits together.
#
# Workshop sections:
#   1. Button setup     — configure three input pins
#   2. LED helper       — control the RGB LED
#   3. Buzzer helper    — play tones with the piezo buzzer
#
# The game loop at the bottom is provided — once your three sections
# are complete, the full game will run.
# =============================================================================

from machine import Pin, PWM
import time
import machine
from tamagotchi import Pet


# =============================================================================
# SECTION 1: BUTTON SETUP
# =============================================================================
# The three buttons connect to GPIO pins on the Pico.
# Each button needs to be configured as an INPUT with a pull-down resistor.
# A pull-down resistor ensures the pin reads 0 when the button is NOT pressed,
# and 1 when it IS pressed.
#
# Use:  Pin(<number>, Pin.IN, Pin.PULL_DOWN)
#
# Pin numbers:
#   Red button    → GP22
#   Yellow button → GP21
#   Green button  → GP19
#
# HINT: Look at how btn_red is used in the game loop below — each button
# is read with .value(), which returns 0 or 1.
# =============================================================================

# === YOUR CODE HERE ===

# btn_red    = ...
# btn_yellow = ...
# btn_green  = ...


# =============================================================================
# SECTION 2: LED HELPER
# =============================================================================
# The RGB LED has three separate colour pins — one for red, one for green,
# one for blue. Setting a pin HIGH (1) turns that colour on.
#
# The three LED pins are already set up for you below.
# Your job is to complete the set_led() function so it sets each pin
# to the value passed in (0 for off, 1 for on).
#
# HINT: Use led_r.value(r) — and do the same for green and blue.
# =============================================================================

led_r = Pin(16, Pin.OUT)
led_g = Pin(17, Pin.OUT)
led_b = Pin(18, Pin.OUT)


def set_led(r, g, b):
    """Set the RGB LED colour. Each channel is 0 (off) or 1 (on)."""
    # === YOUR CODE HERE ===
    pass


# =============================================================================
# SECTION 3: BUZZER HELPER
# =============================================================================
# The piezoelectric buzzer is controlled with PWM (Pulse Width Modulation).
# PWM rapidly switches the pin on and off — the speed (frequency) determines
# the pitch, and the duty cycle determines the volume.
#
# The buzzer pin is already set up for you below.
# Your job is to complete the play_tone() function:
#   1. Set the frequency:   buzzer.freq(frequency)
#   2. Turn it on (50%):    buzzer.duty_u16(32768)
#   3. Wait:                time.sleep_ms(duration_ms)
#   4. Turn it off:         buzzer.duty_u16(0)
#
# HINT: duty_u16 sets the duty cycle from 0 (off) to 65535 (full on).
#       32768 is exactly 50% — a good middle ground for the buzzer.
# =============================================================================

buzzer = PWM(Pin(6))


def play_tone(frequency, duration_ms):
    """Play a tone at the given frequency (Hz) for duration_ms milliseconds."""
    # === YOUR CODE HERE ===
    pass


# =============================================================================
# GAME LOOP (provided — read, don't edit)
# =============================================================================
# This sets up the pet and runs the main loop.
# The pet receives your set_led and play_tone functions — once you've
# completed the sections above, your code will drive the game.
#
# Button debounce: we track the last button state to avoid registering
# a single press multiple times.
# =============================================================================

print("Starting Tomogatchi...")
pet = Pet(play_tone, set_led)

last_red    = 0
last_yellow = 0
last_green  = 0

while True:
    red    = btn_red.value()
    yellow = btn_yellow.value()
    green  = btn_green.value()

    if red and not last_red:
        pet.feed()
    elif yellow and not last_yellow:
        pet.water()
    elif green and not last_green:
        pet.exercise()

    last_red    = red
    last_yellow = yellow
    last_green  = green

    pet.update()
    machine.lightsleep(50)  # low-power wait between loop iterations
