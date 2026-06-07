"""The 19-year Metonic cycle.

Seven of every nineteen Hebrew years are leap years (a 13th month, Adar I, is
inserted). A year ``y`` is leap iff ``(7 * y + 1) mod 19 < 7``.
"""

from __future__ import annotations


def is_leap_year(year: int) -> bool:
    """Return whether the Hebrew ``year`` is a leap (13-month) year."""
    return (7 * year + 1) % 19 < 7


def months_in_year(year: int) -> int:
    """Return the number of months in the Hebrew ``year`` (12 or 13)."""
    return 13 if is_leap_year(year) else 12
