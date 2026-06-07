"""Tests for the Anno Mundi era helpers."""

from __future__ import annotations

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.conversion import to_hebrew
from hebrewcal.eras.anno_mundi import (
    MISSING_YEARS_NOTICE,
    anno_mundi_year,
    traditional_vs_academic_gap,
)


def test_am_year_is_hebrew_year() -> None:
    # AM year is simply the Hebrew year number.
    h = HebrewDate(5785, 7, 1)
    assert anno_mundi_year(h) == 5785


def test_missing_years_gap_constant() -> None:
    # The traditional reckoning is ~165 years short for the Persian period.
    assert traditional_vs_academic_gap() == 165


def test_notice_is_nonempty_and_documented() -> None:
    assert isinstance(MISSING_YEARS_NOTICE, str)
    assert "missing years" in MISSING_YEARS_NOTICE.lower()


def test_known_modern_correspondence() -> None:
    g = GregorianDate(2024, 10, 3)
    assert anno_mundi_year(to_hebrew(g)) == 5785
