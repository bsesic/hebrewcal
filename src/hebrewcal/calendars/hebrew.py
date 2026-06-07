"""The Hebrew calendar date type.

Month numbering is standard (Nisan = 1 ... Tishri = 7 ... Adar/Adar I = 12,
Adar II = 13). The civil year begins at Tishri. Conversion to and from RD uses
the year-typing machinery in :mod:`hebrewcal.hebrew`.
"""

from __future__ import annotations

from dataclasses import dataclass

from hebrewcal.hebrew.yeartype import (
    last_day_of_month,
    last_month_of_year,
    new_year_rd,
)

_TISHRI = 7


@dataclass(frozen=True, order=True)
class HebrewDate:
    """A date in the Hebrew calendar."""

    year: int
    month: int
    day: int

    def __post_init__(self) -> None:
        if not 1 <= self.month <= last_month_of_year(self.year):
            raise ValueError(f"month out of range: {self.month}")
        if not 1 <= self.day <= last_day_of_month(self.year, self.month):
            raise ValueError(f"day out of range: {self.day}")

    def to_rd(self) -> int:
        """Return the Rata Die day count for this date."""
        if self.month < _TISHRI:
            # Months Nisan..Elul fall in the second half of the civil year.
            months_after_tishri = range(_TISHRI, last_month_of_year(self.year) + 1)
            months_before = range(1, self.month)
        else:
            months_after_tishri = range(_TISHRI, self.month)
            months_before = range(0, 0)  # empty
        days_before = sum(
            last_day_of_month(self.year, m) for m in months_after_tishri
        ) + sum(last_day_of_month(self.year, m) for m in months_before)
        return new_year_rd(self.year) + days_before + self.day - 1

    @classmethod
    def from_rd(cls, rd: int) -> HebrewDate:
        """Reconstruct a Hebrew date from an RD value."""
        # Estimate the year, then correct by direct comparison.
        approx = (rd - new_year_rd(1)) // 366 + 1
        year = approx
        while new_year_rd(year + 1) <= rd:
            year += 1
        while new_year_rd(year) > rd:
            year -= 1
        # Determine the starting month: Nisan (1) if on/after 1 Nisan, else Tishri (7).
        start = 1 if rd >= cls(year, 1, 1).to_rd() else _TISHRI
        month = start
        while rd > cls(year, month, last_day_of_month(year, month)).to_rd():
            month += 1
        day = rd - cls(year, month, 1).to_rd() + 1
        return cls(year, month, day)
