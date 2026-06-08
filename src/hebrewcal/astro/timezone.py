"""Bridge between the integer RD day count and timezone-aware datetimes.

An astronomical instant is expressed as an RD value plus either a fraction of a
day or a number of minutes past 00:00 UTC. Minutes outside [0, 1440) are allowed
and roll into adjacent civil days, which is what high-latitude events need.
"""

from __future__ import annotations

import datetime
from zoneinfo import ZoneInfo

from hebrewcal.calendars.gregorian import GregorianDate


def utc_datetime(
    rd: int, day_fraction: float = 0.0, minutes: float | None = None
) -> datetime.datetime:
    """Return a UTC-aware datetime for an RD value.

    Provide either ``day_fraction`` (0.0–1.0+) or ``minutes`` past 00:00 UTC;
    ``minutes`` takes precedence when given and may lie outside a single day.
    """
    g = GregorianDate.from_rd(rd)
    base = datetime.datetime(g.year, g.month, g.day, tzinfo=datetime.UTC)
    if minutes is not None:
        return base + datetime.timedelta(minutes=minutes)
    return base + datetime.timedelta(days=day_fraction)


def local_datetime(
    rd: int,
    day_fraction: float = 0.0,
    minutes: float | None = None,
    timezone: str = "UTC",
) -> datetime.datetime:
    """Return the same instant as :func:`utc_datetime`, in the given time zone."""
    return utc_datetime(rd, day_fraction, minutes).astimezone(ZoneInfo(timezone))
