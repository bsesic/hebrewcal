"""Tests for the curated public API surface of the subpackages."""

from __future__ import annotations

import hebrewcal.astro as astro
import hebrewcal.calendars_alt as calendars_alt
import hebrewcal.religious as religious


def test_astro_exports() -> None:
    for name in (
        "Location",
        "sunrise",
        "sunset",
        "solar_noon",
        "dawn",
        "dusk",
        "solar_declination",
        "equation_of_time",
        "molad_moment",
        "nth_new_moon",
        "new_moon_at_or_after",
    ):
        assert hasattr(astro, name), name


def test_religious_exports() -> None:
    for name in (
        "Holiday",
        "Category",
        "holidays",
        "holidays_on",
        "omer_count",
        "candle_lighting",
        "havdalah",
        "Zmanim",
        "month_announcement",
        "yahrzeit",
        "parasha",
        "is_shmita",
    ):
        assert hasattr(religious, name), name


def test_calendars_alt_exports() -> None:
    for name in ("QumranDate", "SamaritanDate", "KaraiteDate"):
        assert hasattr(calendars_alt, name), name


def test_all_lists_are_consistent() -> None:
    # Everything in __all__ must actually be importable.
    for module in (astro, religious, calendars_alt):
        for name in module.__all__:
            assert hasattr(module, name), f"{module.__name__}.{name}"
