"""The Rata Die (RD) day count — the conversion pivot of the whole library.

RD is a continuous integer count of days. RD 1 is Monday, 1 January 1 in the
proleptic Gregorian calendar (Dershowitz & Reingold, *Calendrical Calculations*).
Every calendar converts to and from RD, so any two calendars are interconvertible
through it.
"""

from __future__ import annotations

# RD 1 = 1 January 1 (proleptic Gregorian). The epoch is kept explicit so the
# meaning of "day zero" is never ambiguous.
RD_EPOCH: int = 1


def weekday_from_rd(rd: int) -> int:
    """Return the day of week for an RD value.

    0 = Sunday, 1 = Monday, ..., 6 = Saturday. RD 1 is a Monday, so ``1 % 7 == 1``.
    """
    return rd % 7


def add_days(rd: int, days: int) -> int:
    """Return the RD value ``days`` after ``rd`` (``days`` may be negative)."""
    return rd + days
