"""Hebrew year typing: new-year RD, year length, and month lengths.

The length of a Hebrew year (353/354/355 common, 383/384/385 leap) determines
whether Marheshvan is long (30) and whether Kislev is short (29), which is what
makes a year deficient, regular, or complete.
"""

from __future__ import annotations

from hebrewcal.hebrew.dechiyot import year_length_correction
from hebrewcal.hebrew.metonic import is_leap_year, months_in_year
from hebrewcal.hebrew.molad import calendar_elapsed_days

# RD of 1 Tishri AM 1 == fixed_from_julian(-3761, 10, 7).
HEBREW_EPOCH: int = -1373427


def last_month_of_year(year: int) -> int:
    """Return the last month number of ``year`` (12 common, 13 leap)."""
    return months_in_year(year)


def new_year_rd(year: int) -> int:
    """Return the RD of 1 Tishri of the Hebrew ``year`` (Rosh Hashanah)."""
    return HEBREW_EPOCH + calendar_elapsed_days(year) + year_length_correction(year)


def days_in_year(year: int) -> int:
    """Return the number of days in the Hebrew ``year``."""
    return new_year_rd(year + 1) - new_year_rd(year)


def is_long_marheshvan(year: int) -> bool:
    """Return whether Marheshvan has 30 days in ``year``."""
    return days_in_year(year) in (355, 385)


def is_short_kislev(year: int) -> bool:
    """Return whether Kislev has 29 days in ``year``."""
    return days_in_year(year) in (353, 383)


def last_day_of_month(year: int, month: int) -> int:
    """Return the number of days in ``month`` of the Hebrew ``year``."""
    if (
        month in (2, 4, 6, 10, 13)
        or (month == 8 and not is_long_marheshvan(year))
        or (month == 9 and is_short_kislev(year))
        or (month == 12 and not is_leap_year(year))
    ):
        return 29
    return 30
