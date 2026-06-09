"""Zmanim - the halachic times of the day.

Seasonal ("proportional") hours divide the daylight span into twelve. The GRA day
runs from sunrise to sunset; the MGA day runs from dawn to nightfall at 16.1
degrees. Deadlines are expressed as a number of seasonal hours after the start of
the relevant day. Each method returns a timezone-aware datetime, or None at high
latitudes where a required event does not occur.
"""

from __future__ import annotations

import datetime

from hebrewcal.astro.location import Location
from hebrewcal.astro.solar import dawn, dusk, solar_noon, sunrise, sunset
from hebrewcal.calendars.gregorian import GregorianDate

_ALOT_DEPRESSION = 16.1
_MISHEYAKIR_DEPRESSION = 11.0
_TZEIT_DEPRESSION = 8.5


def _add(
    start: datetime.datetime | None, hours: float, hour_length: datetime.timedelta | None
) -> datetime.datetime | None:
    if start is None or hour_length is None:
        return None
    return start + hour_length * hours


class Zmanim:
    """Halachic times for a date and location."""

    def __init__(self, date: GregorianDate, location: Location) -> None:
        self._date = date
        self._loc = location

    # Anchor events.
    def sunrise(self) -> datetime.datetime | None:
        return sunrise(self._date, self._loc)

    def sunset(self) -> datetime.datetime | None:
        return sunset(self._date, self._loc)

    def chatzot(self) -> datetime.datetime:
        return solar_noon(self._date, self._loc)

    def alot_hashachar(self) -> datetime.datetime | None:
        return dawn(self._date, self._loc, _ALOT_DEPRESSION)

    def misheyakir(self) -> datetime.datetime | None:
        return dawn(self._date, self._loc, _MISHEYAKIR_DEPRESSION)

    def tzeit_hakochavim(self) -> datetime.datetime | None:
        return dusk(self._date, self._loc, _TZEIT_DEPRESSION)

    # Seasonal-hour lengths.
    def _gra_hour(self) -> datetime.timedelta | None:
        sr, ss = self.sunrise(), self.sunset()
        if sr is None or ss is None:
            return None
        return (ss - sr) / 12

    def _mga_hour(self) -> datetime.timedelta | None:
        start = self.alot_hashachar()
        end = dusk(self._date, self._loc, _ALOT_DEPRESSION)
        if start is None or end is None:
            return None
        return (end - start) / 12

    # GRA deadlines (from sunrise).
    def sof_zman_shma_gra(self) -> datetime.datetime | None:
        return _add(self.sunrise(), 3, self._gra_hour())

    def sof_zman_tefilla_gra(self) -> datetime.datetime | None:
        return _add(self.sunrise(), 4, self._gra_hour())

    # MGA deadlines (from dawn).
    def sof_zman_shma_mga(self) -> datetime.datetime | None:
        return _add(self.alot_hashachar(), 3, self._mga_hour())

    def sof_zman_tefilla_mga(self) -> datetime.datetime | None:
        return _add(self.alot_hashachar(), 4, self._mga_hour())

    # Afternoon (GRA seasonal hours from sunrise).
    def mincha_gedola(self) -> datetime.datetime | None:
        return _add(self.sunrise(), 6.5, self._gra_hour())

    def mincha_ketana(self) -> datetime.datetime | None:
        return _add(self.sunrise(), 9.5, self._gra_hour())

    def plag_hamincha(self) -> datetime.datetime | None:
        return _add(self.sunrise(), 10.75, self._gra_hour())
