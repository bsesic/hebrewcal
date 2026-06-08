"""Sefirat HaOmer - the count of the Omer.

The count runs for 49 days, from 16 Nisan (day 1) to 5 Sivan (day 49); Shavuot
falls on the next day (6 Sivan).
"""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate


def omer_count(date: HebrewDate) -> int | None:
    """Return the Omer day (1-49) for ``date``, or None if outside the count."""
    start = HebrewDate(date.year, 1, 16).to_rd()
    day = date.to_rd() - start + 1
    return day if 1 <= day <= 49 else None


def omer_week_day(date: HebrewDate) -> tuple[int, int] | None:
    """Return (weeks, days) of the Omer for ``date``, or None outside the count."""
    count = omer_count(date)
    if count is None:
        return None
    return count // 7, count % 7
