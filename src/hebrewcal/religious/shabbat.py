"""Shabbat (and yom tov) candle lighting and Havdalah.

Candle lighting is a fixed number of minutes before sunset (18 by default; some
communities use 40, e.g. Jerusalem). Havdalah is nightfall, given either as a
solar depression below the horizon (8.5 degrees by default) or as a fixed number
of minutes after sunset.
"""

from __future__ import annotations

import datetime

from hebrewcal.astro.location import Location
from hebrewcal.astro.solar import dusk, sunset
from hebrewcal.calendars.gregorian import GregorianDate

DEFAULT_CANDLE_OFFSET = 18
DEFAULT_HAVDALAH_DEPRESSION = 8.5


def candle_lighting(
    date: GregorianDate, location: Location, minutes_before_sunset: int = DEFAULT_CANDLE_OFFSET
) -> datetime.datetime | None:
    """Return candle-lighting time, or None if the sun does not set that day."""
    ss = sunset(date, location)
    if ss is None:
        return None
    return ss - datetime.timedelta(minutes=minutes_before_sunset)


def havdalah(
    date: GregorianDate,
    location: Location,
    depression: float = DEFAULT_HAVDALAH_DEPRESSION,
    minutes_after_sunset: int | None = None,
) -> datetime.datetime | None:
    """Return Havdalah time.

    With ``minutes_after_sunset`` set, use that fixed offset after sunset; otherwise
    use nightfall at the given solar ``depression``. Returns None at high latitudes
    where the relevant event does not occur.
    """
    if minutes_after_sunset is not None:
        ss = sunset(date, location)
        if ss is None:
            return None
        return ss + datetime.timedelta(minutes=minutes_after_sunset)
    return dusk(date, location, depression)
