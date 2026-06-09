"""Tests for candle lighting and Havdalah."""

from __future__ import annotations

import datetime

from hebrewcal.astro.location import Location
from hebrewcal.astro.solar import sunset
from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.religious.shabbat import candle_lighting, havdalah

NEW_YORK = Location(40.7128, -74.0060, timezone="America/New_York")


def test_candle_lighting_default_offset() -> None:
    date = GregorianDate(2026, 6, 26)  # a Friday
    cl = candle_lighting(date, NEW_YORK)
    ss = sunset(date, NEW_YORK)
    assert cl is not None and ss is not None
    assert abs((ss - cl) - datetime.timedelta(minutes=18)).total_seconds() < 1


def test_candle_lighting_custom_offset() -> None:
    date = GregorianDate(2026, 6, 26)
    cl = candle_lighting(date, NEW_YORK, minutes_before_sunset=40)
    cl18 = candle_lighting(date, NEW_YORK)
    assert cl is not None and cl18 is not None
    assert abs((cl18 - cl) - datetime.timedelta(minutes=22)).total_seconds() < 1


def test_havdalah_after_sunset() -> None:
    date = GregorianDate(2026, 6, 27)  # Saturday
    hv = havdalah(date, NEW_YORK)
    ss = sunset(date, NEW_YORK)
    assert hv is not None and ss is not None
    assert hv > ss


def test_havdalah_fixed_minutes() -> None:
    date = GregorianDate(2026, 6, 27)
    hv = havdalah(date, NEW_YORK, minutes_after_sunset=72)
    ss = sunset(date, NEW_YORK)
    assert hv is not None and ss is not None
    assert abs((hv - ss) - datetime.timedelta(minutes=72)).total_seconds() < 1
