"""Tests for native Hebrew-script names and date formatting."""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.formatting.dates import format_hebrew
from hebrewcal.names import hebrew_month_name, weekday_name


def test_hebrew_month_names() -> None:
    assert hebrew_month_name(5785, 7, system="hebrew") == "תשרי"
    assert hebrew_month_name(5785, 1, system="hebrew") == "ניסן"
    assert hebrew_month_name(5785, 9, system="hebrew") == "כסלו"


def test_hebrew_adar_naming() -> None:
    # Common year: plain Adar. Leap year: Adar I (month 12) and Adar II (month 13).
    assert hebrew_month_name(5785, 12, system="hebrew") == "אדר"
    assert hebrew_month_name(5784, 12, system="hebrew") == "אדר א׳"
    assert hebrew_month_name(5784, 13, system="hebrew") == "אדר ב׳"


def test_hebrew_weekday_names() -> None:
    assert weekday_name(0, hebrew=True) == "יום ראשון"
    assert weekday_name(6, hebrew=True) == "שבת"
    # Default is still the transliteration.
    assert weekday_name(0) == "Yom Rishon"


def test_format_hebrew_script() -> None:
    # 1 Tishri 5785 with the day and year as gematria numerals.
    assert format_hebrew(HebrewDate(5785, 7, 1), style="hebrew") == "א׳ תשרי ה׳תשפ״ה"
    # 15 Adar II 5784 (leap year).
    assert format_hebrew(HebrewDate(5784, 13, 15), style="hebrew") == "ט״ו אדר ב׳ ה׳תשפ״ד"


def test_other_styles_unchanged() -> None:
    assert format_hebrew(HebrewDate(5785, 7, 1), style="named") == "1 Tishri 5785"
    assert format_hebrew(HebrewDate(5785, 7, 1), style="numeric") == "5785-07-01"
