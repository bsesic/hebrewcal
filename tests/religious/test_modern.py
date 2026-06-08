"""Tests for the modern Israeli days and their adjustment rules."""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.religious.holidays import holidays_on


def _names(year: int, m: int, d: int) -> set[str]:
    return {h.name for h in holidays_on(HebrewDate(year, m, d))}


def test_5784_monday_rule() -> None:
    # 5 Iyyar 5784 is Monday: Zikaron 5 Iyyar, Atzmaut 6 Iyyar; Shoah 28 Nisan.
    assert "Yom HaShoah" in _names(5784, 1, 28)
    assert "Yom HaZikaron" in _names(5784, 2, 5)
    assert "Yom HaAtzmaut" in _names(5784, 2, 6)


def test_5785_friday_saturday_rule() -> None:
    # 5 Iyyar 5785 is Saturday: Atzmaut Thursday 3 Iyyar, Zikaron Wednesday 2 Iyyar;
    # 27 Nisan is Friday so Shoah moves to 26 Nisan.
    assert "Yom HaShoah" in _names(5785, 1, 26)
    assert "Yom HaZikaron" in _names(5785, 2, 2)
    assert "Yom HaAtzmaut" in _names(5785, 2, 3)


def test_5786_no_adjustment() -> None:
    # 5 Iyyar 5786 is Wednesday: default placement; 27 Nisan Tuesday (no move).
    assert "Yom HaShoah" in _names(5786, 1, 27)
    assert "Yom HaZikaron" in _names(5786, 2, 4)
    assert "Yom HaAtzmaut" in _names(5786, 2, 5)


def test_yom_yerushalayim_fixed() -> None:
    assert "Yom Yerushalayim" in _names(5785, 2, 28)
