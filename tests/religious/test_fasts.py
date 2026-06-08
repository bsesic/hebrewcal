"""Tests for the public fasts and their postponement rules."""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.religious.holidays import holidays_on


def _names(year: int, m: int, d: int) -> set[str]:
    return {h.name for h in holidays_on(HebrewDate(year, m, d))}


def test_tzom_gedaliah_postponed_when_on_shabbat() -> None:
    # 5785: 3 Tishri is Shabbat, so the fast is on 4 Tishri.
    assert "Tzom Gedaliah" in _names(5785, 7, 4)
    assert "Tzom Gedaliah" not in _names(5785, 7, 3)


def test_tisha_bav_postponed() -> None:
    # 5782: 9 Av is Shabbat, observed on 10 Av.
    assert "Tisha B'Av" in _names(5782, 5, 10)
    assert "Tisha B'Av" not in _names(5782, 5, 9)


def test_taanit_esther_moved_when_13_adar_is_shabbat() -> None:
    # 5784 (leap): 13 Adar II is Shabbat, so Ta'anit Esther is on 11 Adar II (Thursday).
    assert "Ta'anit Esther" in _names(5784, 13, 11)


def test_asara_btevet() -> None:
    assert "Asara B'Tevet" in _names(5785, 10, 10)
