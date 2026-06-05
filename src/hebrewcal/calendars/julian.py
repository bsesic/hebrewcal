"""The proleptic Julian calendar with explicit reform handling.

The library never performs a silent Julian/Gregorian switch. Everything is
computed through RD; the historical 1582 (and later, regional) reform is exposed
as an explicit, configurable helper so callers decide when the cutover applies.
"""

from __future__ import annotations

from dataclasses import dataclass

from hebrewcal.calendars.gregorian import GregorianDate

# RD of Julian 1 January 1 == Gregorian 30 December 0 == -1.
JULIAN_EPOCH: int = -1

_MONTH_LENGTHS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def is_leap_year(year: int) -> bool:
    """Return whether ``year`` is a Julian leap year (proleptic, no year 0)."""
    if year > 0:
        return year % 4 == 0
    # There is no year 0; proleptically, leap years satisfy year % 4 == 3.
    return year % 4 == 3


def last_day_of_month(year: int, month: int) -> int:
    """Return the number of days in ``month`` of ``year``."""
    if month == 2 and is_leap_year(year):
        return 29
    return _MONTH_LENGTHS[month - 1]


@dataclass(frozen=True, order=True)
class JulianDate:
    """A date in the proleptic Julian calendar."""

    year: int
    month: int
    day: int

    def __post_init__(self) -> None:
        if self.year == 0:
            raise ValueError("Julian calendar has no year 0")
        if not 1 <= self.month <= 12:
            raise ValueError(f"month out of range: {self.month}")
        if not 1 <= self.day <= last_day_of_month(self.year, self.month):
            raise ValueError(f"day out of range: {self.day}")

    def to_rd(self) -> int:
        """Return the Rata Die day count for this date."""
        y = self.year + 1 if self.year < 0 else self.year
        if self.month <= 2:
            correction = 0
        elif is_leap_year(self.year):
            correction = -1
        else:
            correction = -2
        return (
            JULIAN_EPOCH
            - 1
            + 365 * (y - 1)
            + (y - 1) // 4
            + (367 * self.month - 362) // 12
            + correction
            + self.day
        )

    @classmethod
    def from_rd(cls, rd: int) -> JulianDate:
        """Reconstruct a Julian date from an RD value."""
        approx = (4 * (rd - JULIAN_EPOCH) + 1464) // 1461
        year = approx - 1 if approx <= 0 else approx
        prior_days = rd - cls(year, 1, 1).to_rd()
        if rd < cls(year, 3, 1).to_rd():
            correction = 0
        elif is_leap_year(year):
            correction = 1
        else:
            correction = 2
        month = (12 * (prior_days + correction) + 373) // 367
        day = rd - cls(year, month, 1).to_rd() + 1
        return cls(year, month, day)


def last_gregorian_before_reform() -> GregorianDate:
    """Return the last Gregorian-labelled date before the 1582 papal cutover.

    The papal bull skipped from Julian Thursday 4 October 1582 to Gregorian
    Friday 15 October 1582. Adoption was regional and much later in many places;
    callers that need a different cutover should supply their own date. This
    helper exists so the default reference point is explicit, not implicit.
    """
    return GregorianDate(1582, 10, 4)
