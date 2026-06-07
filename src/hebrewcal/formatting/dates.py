"""Render dates in numeric and named output formats."""

from __future__ import annotations

from typing import Literal

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.names import hebrew_month_name

GregorianStyle = Literal["iso", "din"]
HebrewStyle = Literal["named", "numeric"]


def format_gregorian(date: GregorianDate, style: GregorianStyle = "iso") -> str:
    """Format a Gregorian date as ISO 8601 or DIN 5008."""
    if style == "iso":
        return f"{date.year:04d}-{date.month:02d}-{date.day:02d}"
    if style == "din":
        return f"{date.day:02d}.{date.month:02d}.{date.year:04d}"
    raise ValueError(f"unknown style: {style!r}")


def format_hebrew(date: HebrewDate, style: HebrewStyle = "named") -> str:
    """Format a Hebrew date numerically or with a transliterated month name."""
    if style == "numeric":
        return f"{date.year}-{date.month:02d}-{date.day:02d}"
    if style == "named":
        name = hebrew_month_name(date.year, date.month, system="transliteration")
        return f"{date.day} {name} {date.year}"
    raise ValueError(f"unknown style: {style!r}")
