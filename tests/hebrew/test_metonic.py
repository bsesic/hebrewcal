"""Tests for the 19-year Metonic cycle."""

from __future__ import annotations

from hebrewcal.hebrew.metonic import is_leap_year, months_in_year


def test_known_leap_years() -> None:
    # Verified with the rule: a year is leap iff (7*y + 1) % 19 < 7.
    assert is_leap_year(5782) is True
    assert is_leap_year(5784) is True
    assert is_leap_year(5787) is True
    assert is_leap_year(5783) is False
    assert is_leap_year(5785) is False
    assert is_leap_year(5786) is False


def test_leap_year_pattern_over_one_cycle() -> None:
    # Exactly 7 leap years occur in any 19 consecutive years.
    leaps = [y for y in range(5701, 5720) if is_leap_year(y)]
    assert len(leaps) == 7


def test_months_in_year() -> None:
    assert months_in_year(5784) == 13  # leap
    assert months_in_year(5785) == 12  # common
