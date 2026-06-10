"""Tests for the elevation horizon-dip correction."""

from __future__ import annotations

from hebrewcal.astro.location import Location
from hebrewcal.astro.solar import elevation_depression, sunrise, sunset
from hebrewcal.calendars.gregorian import GregorianDate

JERUSALEM = Location(31.7683, 35.2137, elevation=754.0, timezone="Asia/Jerusalem")
SEA_LEVEL = Location(31.7683, 35.2137, elevation=0.0, timezone="Asia/Jerusalem")


def test_dip_formula() -> None:
    assert elevation_depression(0.0) == 0.0
    assert elevation_depression(-5.0) == 0.0
    # 754 m gives about 0.88 degrees of dip (KosherJava geometric formula).
    assert abs(elevation_depression(754.0) - 0.8824) < 0.001


def test_elevation_shifts_sunrise_earlier_and_sunset_later() -> None:
    date = GregorianDate(2026, 6, 26)
    sr_sea = sunrise(date, SEA_LEVEL)
    sr_elev = sunrise(date, JERUSALEM, elevation=True)
    ss_sea = sunset(date, SEA_LEVEL)
    ss_elev = sunset(date, JERUSALEM, elevation=True)
    assert sr_sea is not None and sr_elev is not None
    assert ss_sea is not None and ss_elev is not None
    assert sr_elev < sr_sea          # sunrise earlier at elevation
    assert ss_elev > ss_sea          # sunset later at elevation
    # Default (no elevation flag) ignores elevation.
    assert sunrise(date, JERUSALEM) == sr_sea
