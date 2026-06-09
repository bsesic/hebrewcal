"""The four postponement rules (dechiyot), expressed as a year-length correction.

Rosh Hashanah cannot fall on certain weekdays, and two cases adjust the length
of the year so that no year is illegally short or long. Together with the
molad-zaken adjustment inside ``calendar_elapsed_days`` these implement the
classical "four gates". The correction here adds 0, 1, or 2 days based on the
gap between consecutive years' elapsed-day counts (Dershowitz & Reingold).
"""

from __future__ import annotations

from functools import lru_cache

from hebrewcal.hebrew.molad import calendar_elapsed_days


@lru_cache(maxsize=8192)
def year_length_correction(year: int) -> int:
    """Return the 0, 1, or 2 day correction applied to ``year``'s new year."""
    ny0 = calendar_elapsed_days(year - 1)
    ny1 = calendar_elapsed_days(year)
    ny2 = calendar_elapsed_days(year + 1)
    if ny2 - ny1 == 356:
        # A year that would otherwise be 356 days long is postponed two days.
        return 2
    if ny1 - ny0 == 382:
        # A year that would otherwise be 382 days long is postponed one day.
        return 1
    return 0
