"""Tests for twilight (dawn and dusk) at the standard depression angles."""

from __future__ import annotations

from hebrewcal.astro.location import Location
from hebrewcal.astro.solar import (
    ASTRONOMICAL_DEPRESSION,
    CIVIL_DEPRESSION,
    NAUTICAL_DEPRESSION,
    dawn,
    dusk,
    sunrise,
    sunset,
)
from hebrewcal.calendars.gregorian import GregorianDate

NEW_YORK = Location(40.7128, -74.0060, timezone="America/New_York")


def test_depression_constants() -> None:
    assert CIVIL_DEPRESSION == 6.0
    assert NAUTICAL_DEPRESSION == 12.0
    assert ASTRONOMICAL_DEPRESSION == 18.0


def test_dawn_ordering() -> None:
    # Morning order: astronomical dawn < nautical < civil < sunrise.
    date = GregorianDate(2026, 6, 26)
    astro = dawn(date, NEW_YORK, ASTRONOMICAL_DEPRESSION)
    naut = dawn(date, NEW_YORK, NAUTICAL_DEPRESSION)
    civil = dawn(date, NEW_YORK, CIVIL_DEPRESSION)
    rise = sunrise(date, NEW_YORK)
    assert astro is not None and naut is not None and civil is not None and rise is not None
    assert astro < naut < civil < rise


def test_dusk_ordering() -> None:
    # Evening order: sunset < civil dusk < nautical < astronomical.
    date = GregorianDate(2026, 6, 26)
    set_ = sunset(date, NEW_YORK)
    civil = dusk(date, NEW_YORK, CIVIL_DEPRESSION)
    naut = dusk(date, NEW_YORK, NAUTICAL_DEPRESSION)
    astro = dusk(date, NEW_YORK, ASTRONOMICAL_DEPRESSION)
    assert set_ is not None and civil is not None and naut is not None and astro is not None
    assert set_ < civil < naut < astro


def test_default_dawn_is_civil() -> None:
    date = GregorianDate(2026, 6, 26)
    assert dawn(date, NEW_YORK) == dawn(date, NEW_YORK, CIVIL_DEPRESSION)
