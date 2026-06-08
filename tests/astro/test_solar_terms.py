"""Tests for the core solar position terms."""

from __future__ import annotations

from hebrewcal.astro.solar import equation_of_time, solar_declination


def test_declination_near_solstices() -> None:
    # Around the June solstice the declination is near +23.4 degrees; around the
    # December solstice near -23.4 degrees.
    jun = solar_declination(2026, 6, 21)
    dec = solar_declination(2026, 12, 21)
    assert 23.0 <= jun <= 23.5
    assert -23.5 <= dec <= -23.0


def test_declination_near_equinoxes() -> None:
    # Near the equinoxes the declination crosses zero.
    assert abs(solar_declination(2026, 3, 20)) < 1.0
    assert abs(solar_declination(2026, 9, 23)) < 1.0


def test_equation_of_time_range() -> None:
    # The equation of time stays within roughly +-16.5 minutes across the year.
    values = [equation_of_time(2026, m, 15) for m in range(1, 13)]
    assert all(-17.0 <= v <= 17.0 for v in values)
    # It is strongly negative in mid-February and strongly positive in early November.
    assert equation_of_time(2026, 2, 11) < -13.0
    assert equation_of_time(2026, 11, 3) > 16.0
