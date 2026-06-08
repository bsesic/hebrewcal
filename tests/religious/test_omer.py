"""Tests for the Omer count."""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.religious.omer import omer_count, omer_week_day


def test_first_and_last_day() -> None:
    assert omer_count(HebrewDate(5785, 1, 16)) == 1     # 16 Nisan = day 1
    assert omer_count(HebrewDate(5785, 3, 5)) == 49     # 5 Sivan = day 49


def test_outside_the_count() -> None:
    assert omer_count(HebrewDate(5785, 1, 15)) is None   # 15 Nisan, before
    assert omer_count(HebrewDate(5785, 3, 6)) is None    # 6 Sivan, Shavuot


def test_week_and_day_breakdown() -> None:
    # Lag BaOmer is day 33 = 4 weeks and 5 days.
    assert omer_count(HebrewDate(5785, 2, 18)) == 33
    assert omer_week_day(HebrewDate(5785, 2, 18)) == (4, 5)
