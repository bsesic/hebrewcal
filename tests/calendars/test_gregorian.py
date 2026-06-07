"""Tests for the proleptic Gregorian calendar."""

from __future__ import annotations

import datetime

from hebrewcal.calendars.gregorian import GregorianDate, is_leap_year


def test_epoch_round_trip() -> None:
    assert GregorianDate(1, 1, 1).to_rd() == 1
    assert GregorianDate.from_rd(1) == GregorianDate(1, 1, 1)


def test_known_rd_values() -> None:
    # Reference values cross-checked against datetime.date.toordinal().
    assert GregorianDate(1945, 11, 12).to_rd() == 710347
    assert GregorianDate(2026, 6, 26).to_rd() == 739793


def test_leap_year_rule() -> None:
    assert is_leap_year(2000) is True
    assert is_leap_year(1900) is False
    assert is_leap_year(2024) is True
    assert is_leap_year(2023) is False


def test_proleptic_negative_years() -> None:
    # Round trips must hold for years <= 0 (proleptic).
    for rd in (-100000, -365, 0, 1, 1000, 739428):
        assert GregorianDate.from_rd(rd).to_rd() == rd


def test_matches_stdlib_for_modern_dates() -> None:
    # The stdlib proleptic Gregorian ordinal equals RD.
    for ord_ in (1, 100000, 700000, 739428):
        d = datetime.date.fromordinal(ord_)
        g = GregorianDate(d.year, d.month, d.day)
        assert g.to_rd() == ord_
        assert GregorianDate.from_rd(ord_) == g
