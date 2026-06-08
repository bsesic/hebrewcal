"""Tests for the minor festivals."""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.religious.holidays import holidays_on


def _names(year: int, m: int, d: int) -> set[str]:
    return {h.name for h in holidays_on(HebrewDate(year, m, d))}


def test_hanukkah_eight_days_common_year() -> None:
    # 5785: 25 Kislev .. 2 Tevet (Kislev is 30 days).
    assert "Hanukkah" in _names(5785, 9, 25)
    assert "Hanukkah" in _names(5785, 10, 2)


def test_purim_common_year() -> None:
    assert "Purim" in _names(5785, 12, 14)
    assert "Shushan Purim" in _names(5785, 12, 15)


def test_purim_leap_year_in_adar_ii() -> None:
    assert "Purim" in _names(5784, 13, 14)
    assert "Purim Katan" in _names(5784, 12, 14)


def test_other_minor_days() -> None:
    assert "Tu BiShvat" in _names(5785, 11, 15)
    assert "Pesach Sheni" in _names(5785, 2, 14)
    assert "Lag BaOmer" in _names(5785, 2, 18)
    assert "Tu B'Av" in _names(5785, 5, 15)
