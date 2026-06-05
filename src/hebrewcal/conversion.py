"""High-level, ergonomic conversion between the supported calendars.

Every function routes through RD via :func:`hebrewcal.core.calendar.convert`.
"""

from __future__ import annotations

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.calendars.julian import JulianDate
from hebrewcal.core.calendar import CalendarDate, Weekday, convert
from hebrewcal.core.calendar import weekday as _weekday


def to_gregorian(date: CalendarDate) -> GregorianDate:
    """Convert any supported date to a Gregorian date."""
    return convert(date, GregorianDate)


def to_julian(date: CalendarDate) -> JulianDate:
    """Convert any supported date to a Julian date."""
    return convert(date, JulianDate)


def to_hebrew(date: CalendarDate) -> HebrewDate:
    """Convert any supported date to a Hebrew date."""
    return convert(date, HebrewDate)


def weekday(date: CalendarDate) -> Weekday:
    """Return the weekday of any supported date."""
    return _weekday(date)
