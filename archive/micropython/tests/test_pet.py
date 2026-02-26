# tests/test_pet.py
"""
Tests for Pet state machine logic.
Run on host: python -m pytest tests/test_pet.py -v

These tests use a mock Pet that replaces hardware-dependent code,
testing only the pure stat/mood logic.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tests.mock_pet import MockPet


class TestStats:
    def test_initial_stats_are_full(self):
        pet = MockPet()
        assert pet.food == 100
        assert pet.water == 100
        assert pet.energy == 100

    def test_feed_increases_food(self):
        pet = MockPet()
        pet.food = 50
        pet.feed()
        assert pet.food == 70

    def test_feed_caps_at_100(self):
        pet = MockPet()
        pet.food = 95
        pet.feed()
        assert pet.food == 100

    def test_water_increases_water(self):
        pet = MockPet()
        pet.water = 40
        pet.water_pet()
        assert pet.water == 60

    def test_exercise_increases_energy(self):
        pet = MockPet()
        pet.energy = 30
        pet.exercise()
        assert pet.energy == 50

    def test_stats_floor_at_zero(self):
        pet = MockPet()
        pet.food = 5
        pet._decay_stat("food", 10)
        assert pet.food == 0


class TestMood:
    def test_all_high_is_happy(self):
        pet = MockPet()
        pet.food = 80
        pet.water = 80
        pet.energy = 80
        assert pet.mood() == "happy"

    def test_any_below_40_is_sad(self):
        pet = MockPet()
        pet.food = 35
        pet.water = 80
        pet.energy = 80
        assert pet.mood() == "sad"

    def test_mixed_is_okay(self):
        pet = MockPet()
        pet.food = 50
        pet.water = 50
        pet.energy = 50
        assert pet.mood() == "okay"

    def test_boundary_exactly_60_is_happy(self):
        pet = MockPet()
        pet.food = 60
        pet.water = 60
        pet.energy = 60
        assert pet.mood() == "happy"

    def test_boundary_exactly_40_is_okay_not_sad(self):
        pet = MockPet()
        pet.food = 40
        pet.water = 80
        pet.energy = 80
        assert pet.mood() == "okay"


class TestAlerts:
    def test_alert_fires_when_stat_below_30(self):
        pet = MockPet()
        pet.food = 25
        assert pet.needs_alert() is True

    def test_no_alert_when_all_stats_ok(self):
        pet = MockPet()
        pet.food = 50
        pet.water = 50
        pet.energy = 50
        assert pet.needs_alert() is False
