"""Tests for the major festivals."""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.religious.holidays import holidays_on


def _names(year: int, m: int, d: int, diaspora: bool) -> set[str]:
    return {h.name for h in holidays_on(HebrewDate(year, m, d), diaspora)}


def test_yom_kippur() -> None:
    assert "Yom Kippur" in _names(5785, 7, 10, True)


def test_simchat_torah_israel_vs_diaspora() -> None:
    # Israel: Simchat Torah on 22 Tishri (with Shemini Atzeret). Diaspora: 23 Tishri.
    assert "Simchat Torah" in _names(5785, 7, 22, False)   # Israel
    assert "Simchat Torah" not in _names(5785, 7, 22, True)  # Diaspora
    assert "Simchat Torah" in _names(5785, 7, 23, True)      # Diaspora


def test_pesach_eighth_day_diaspora_only() -> None:
    assert "Pesach" in _names(5785, 1, 22, True)    # 8th day, Diaspora
    assert "Pesach" not in _names(5785, 1, 22, False)  # Israel has 7 days


def test_shavuot_second_day_diaspora_only() -> None:
    assert "Shavuot" in _names(5785, 3, 7, True)
    assert "Shavuot" not in _names(5785, 3, 7, False)


def test_sukkot_and_shemini_atzeret() -> None:
    assert "Sukkot" in _names(5785, 7, 15, True)
    assert "Shemini Atzeret" in _names(5785, 7, 22, True)
