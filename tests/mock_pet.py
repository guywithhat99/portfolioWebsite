# tests/mock_pet.py
"""Host-testable Pet logic for unit tests. No MicroPython dependencies."""


class MockPet:
    STAT_MAX = 100
    STAT_MIN = 0
    HAPPY_THRESHOLD = 60
    SAD_THRESHOLD = 40
    ALERT_THRESHOLD = 30
    FEED_AMOUNT = 20

    def __init__(self):
        self.food = 100
        self.water = 100
        self.energy = 100

    def feed(self):
        self.food = min(self.STAT_MAX, self.food + self.FEED_AMOUNT)

    def water_pet(self):
        self.water = min(self.STAT_MAX, self.water + self.FEED_AMOUNT)

    def exercise(self):
        self.energy = min(self.STAT_MAX, self.energy + self.FEED_AMOUNT)

    def _decay_stat(self, stat_name, amount):
        current = getattr(self, stat_name)
        setattr(self, stat_name, max(self.STAT_MIN, current - amount))

    def mood(self):
        if self.food >= self.HAPPY_THRESHOLD and \
           self.water >= self.HAPPY_THRESHOLD and \
           self.energy >= self.HAPPY_THRESHOLD:
            return "happy"
        if self.food < self.SAD_THRESHOLD or \
           self.water < self.SAD_THRESHOLD or \
           self.energy < self.SAD_THRESHOLD:
            return "sad"
        return "okay"

    def needs_alert(self):
        return (self.food < self.ALERT_THRESHOLD or
                self.water < self.ALERT_THRESHOLD or
                self.energy < self.ALERT_THRESHOLD)
