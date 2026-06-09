"""Tests for the Qumran (364-day) calendar."""

from __future__ import annotations

import pytest

from hebrewcal.calendars_alt.qumran import QumranDate, days_in_year
from hebrewcal.core.rata_die import weekday_from_rd


def test_year_is_364_days() -> None:
    assert days_in_year() == 364


def test_round_trip() -> None:
    for rd in range(-50000, 50000, 13):
        assert QumranDate.from_rd(rd).to_rd() == rd


def test_new_year_always_same_weekday() -> None:
    weekdays = {weekday_from_rd(QumranDate(y, 1, 1).to_rd()) for y in range(1, 40)}
    assert len(weekdays) == 1  # every year starts on the same weekday


def test_month_lengths() -> None:
    # Months 3, 6, 9, 12 have 31 days; the rest have 30.
    assert QumranDate(5, 3, 31).month == 3
    with pytest.raises(ValueError):
        QumranDate(5, 1, 31)  # month 1 has only 30 days


def test_known_structure() -> None:
    d = QumranDate(1, 1, 1)
    assert d.to_rd() + 364 == QumranDate(2, 1, 1).to_rd()
