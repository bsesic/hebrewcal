"""Tests for the Hebrew date type and its RD conversion."""

from __future__ import annotations

import pytest

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars.hebrew import HebrewDate


def test_round_trip_over_many_years() -> None:
    # Every day of several years must round-trip through RD.
    start = HebrewDate(5780, 7, 1).to_rd()
    end = HebrewDate(5790, 7, 1).to_rd()
    for rd in range(start, end):
        assert HebrewDate.from_rd(rd).to_rd() == rd


def test_known_correspondence() -> None:
    # 1 Tishri 5785 corresponds to 3 October 2024 (Gregorian).
    rd = HebrewDate(5785, 7, 1).to_rd()
    assert GregorianDate.from_rd(rd) == GregorianDate(2024, 10, 3)


def test_leap_year_has_adar_ii() -> None:
    # 5784 is a leap year: month 13 (Adar II) exists and follows Adar I (12).
    assert HebrewDate(5784, 13, 1).to_rd() > HebrewDate(5784, 12, 1).to_rd()


def test_invalid_day_rejected() -> None:
    with pytest.raises(ValueError):
        HebrewDate(5785, 2, 30)  # Iyyar has 29 days
