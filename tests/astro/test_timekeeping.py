"""Tests for the Julian Day time base."""

from __future__ import annotations

from hebrewcal.astro.timekeeping import (
    J2000,
    julian_centuries,
    julian_day,
    julian_day_from_rd,
)
from hebrewcal.calendars.gregorian import GregorianDate


def test_j2000_epoch() -> None:
    # J2000.0 is 2000-01-01 12:00 TT ~ JD 2451545.0.
    assert julian_day(2000, 1, 1, 0.5) == J2000
    assert J2000 == 2451545.0


def test_jd_from_rd_matches_gregorian() -> None:
    rd = GregorianDate(2000, 1, 1).to_rd()
    assert julian_day_from_rd(rd, 0.5) == julian_day(2000, 1, 1, 0.5)


def test_jd_at_midnight() -> None:
    # JD of proleptic Gregorian 0001-01-01 00:00 is 1721425.5; RD of that date is 1.
    assert julian_day(1, 1, 1, 0.0) == 1721425.5


def test_julian_centuries_zero_at_j2000() -> None:
    assert julian_centuries(J2000) == 0.0
    assert julian_centuries(J2000 + 36525.0) == 1.0
