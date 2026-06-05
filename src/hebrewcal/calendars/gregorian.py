"""The proleptic Gregorian calendar.

Valid for all years, including years <= 0 (proleptic). The RD value matches the
Python standard-library proleptic Gregorian ordinal, which makes cross-checking
straightforward.
"""

from __future__ import annotations

from dataclasses import dataclass

from hebrewcal.core.rata_die import RD_EPOCH

_MONTH_LENGTHS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def is_leap_year(year: int) -> bool:
    """Return whether ``year`` is a Gregorian leap year."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def last_day_of_month(year: int, month: int) -> int:
    """Return the number of days in ``month`` of ``year``."""
    if month == 2 and is_leap_year(year):
        return 29
    return _MONTH_LENGTHS[month - 1]


@dataclass(frozen=True, order=True)
class GregorianDate:
    """A date in the proleptic Gregorian calendar."""

    year: int
    month: int
    day: int

    def __post_init__(self) -> None:
        if not 1 <= self.month <= 12:
            raise ValueError(f"month out of range: {self.month}")
        if not 1 <= self.day <= last_day_of_month(self.year, self.month):
            raise ValueError(f"day out of range: {self.day}")

    def to_rd(self) -> int:
        """Return the Rata Die day count for this date."""
        y = self.year
        if self.month <= 2:
            correction = 0
        elif is_leap_year(y):
            correction = -1
        else:
            correction = -2
        return (
            RD_EPOCH
            - 1
            + 365 * (y - 1)
            + (y - 1) // 4
            - (y - 1) // 100
            + (y - 1) // 400
            + (367 * self.month - 362) // 12
            + correction
            + self.day
        )

    @classmethod
    def from_rd(cls, rd: int) -> GregorianDate:
        """Reconstruct a Gregorian date from an RD value."""
        year = _year_from_rd(rd)
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


def _year_from_rd(rd: int) -> int:
    """Return the Gregorian year containing the given RD value."""
    d0 = rd - RD_EPOCH
    n400, d1 = divmod(d0, 146097)
    n100, d2 = divmod(d1, 36524)
    n4, d3 = divmod(d2, 1461)
    n1 = d3 // 365
    year = 400 * n400 + 100 * n100 + 4 * n4 + n1
    if n100 == 4 or n1 == 4:
        return year
    return year + 1
