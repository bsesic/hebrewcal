"""Tests for new-year RD, year length and month lengths."""

from __future__ import annotations

from hebrewcal.hebrew.yeartype import (
    days_in_year,
    last_day_of_month,
    last_month_of_year,
    new_year_rd,
)


def test_new_year_strictly_increases() -> None:
    prev = new_year_rd(5700)
    for year in range(5701, 5760):
        cur = new_year_rd(year)
        assert cur > prev
        prev = cur


def test_year_lengths_are_valid() -> None:
    # Common years: 353/354/355; leap years: 383/384/385.
    for year in range(5700, 5800):
        length = days_in_year(year)
        assert length in (353, 354, 355, 383, 384, 385)


def test_last_month_of_year() -> None:
    assert last_month_of_year(5784) == 13  # leap
    assert last_month_of_year(5785) == 12  # common


def test_tishri_and_nisan_lengths() -> None:
    # Tishri (7) always 30, Nisan (1) always 30, Iyyar (2) always 29.
    assert last_day_of_month(5785, 7) == 30
    assert last_day_of_month(5785, 1) == 30
    assert last_day_of_month(5785, 2) == 29
