"""Yahrzeit - the Hebrew-calendar anniversary of a death.

The observance date depends on community custom in two cases, both exposed as
options:

- **Adar in a leap year.** For someone who died in (plain) Adar of a common year,
  the yahrzeit in a leap year is observed in Adar II by the common Ashkenazi ruling
  (Rema), or in Adar I by other customs. Select with :class:`AdarObservance`
  (default Adar II). A death in Adar I is always kept in Adar I; a death in Adar II
  is kept in Adar II (and in Adar of a common year).
- **The 30th of Marheshvan or Kislev.** When the target year's month has only 29
  days, the yahrzeit is observed on the 1st of the following month (the common
  ruling) or on the 29th of the same month. Select with :class:`Month30Observance`
  (default the 1st of the next month).

```{note}
The first-year custom of following the date of *burial* rather than death is not
modelled here (only the death date is taken); subsequent years follow the death
date, which is what this function returns.
```
"""

from __future__ import annotations

from enum import Enum

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.hebrew.metonic import is_leap_year
from hebrewcal.hebrew.yeartype import last_day_of_month


class AdarObservance(Enum):
    """Where a plain-Adar yahrzeit falls in a leap year."""

    ADAR_II = "adar_ii"  # common Ashkenazi ruling (Rema)
    ADAR_I = "adar_i"


class Month30Observance(Enum):
    """Where a 30th-of-month yahrzeit falls when the month is short that year."""

    FIRST_OF_NEXT = "first_of_next"  # the common ruling
    TWENTY_NINTH = "twenty_ninth"


def _yahrzeit_month(death: HebrewDate, year: int, adar: AdarObservance) -> int:
    if death.month == 13:  # Adar II
        return 13 if is_leap_year(year) else 12
    if death.month == 12 and is_leap_year(death.year):  # Adar I
        return 12
    if death.month == 12:  # plain Adar (common-year death)
        if is_leap_year(year):
            return 13 if adar is AdarObservance.ADAR_II else 12
        return 12
    return death.month


def yahrzeit(
    death: HebrewDate,
    year: int,
    *,
    adar: AdarObservance = AdarObservance.ADAR_II,
    month30: Month30Observance = Month30Observance.FIRST_OF_NEXT,
) -> HebrewDate:
    """Return the yahrzeit date in the Hebrew ``year`` for a death on ``death``.

    ``adar`` and ``month30`` select the community customs described in the module
    docstring.
    """
    month = _yahrzeit_month(death, year, adar)
    day = death.day

    if day == 30 and last_day_of_month(year, month) == 29:
        if month30 is Month30Observance.TWENTY_NINTH:
            return HebrewDate(year, month, 29)
        return HebrewDate(year, month + 1, 1)

    return HebrewDate(year, month, day)
