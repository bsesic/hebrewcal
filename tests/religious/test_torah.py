"""Tests for the Torah-reading schedule."""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.religious.torah import parasha, triennial_portion


def _safe_saturday(year: int, m: int, d: int) -> bool:
    try:
        date = HebrewDate(year, m, d)
    except ValueError:
        return False
    return date.to_rd() % 7 == 6


def test_known_readings_diaspora_5785() -> None:
    # 24 Tishri 5785 (Sat) is Bereshit; 1 Marheshvan is Noach.
    assert parasha(HebrewDate(5785, 7, 24)) == "Bereshit"
    assert parasha(HebrewDate(5785, 8, 1)) == "Noach"


def test_festival_shabbat_has_no_parasha() -> None:
    # 17 Tishri 5785 is Shabbat Chol HaMoed Sukkot: no weekly parasha.
    assert parasha(HebrewDate(5785, 7, 17)) is None


def test_non_saturday_returns_none() -> None:
    # 25 Tishri 5785 is a Sunday.
    assert parasha(HebrewDate(5785, 7, 25)) is None


def test_combined_parasha() -> None:
    found = {
        parasha(HebrewDate(5785, m, d))
        for m in range(1, 13)
        for d in range(1, 31)
        if _safe_saturday(5785, m, d)
    }
    assert "Matot-Masei" in found


def test_triennial_portion_is_1_2_or_3() -> None:
    assert triennial_portion(HebrewDate(5785, 7, 24)) in (1, 2, 3)
