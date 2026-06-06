"""Tests for month and weekday name tables."""

from __future__ import annotations

import pytest

from hebrewcal.names import hebrew_month_name, weekday_name


def test_standard_month_names() -> None:
    assert hebrew_month_name(5785, 7, system="transliteration") == "Tishri"
    assert hebrew_month_name(5785, 1, system="transliteration") == "Nisan"


def test_leap_year_adar_naming() -> None:
    # Month 12 in a leap year is Adar I; month 13 is Adar II.
    assert hebrew_month_name(5784, 12, system="transliteration") == "Adar I"
    assert hebrew_month_name(5784, 13, system="transliteration") == "Adar II"
    # In a common year month 12 is simply Adar.
    assert hebrew_month_name(5785, 12, system="transliteration") == "Adar"


def test_babylonian_and_biblical_systems() -> None:
    # Babylonian name of Tishri is Tashritu; a biblical name of Nisan is Aviv.
    assert hebrew_month_name(5785, 7, system="babylonian") == "Tashritu"
    assert hebrew_month_name(5785, 1, system="biblical") == "Aviv"


def test_weekday_names() -> None:
    # 0 = Sunday ... 6 = Saturday.
    assert weekday_name(0) == "Yom Rishon"
    assert weekday_name(1) == "Yom Sheni"
    assert weekday_name(6) == "Shabbat"


def test_unknown_system_rejected() -> None:
    with pytest.raises(ValueError):
        hebrew_month_name(5785, 7, system="klingon")  # type: ignore[arg-type]
