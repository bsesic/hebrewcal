"""The Samaritan calendar - a computed model.

.. warning::

   This is a *computed mean-lunar model*, not an authoritative reproduction of the
   Samaritan calendar. The living Samaritan calendar is fixed by the Samaritan High
   Priesthood using their own calculation, and the absolute correspondence and year
   numbering here are conventional. This module has NOT been verified against an
   authoritative Samaritan source; it is provided to demonstrate the extensible
   calendar interface and the mean-lunar structure.

The model is a mean-conjunction lunar calendar (mean synodic month, 12 or 13
months on the 19-year Metonic cycle), anchored to the Anno Mundi epoch so that
year numbers approximate the traditional count. Month lengths are 29 or 30 days.
"""

from __future__ import annotations

from dataclasses import dataclass

from hebrewcal.calendars_alt import _meanlunar
from hebrewcal.hebrew.yeartype import HEBREW_EPOCH

# Conventional epoch and numbering (see the module warning).
_EPOCH_RD = HEBREW_EPOCH
_LAG = 0

is_leap_year = _meanlunar.is_leap_year
months_in_year = _meanlunar.months_in_year


def last_day_of_month(year: int, month: int) -> int:
    """Return the number of days in ``month`` of ``year`` (29 or 30)."""
    return _meanlunar.last_day_of_month(_EPOCH_RD, year, month)


@dataclass(frozen=True, order=True)
class SamaritanDate:
    """A date in the Samaritan computed-model calendar."""

    year: int
    month: int
    day: int

    def __post_init__(self) -> None:
        if not 1 <= self.month <= months_in_year(self.year):
            raise ValueError(f"month out of range: {self.month}")
        if not 1 <= self.day <= last_day_of_month(self.year, self.month):
            raise ValueError(f"day out of range: {self.day}")

    def to_rd(self) -> int:
        """Return the Rata Die day count for this date."""
        return _meanlunar.to_rd(_EPOCH_RD, _LAG, self.year, self.month, self.day)

    @classmethod
    def from_rd(cls, rd: int) -> SamaritanDate:
        """Reconstruct a Samaritan date from an RD value."""
        year, month, day = _meanlunar.from_rd(_EPOCH_RD, _LAG, rd)
        return cls(year, month, day)
