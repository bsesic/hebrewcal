"""The Qumran / Jubilees 364-day solar calendar.

The calendar found in the Dead Sea Scrolls and the Book of Jubilees has a fixed
364-day year: four quarters of 91 days, each quarter being three months of 30, 30
and 31 days (so months 3, 6, 9 and 12 have 31 days). Because 364 = 52 weeks
exactly, every year — and every festival — falls on the same weekday each year.
The calendar has no intercalation, so it drifts against the seasons over time.

The epoch is conventional: year 1, month 1, day 1 is anchored to the Wednesday on
or after the proleptic Gregorian March equinox of year 1 (the Jubilees New Year is
traditionally a Wednesday, the day the luminaries were created). Year numbering is
therefore nominal; the calendar's defining properties are its 364-day structure
and fixed weekday alignment, both of which are exact.
"""

from __future__ import annotations

from dataclasses import dataclass

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.core.rata_die import weekday_from_rd

_WEDNESDAY = 3
# Month lengths: 30, 30, 31 repeated for each of the four quarters.
_MONTH_LENGTHS = (30, 30, 31, 30, 30, 31, 30, 30, 31, 30, 30, 31)
_YEAR_LENGTH = sum(_MONTH_LENGTHS)  # 364


def _first_weekday_on_or_after(rd: int, weekday: int) -> int:
    return rd + (weekday - weekday_from_rd(rd)) % 7


# Conventional epoch: the Wednesday on or after the proleptic Gregorian March
# equinox of year 1.
QUMRAN_EPOCH: int = _first_weekday_on_or_after(GregorianDate(1, 3, 21).to_rd(), _WEDNESDAY)


def days_in_year() -> int:
    """Return the (constant) length of a Qumran year, 364 days."""
    return _YEAR_LENGTH


def last_day_of_month(month: int) -> int:
    """Return the number of days in ``month`` (30, or 31 for months 3, 6, 9, 12)."""
    return _MONTH_LENGTHS[month - 1]


@dataclass(frozen=True, order=True)
class QumranDate:
    """A date in the Qumran / Jubilees 364-day calendar."""

    year: int
    month: int
    day: int

    def __post_init__(self) -> None:
        if not 1 <= self.month <= 12:
            raise ValueError(f"month out of range: {self.month}")
        if not 1 <= self.day <= last_day_of_month(self.month):
            raise ValueError(f"day out of range: {self.day}")

    def to_rd(self) -> int:
        """Return the Rata Die day count for this date."""
        days_before = sum(_MONTH_LENGTHS[: self.month - 1])
        return QUMRAN_EPOCH + (self.year - 1) * _YEAR_LENGTH + days_before + self.day - 1

    @classmethod
    def from_rd(cls, rd: int) -> QumranDate:
        """Reconstruct a Qumran date from an RD value."""
        offset = rd - QUMRAN_EPOCH
        year = offset // _YEAR_LENGTH + 1
        day_of_year = offset % _YEAR_LENGTH
        month = 1
        while day_of_year >= _MONTH_LENGTHS[month - 1]:
            day_of_year -= _MONTH_LENGTHS[month - 1]
            month += 1
        return cls(year, month, day_of_year + 1)
