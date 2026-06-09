"""A generic mean-conjunction lunar calendar engine.

Shared by the Samaritan and Karaite computed models. Months follow the mean
synodic month (29 days, 12 hours, 793 parts) from a configurable epoch, and the
year carries 12 or 13 months on the 19-year Metonic cycle. An optional whole-day
``lag`` shifts every month start (used to approximate the observational delay
between conjunction and first sighting).

This is a *mean* model: it does not reproduce the decisions of any living
calendar authority. The concrete calendars built on it document their status and
conventions explicitly.
"""

from __future__ import annotations

HALAKIM_PER_DAY = 25920
# The mean synodic month: 29 days, 12 hours, 793 parts.
MEAN_MONTH_PARTS = 29 * HALAKIM_PER_DAY + 12 * 1080 + 793  # 765433


def is_leap_year(year: int) -> bool:
    """Return whether ``year`` carries a 13th month (Metonic cycle)."""
    return (7 * year + 1) % 19 < 7


def months_in_year(year: int) -> int:
    """Return the number of months in ``year`` (12 or 13)."""
    return 13 if is_leap_year(year) else 12


def _months_before_year(year: int) -> int:
    """Return the number of months from the epoch year to the start of ``year``."""
    return (235 * year - 234) // 19


def new_month_rd(epoch_rd: int, months_elapsed: int) -> int:
    """Return the RD on which the month ``months_elapsed`` after the epoch begins."""
    return epoch_rd + (months_elapsed * MEAN_MONTH_PARTS) // HALAKIM_PER_DAY


def to_rd(epoch_rd: int, lag: int, year: int, month: int, day: int) -> int:
    """Return the RD of ``year``/``month``/``day`` for the given epoch and lag."""
    months_elapsed = _months_before_year(year) + (month - 1)
    return new_month_rd(epoch_rd, months_elapsed) + (day - 1) + lag


def last_day_of_month(epoch_rd: int, year: int, month: int) -> int:
    """Return the number of days in ``month`` of ``year`` (29 or 30)."""
    months_elapsed = _months_before_year(year) + (month - 1)
    return new_month_rd(epoch_rd, months_elapsed + 1) - new_month_rd(epoch_rd, months_elapsed)


def from_rd(epoch_rd: int, lag: int, rd: int) -> tuple[int, int, int]:
    """Return the (year, month, day) for an RD under the given epoch and lag."""
    adj = rd - lag
    months_elapsed = ((adj - epoch_rd) * HALAKIM_PER_DAY) // MEAN_MONTH_PARTS
    while new_month_rd(epoch_rd, months_elapsed) > adj:
        months_elapsed -= 1
    while new_month_rd(epoch_rd, months_elapsed + 1) <= adj:
        months_elapsed += 1
    year = (months_elapsed * 19 + 234) // 235 + 1
    while _months_before_year(year) > months_elapsed:
        year -= 1
    while _months_before_year(year + 1) <= months_elapsed:
        year += 1
    month = months_elapsed - _months_before_year(year) + 1
    day = adj - new_month_rd(epoch_rd, months_elapsed) + 1
    return year, month, day
