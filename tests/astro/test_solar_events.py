"""Tests for sunrise, sunset and solar noon."""

from __future__ import annotations

import datetime

from hebrewcal.astro.location import Location
from hebrewcal.astro.solar import solar_noon, sunrise, sunset
from hebrewcal.calendars.gregorian import GregorianDate

NEW_YORK = Location(40.7128, -74.0060, timezone="America/New_York")
JERUSALEM = Location(31.7683, 35.2137, timezone="Asia/Jerusalem")
NORTH_POLE = Location(89.9, 0.0, timezone="UTC")


def _close(actual: datetime.datetime, hh: int, mm: int, ss: int, tol_seconds: int = 120) -> bool:
    expect = actual.replace(hour=hh, minute=mm, second=ss, microsecond=0)
    return abs((actual - expect).total_seconds()) <= tol_seconds


def test_new_york_sunrise_sunset() -> None:
    date = GregorianDate(2026, 6, 26)
    # Reference (cross-checked against NOAA/astral): 05:26:45 and 20:31:03 EDT.
    rise = sunrise(date, NEW_YORK)
    set_ = sunset(date, NEW_YORK)
    assert rise is not None and set_ is not None
    assert _close(rise, 5, 26, 45)
    assert _close(set_, 20, 31, 3)


def test_jerusalem_sunrise_sunset() -> None:
    date = GregorianDate(2026, 6, 26)
    # Reference: 05:35:41 and 19:48:16 IDT.
    rise = sunrise(date, JERUSALEM)
    set_ = sunset(date, JERUSALEM)
    assert rise is not None and set_ is not None
    assert _close(rise, 5, 35, 41)
    assert _close(set_, 19, 48, 16)


def test_solar_noon_between_rise_and_set() -> None:
    date = GregorianDate(2026, 6, 26)
    rise = sunrise(date, NEW_YORK)
    noon = solar_noon(date, NEW_YORK)
    set_ = sunset(date, NEW_YORK)
    assert rise is not None and set_ is not None
    assert rise < noon < set_
    # Solar noon is (within a second or two) the midpoint of rise and set.
    midpoint = rise + (set_ - rise) / 2
    assert abs((noon - midpoint).total_seconds()) <= 60


def test_polar_no_event_returns_none() -> None:
    # Near the North Pole at the June solstice the sun never sets.
    date = GregorianDate(2026, 6, 21)
    assert sunrise(date, NORTH_POLE) is None
    assert sunset(date, NORTH_POLE) is None
