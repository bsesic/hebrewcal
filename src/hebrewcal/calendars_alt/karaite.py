"""The Karaite calendar - a computed approximation.

```{warning}
The authentic Karaite calendar is *observational*: each month begins with the
first sighting of the new crescent moon over the Land of Israel, and the year is
intercalated according to the ripeness of the barley (aviv). Those depend on
observation and cannot be reduced to a formula. This module therefore provides a
*computed approximation* only — a mean-conjunction lunar calendar with a one-day
lag standing in for the delay between conjunction and first sighting. It has NOT
been verified against actual Karaite practice and should not be used to determine
observance.
```

The approximation shares the mean-lunar engine with the Samaritan model and adds a
one-day sighting lag; the epoch and year numbering are conventional (anchored to
the Anno Mundi count). Month lengths are 29 or 30 days.
"""

from __future__ import annotations

from dataclasses import dataclass

from hebrewcal.calendars_alt import _meanlunar
from hebrewcal.hebrew.yeartype import HEBREW_EPOCH

# Conventional epoch; the one-day lag approximates first-sighting after conjunction.
_EPOCH_RD = HEBREW_EPOCH
_LAG = 1

is_leap_year = _meanlunar.is_leap_year
months_in_year = _meanlunar.months_in_year


def last_day_of_month(year: int, month: int) -> int:
    """Return the number of days in ``month`` of ``year`` (29 or 30)."""
    return _meanlunar.last_day_of_month(_EPOCH_RD, year, month)


@dataclass(frozen=True, order=True)
class KaraiteDate:
    """A date in the Karaite computed-approximation calendar."""

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
    def from_rd(cls, rd: int) -> KaraiteDate:
        """Reconstruct a Karaite date from an RD value."""
        year, month, day = _meanlunar.from_rd(_EPOCH_RD, _LAG, rd)
        return cls(year, month, day)
