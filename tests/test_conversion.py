"""Tests for the high-level conversion API, including the roadmap acceptance case."""

from __future__ import annotations

import hebrewcal
from hebrewcal import (
    GregorianDate,
    HebrewDate,
    Weekday,
    to_gregorian,
    to_hebrew,
    to_julian,
    weekday,
)


def test_public_exports_exist() -> None:
    for name in (
        "GregorianDate",
        "JulianDate",
        "HebrewDate",
        "Weekday",
        "to_gregorian",
        "to_hebrew",
        "to_julian",
        "weekday",
    ):
        assert hasattr(hebrewcal, name)


def test_acceptance_1867_10_31() -> None:
    # "What Hebrew date and weekday corresponds to 1867-10-31?"
    g = GregorianDate(1867, 10, 31)
    h = to_hebrew(g)
    assert (h.year, h.month, h.day) == (5628, 8, 2)  # 2 Marheshvan 5628
    assert weekday(g) is Weekday.THURSDAY


def test_gregorian_julian_round_trip() -> None:
    g = GregorianDate(2026, 6, 26)
    j = to_julian(g)
    assert to_gregorian(j) == g


def test_hebrew_gregorian_round_trip() -> None:
    h = HebrewDate(5785, 7, 1)
    g = to_gregorian(h)
    assert to_hebrew(g) == h
