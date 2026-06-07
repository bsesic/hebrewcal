"""Tests for date formatting."""

from __future__ import annotations

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.formatting.dates import format_gregorian, format_hebrew


def test_iso_format() -> None:
    assert format_gregorian(GregorianDate(2026, 6, 26), style="iso") == "2026-06-26"


def test_din_format() -> None:
    assert format_gregorian(GregorianDate(2026, 6, 26), style="din") == "26.06.2026"


def test_hebrew_named_format() -> None:
    # 1 Tishri 5785 with standard transliterated month name.
    text = format_hebrew(HebrewDate(5785, 7, 1), style="named")
    assert "Tishri" in text
    assert "5785" in text


def test_hebrew_leap_month_naming() -> None:
    # Month 12 in a leap year is "Adar I", month 13 is "Adar II".
    assert "Adar I" in format_hebrew(HebrewDate(5784, 12, 1), style="named")
    assert "Adar II" in format_hebrew(HebrewDate(5784, 13, 1), style="named")
