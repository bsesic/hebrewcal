"""Astronomical time base: Julian Day and Julian centuries.

The Julian Day is derived from the library's Rata Die day count, which keeps the
astronomy layer exactly consistent with the calendar core:

    JD(00:00 UTC) = RD + 1721424.5

so RD 1 (proleptic Gregorian 0001-01-01) is JD 1721425.5 at midnight.
"""

from __future__ import annotations

from hebrewcal.calendars.gregorian import GregorianDate

# Julian Day of the J2000.0 epoch (2000-01-01 12:00).
J2000: float = 2451545.0

# Offset from the Rata Die count to the Julian Day at 00:00.
_RD_TO_JD: float = 1721424.5


def julian_day_from_rd(rd: int, day_fraction: float = 0.0) -> float:
    """Return the Julian Day for an RD value plus a fraction of a day."""
    return rd + _RD_TO_JD + day_fraction


def julian_day(year: int, month: int, day: int, day_fraction: float = 0.0) -> float:
    """Return the Julian Day for a proleptic Gregorian date plus a day fraction."""
    return julian_day_from_rd(GregorianDate(year, month, day).to_rd(), day_fraction)


def julian_centuries(jd: float) -> float:
    """Return Julian centuries since J2000.0 for the given Julian Day."""
    return (jd - J2000) / 36525.0
