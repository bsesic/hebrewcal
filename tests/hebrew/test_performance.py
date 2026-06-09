"""Tests for the memoisation of hot year-keyed helpers."""

from __future__ import annotations

from hebrewcal.hebrew.molad import calendar_elapsed_days
from hebrewcal.hebrew.yeartype import new_year_rd


def test_new_year_rd_is_cached() -> None:
    new_year_rd.cache_clear()
    new_year_rd(5785)
    new_year_rd(5785)
    info = new_year_rd.cache_info()
    assert info.hits >= 1


def test_calendar_elapsed_days_is_cached() -> None:
    calendar_elapsed_days.cache_clear()
    calendar_elapsed_days(5785)
    calendar_elapsed_days(5785)
    assert calendar_elapsed_days.cache_info().hits >= 1


def test_values_unchanged_by_caching() -> None:
    # Caching must not change results.
    assert new_year_rd(5785) == 739162
    assert new_year_rd(5786) - new_year_rd(5785) == 355  # year length
