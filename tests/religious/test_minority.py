"""Tests for minority / communal feasts."""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.religious.holidays import Category, holidays_on


def test_sigd() -> None:
    # Sigd: 29 Marheshvan (50 days after Yom Kippur), Ethiopian Jewry.
    found = holidays_on(HebrewDate(5785, 8, 29))
    assert any(h.name == "Sigd" and h.category is Category.MINORITY for h in found)


def test_mimouna() -> None:
    # Mimouna: the day after Pesach, 22 Nisan.
    found = holidays_on(HebrewDate(5785, 1, 22))
    assert any(h.name == "Mimouna" for h in found)
