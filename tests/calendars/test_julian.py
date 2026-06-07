"""Tests for the proleptic Julian calendar and the reform helper."""

from __future__ import annotations

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars.julian import (
    JULIAN_EPOCH,
    JulianDate,
    is_leap_year,
    last_gregorian_before_reform,
)


def test_epoch_value() -> None:
    # Julian 1 Jan 1 sits one day before the Gregorian epoch.
    assert JULIAN_EPOCH == -1
    assert JulianDate(1, 1, 1).to_rd() == -1


def test_leap_year_rule_handles_no_year_zero() -> None:
    assert is_leap_year(4) is True
    assert is_leap_year(3) is False
    assert is_leap_year(1900) is True  # Julian: every 4th year is leap
    assert is_leap_year(-1) is True    # proleptic: year -1 is leap


def test_round_trip_including_proleptic() -> None:
    for rd in (-200000, -1, 0, 1, 700000, 739428):
        assert JulianDate.from_rd(rd).to_rd() == rd


def test_reform_offset_1582() -> None:
    # The 1582 reform: Julian Thursday 4 Oct 1582 was followed by
    # Gregorian Friday 15 Oct 1582 — consecutive RD values.
    julian_last = JulianDate(1582, 10, 4)
    gregorian_first = GregorianDate(1582, 10, 15)
    assert julian_last.to_rd() + 1 == gregorian_first.to_rd()


def test_reform_helper() -> None:
    assert last_gregorian_before_reform() == GregorianDate(1582, 10, 4)
