"""Tests for the special Shabbatot."""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.core.rata_die import weekday_from_rd
from hebrewcal.religious.holidays import Category, holidays


def _specials(year: int) -> dict[str, int]:
    return {
        h.name: h.date.to_rd()
        for h in holidays(year)
        if h.category is Category.SPECIAL_SHABBAT
    }


def test_all_on_saturday() -> None:
    for rd in _specials(5785).values():
        assert weekday_from_rd(rd) == 6  # Saturday


def test_expected_set_present() -> None:
    names = set(_specials(5785))
    for name in (
        "Shabbat Shekalim",
        "Shabbat Zachor",
        "Shabbat Parah",
        "Shabbat HaChodesh",
        "Shabbat HaGadol",
        "Shabbat Shuvah",
        "Shabbat Chazon",
        "Shabbat Nachamu",
    ):
        assert name in names


def test_hagadol_is_before_pesach() -> None:
    specials = _specials(5785)
    assert specials["Shabbat HaGadol"] < HebrewDate(5785, 1, 15).to_rd()
    assert HebrewDate(5785, 1, 15).to_rd() - specials["Shabbat HaGadol"] <= 7
