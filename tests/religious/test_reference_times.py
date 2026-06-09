"""Cross-checked reference values and invariants for the religious times."""

from __future__ import annotations

import datetime

import pytest

from hebrewcal.astro.location import Location
from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.religious.sabbatical import is_shmita
from hebrewcal.religious.shabbat import candle_lighting, havdalah
from hebrewcal.religious.torah import parasha

NEW_YORK = Location(40.7128, -74.0060, timezone="America/New_York")


def test_candle_lighting_new_york_reference() -> None:
    # Friday 2026-06-26: sunset ~20:31, candle lighting ~20:13.
    cl = candle_lighting(GregorianDate(2026, 6, 26), NEW_YORK)
    assert cl is not None
    expected = cl.replace(hour=20, minute=13, second=0, microsecond=0)
    assert abs(cl - expected) <= datetime.timedelta(minutes=2)


def test_havdalah_after_candle_lighting() -> None:
    cl = candle_lighting(GregorianDate(2026, 6, 26), NEW_YORK)
    hv = havdalah(GregorianDate(2026, 6, 27), NEW_YORK)
    assert cl is not None and hv is not None
    assert hv > cl


@pytest.mark.parametrize(
    "m,d,name",
    [(7, 24, "Bereshit"), (8, 1, "Noach"), (8, 8, "Lech-Lecha")],
)
def test_torah_reference_diaspora_5785(m: int, d: int, name: str) -> None:
    assert parasha(HebrewDate(5785, m, d)) == name


def test_shmita_anchor() -> None:
    assert is_shmita(5782) and is_shmita(5789)
    assert not is_shmita(5785)
