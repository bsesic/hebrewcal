"""Tests for the holiday model, engine and Rosh Chodesh."""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.religious.holidays import Category, Holiday, holidays, holidays_on, rosh_chodesh


def test_holiday_is_frozen_and_typed() -> None:
    h = Holiday("Test", HebrewDate(5785, 7, 1), Category.MAJOR_FESTIVAL)
    assert h.name == "Test"
    assert h.date == HebrewDate(5785, 7, 1)
    assert h.category is Category.MAJOR_FESTIVAL


def test_rosh_chodesh_two_days_when_prev_month_long() -> None:
    # Kislev 5785 has 30 days, so Rosh Chodesh Tevet is 30 Kislev + 1 Tevet.
    names = {(h.date.month, h.date.day) for h in rosh_chodesh(5785)}
    assert (9, 30) in names  # 30 Kislev
    assert (10, 1) in names  # 1 Tevet


def test_rosh_chodesh_excludes_tishri() -> None:
    # 1 Tishri is Rosh Hashanah, never labelled Rosh Chodesh.
    assert all(not (h.date.month == 7 and h.date.day == 1) for h in rosh_chodesh(5785))


def test_holidays_sorted_chronologically() -> None:
    days = holidays(5785)
    rds = [h.date.to_rd() for h in days]
    assert rds == sorted(rds)


def test_holidays_on_returns_matches() -> None:
    found = holidays_on(HebrewDate(5785, 7, 1))
    assert any(h.name == "Rosh Hashanah" for h in found)
