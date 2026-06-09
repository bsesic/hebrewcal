"""Render dates in numeric and named output formats."""

from __future__ import annotations

from typing import Literal

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.names import hebrew_month_name
from hebrewcal.numerals import to_hebrew_numeral

GregorianStyle = Literal["iso", "din"]
HebrewStyle = Literal["named", "numeric", "hebrew"]


def format_gregorian(date: GregorianDate, style: GregorianStyle = "iso") -> str:
    """Format a Gregorian date as ISO 8601 or DIN 5008."""
    if style == "iso":
        return f"{date.year:04d}-{date.month:02d}-{date.day:02d}"
    if style == "din":
        return f"{date.day:02d}.{date.month:02d}.{date.year:04d}"
    raise ValueError(f"unknown style: {style!r}")


def format_hebrew(date: HebrewDate, style: HebrewStyle = "named") -> str:
    """Format a Hebrew date.

    Styles: ``"numeric"`` (e.g. ``5785-07-01``), ``"named"`` (transliterated month
    name, e.g. ``1 Tishri 5785``), or ``"hebrew"`` (native Hebrew script with the
    day and year as gematria numerals, e.g. ``א׳ תשרי ה׳תשפ״ה``).
    """
    if style == "numeric":
        return f"{date.year}-{date.month:02d}-{date.day:02d}"
    if style == "named":
        name = hebrew_month_name(date.year, date.month, system="transliteration")
        return f"{date.day} {name} {date.year}"
    if style == "hebrew":
        name = hebrew_month_name(date.year, date.month, system="hebrew")
        return f"{to_hebrew_numeral(date.day)} {name} {to_hebrew_numeral(date.year)}"
    raise ValueError(f"unknown style: {style!r}")
