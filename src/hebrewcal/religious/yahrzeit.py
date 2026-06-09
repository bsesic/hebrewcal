"""Yahrzeit - the Hebrew-calendar anniversary of a death.

Edge cases handled:
- A death on the 30th of Marheshvan or Kislev: in a later year where that month has
  only 29 days, the yahrzeit moves to the 1st of the following month.
- A death in Adar of a common year, or Adar II of a leap year, maps to Adar
  (month 12) in a common year and to Adar II (month 13) in a leap year.
- A death in Adar I (month 12) of a leap year maps to Adar (month 12).
"""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.hebrew.metonic import is_leap_year
from hebrewcal.hebrew.yeartype import last_day_of_month


def yahrzeit(death: HebrewDate, year: int) -> HebrewDate:
    """Return the yahrzeit date in the Hebrew ``year`` for a death on ``death``."""
    month, day = death.month, death.day

    if death.month == 13:  # Adar II
        month = 13 if is_leap_year(year) else 12
    elif death.month == 12:  # Adar (common) or Adar I (leap)
        month = 12

    # A 30th-day death in a month that has only 29 days in the target year moves to
    # the 1st of the next month.
    if day == 30 and last_day_of_month(year, month) == 29:
        return HebrewDate(year, month + 1, 1)

    return HebrewDate(year, month, day)
