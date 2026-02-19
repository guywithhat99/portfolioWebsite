# tamagotchi.py
"""
Tomogatchi Workshop — boilerplate (read-only)

This file contains the pet state machine, display rendering, stat decay,
alert system, and power saving logic. You don't need to modify this file —
but reading it is encouraged!
"""

import time
import urandom
from display import Display

# ── Constants ────────────────────────────────────────────────────────────────

STAT_MAX        = 100
STAT_MIN        = 0
HAPPY_THRESHOLD = 60   # all stats must be at or above this to be happy
SAD_THRESHOLD   = 40   # any stat below this triggers sad mood
ALERT_THRESHOLD = 30   # any stat below this triggers buzzer alert
FEED_AMOUNT     = 20   # how much each button press adds to a stat
DECAY_RATE      = 1    # stat points lost per DECAY_INTERVAL_MS
DECAY_INTERVAL  = 10000  # ms between each decay tick (10 seconds)
BACKLIGHT_TIMEOUT = 30000  # ms of inactivity before backlight turns off

# Alert tone
ALERT_FREQ      = 880   # Hz
ALERT_DURATION  = 150   # ms

# Display layout
SPRITE_W   = 120
SPRITE_H   = 120
SPRITE_X   = (Display.WIDTH - SPRITE_W) // 2   # centered
SPRITE_Y   = 20

# Text zone (below sprite)
TEXT_Y     = SPRITE_Y + SPRITE_H + 10

# Button indicator row
INDICATOR_Y    = Display.HEIGHT - 30
INDICATOR_R    = 8
INDICATOR_POSITIONS = [40, 120, 200]
INDICATOR_COLORS    = [Display.RED, Display.YELLOW, Display.GREEN]
INDICATOR_LABELS    = ["Food", "Water", "Move"]

# Encouragement messages per action
MESSAGES = {
    "feed":     ["Yum!", "So tasty!", "Delicious!", "Thanks!", "More please!"],
    "water":    ["Refreshing!", "So hydrated!", "Ahh!", "Thanks!", "Splish splash!"],
    "exercise": ["Go go go!", "Feeling fit!", "Wahoo!", "So strong!", "Keep it up!"],
    "alert":    ["Hey...", "I'm hungry...", "Don't forget me!", "Hellooo?"],
}


# ── Sprite loading ───────────────────────────────────────────────────────────

def _load_sprite(mood):
    """Load a 120x120 RGB565 raw image from the images/ directory."""
    for path in (f"/images/{mood}.raw", f"images/{mood}.raw"):
        try:
            with open(path, "rb") as f:
                return f.read()
        except OSError:
            pass
    # Fallback: solid grey block if file missing (memory-efficient)
    return b'\x84\x10' * (SPRITE_W * SPRITE_H)


# ── Pet class ─────────────────────────────────────────────────────────────────

class Pet:
    """
    The virtual pet. Receives play_tone and set_led as callables so
    participant-written hardware code drives the game.

    Usage:
        pet = Pet(play_tone, set_led)
        pet.feed()      # red button
        pet.water()     # yellow button
        pet.exercise()  # green button
        pet.update()    # call every loop iteration
    """

    def __init__(self, play_tone, set_led):
        self._play_tone = play_tone
        self._set_led   = set_led
        self._lcd       = Display()

        # Stats
        self.food   = STAT_MAX
        self.water  = STAT_MAX
        self.energy = STAT_MAX

        # Internal timing
        self._last_decay    = time.ticks_ms()
        self._last_activity = time.ticks_ms()
        self._msg_clear_at  = 0
        self._backlight_on  = True
        self._last_mood     = None
        self._current_msg   = ""
        self._last_alert    = 0  # cooldown timer for alerts

        # Draw initial screen
        self._lcd.fill(Display.BLACK)
        self._draw_indicators()
        self._redraw()

    # ── Public API ───────────────────────────────────────────────────────────

    def feed(self):
        self.food = min(STAT_MAX, self.food + FEED_AMOUNT)
        self._on_action("feed")

    def water(self):
        self.water = min(STAT_MAX, self.water + FEED_AMOUNT)
        self._on_action("water")

    def exercise(self):
        self.energy = min(STAT_MAX, self.energy + FEED_AMOUNT)
        self._on_action("exercise")

    def update(self):
        """Call every loop iteration. Handles decay, alerts, and redraw."""
        now = time.ticks_ms()

        # Stat decay
        if time.ticks_diff(now, self._last_decay) >= DECAY_INTERVAL:
            self._decay_all()
            self._last_decay = now

        # Clear message after 2 seconds
        if self._current_msg and time.ticks_diff(now, self._msg_clear_at) >= 0:
            self._current_msg = ""
            self._clear_text_zone()

        # Backlight timeout (power saving)
        # The display backlight is the biggest battery drain. Turning it off
        # after 30 seconds of inactivity significantly extends battery life.
        # We use machine.lightsleep() in the main loop for the same reason.
        if self._backlight_on:
            if time.ticks_diff(now, self._last_activity) >= BACKLIGHT_TIMEOUT:
                self._lcd.backlight(False)
                self._backlight_on = False

        # Redraw if mood changed
        new_mood = self.mood()
        if new_mood != self._last_mood:
            self._redraw()

        # Alert if any stat is critical (with 15-second cooldown)
        if self.needs_alert():
            if time.ticks_diff(now, self._last_alert) >= 15000:
                self._last_alert = now
                self._trigger_alert()

    # ── Stat logic ───────────────────────────────────────────────────────────

    def mood(self):
        if (self.food  >= HAPPY_THRESHOLD and
            self.water >= HAPPY_THRESHOLD and
            self.energy >= HAPPY_THRESHOLD):
            return "happy"
        if (self.food  < SAD_THRESHOLD or
            self.water < SAD_THRESHOLD or
            self.energy < SAD_THRESHOLD):
            return "sad"
        return "okay"

    def needs_alert(self):
        return (self.food  < ALERT_THRESHOLD or
                self.water < ALERT_THRESHOLD or
                self.energy < ALERT_THRESHOLD)

    def _decay_all(self):
        self.food   = max(STAT_MIN, self.food   - DECAY_RATE)
        self.water  = max(STAT_MIN, self.water  - DECAY_RATE)
        self.energy = max(STAT_MIN, self.energy - DECAY_RATE)

    # ── Private helpers ──────────────────────────────────────────────────────

    def _on_action(self, action):
        """Shared logic for all button actions."""
        self._last_activity = time.ticks_ms()
        if not self._backlight_on:
            self._lcd.backlight(True)
            self._backlight_on = True
        msg = MESSAGES[action][urandom.randint(0, len(MESSAGES[action]) - 1)]
        self._show_message(msg)
        self._redraw()

    def _trigger_alert(self):
        msg = MESSAGES["alert"][urandom.randint(0, len(MESSAGES["alert"]) - 1)]
        self._show_message(msg)
        self._play_tone(ALERT_FREQ, ALERT_DURATION)
        # Brief red LED flash
        self._set_led(1, 0, 0)
        time.sleep_ms(200)
        self._set_led(0, 0, 0)
        self._redraw_sprite("alert")

    def _redraw(self):
        mood = self.mood()
        self._last_mood = mood
        self._redraw_sprite(mood)
        if self._current_msg:
            self._draw_text(self._current_msg)

    def _redraw_sprite(self, name):
        data = _load_sprite(name)
        self._lcd.sprite(data, SPRITE_X, SPRITE_Y, SPRITE_W, SPRITE_H)

    def _draw_indicators(self):
        """Draw the static button indicator row. Called once at init."""
        for x, color, label in zip(
                INDICATOR_POSITIONS, INDICATOR_COLORS, INDICATOR_LABELS):
            self._lcd.fill_circle(x, INDICATOR_Y, INDICATOR_R, color)
            # Centre label text under its circle
            lx = x - self._lcd.text_width(label) // 2
            self._lcd.text(label, lx, INDICATOR_Y + INDICATOR_R + 4,
                           Display.WHITE)

    def _show_message(self, msg):
        self._current_msg = msg
        self._msg_clear_at = time.ticks_ms() + 2000
        self._draw_text(msg)

    def _draw_text(self, msg):
        self._clear_text_zone()
        self._lcd.text_centered(msg, TEXT_Y, Display.WHITE, scale=2)

    def _clear_text_zone(self):
        self._lcd.fill_rect(0, TEXT_Y, Display.WIDTH, 30, Display.BLACK)
