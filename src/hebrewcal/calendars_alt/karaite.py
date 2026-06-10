"""The Karaite calendar — an astronomical estimate of the observational calendar.

.. warning::

   The authentic Karaite calendar is **observational**: each month begins with the
   first naked-eye sighting of the new crescent over the Land of Israel, and the
   year is intercalated by the ripeness of the spring barley (aviv). Neither can be
   reduced to a formula, and actual practice depends on reports from observers.

   This module provides an **astronomical estimate**, not the authentic calendar:

   - A month begins on the evening of the first *estimated* crescent visibility over
     Jerusalem — modelled as the first sunset, at or after the true lunar conjunction
     (see :mod:`hebrewcal.astro.lunar`), at which the moon is at least
     :data:`MIN_MOON_AGE_HOURS` hours old. This is a simple age criterion, **not** a
     full first-visibility model (it ignores the moon's altitude and elongation).
   - The year begins with the month whose 15th day (Passover) is the first on or
     after the vernal equinox — a standard *approximation* of the aviv rule.

   The underlying astronomy (true conjunction, sunset, equinox) is verified, but the
   resulting calendar is **not** validated against actual Karaite practice and must
   not be used to determine observance.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from functools import lru_cache

from hebrewcal.astro.location import Location
from hebrewcal.astro.lunar import nth_new_moon
from hebrewcal.astro.solar import solar_declination, sunset
from hebrewcal.calendars.gregorian import GregorianDate

# Jerusalem, the reference location for crescent visibility.
JERUSALEM = Location(31.7683, 35.2137, elevation=754.0, timezone="Asia/Jerusalem")

# Minimum moon age at sunset for the crescent to be treated as visible. A young
# crescent below ~15-24 hours is generally not seen; 20 hours is a middle value.
MIN_MOON_AGE_HOURS: float = 20.0

# Karaite year Y is aligned with the spring of Gregorian year (Y - _AM_OFFSET).
_AM_OFFSET = 3760


def _estimate_lunation(rd: int) -> int:
    jd = rd + 1721424.5
    return round((jd - 2451550.09766) / 29.530588861)


@lru_cache(maxsize=8192)
def _month_start_rd(lunation: int) -> int:
    """Return the RD of day 1 of the month for the given true-conjunction lunation.

    Day 1 is the daytime following the evening of estimated first visibility.
    """
    conjunction = nth_new_moon(lunation)
    local = conjunction.astimezone(JERUSALEM.tzinfo)
    base = GregorianDate(local.year, local.month, local.day).to_rd()
    threshold = datetime.timedelta(hours=MIN_MOON_AGE_HOURS)
    for offset in range(0, 3):
        evening = GregorianDate.from_rd(base + offset)
        dusk = sunset(evening, JERUSALEM, elevation=True)
        if dusk is not None and dusk - conjunction >= threshold:
            return base + offset + 1
    return base + 2  # pragma: no cover - visibility is always found within 3 days


@lru_cache(maxsize=4096)
def _march_equinox_rd(gregorian_year: int) -> int:
    """Return the RD of the March (vernal) equinox, to day precision."""
    best_rd = GregorianDate(gregorian_year, 3, 20).to_rd()
    best = abs(solar_declination(gregorian_year, 3, 20))
    for day in range(17, 24):
        value = abs(solar_declination(gregorian_year, 3, day))
        if value < best:
            best = value
            best_rd = GregorianDate(gregorian_year, 3, day).to_rd()
    return best_rd


@lru_cache(maxsize=4096)
def _aviv_lunation(year: int) -> int:
    """Return the lunation index of Aviv (month 1) for the Karaite ``year``."""
    equinox = _march_equinox_rd(year - _AM_OFFSET)
    lunation = _estimate_lunation(equinox) - 3
    # Aviv is the first month whose 15th day (start + 14) is on or after the equinox.
    while _month_start_rd(lunation) + 14 < equinox:
        lunation += 1
    while _month_start_rd(lunation - 1) + 14 >= equinox:
        lunation -= 1
    return lunation


def months_in_year(year: int) -> int:
    """Return the number of months in the Karaite ``year`` (12 or 13)."""
    return _aviv_lunation(year + 1) - _aviv_lunation(year)


def last_day_of_month(year: int, month: int) -> int:
    """Return the number of days in ``month`` of ``year`` (29 or 30)."""
    lunation = _aviv_lunation(year) + (month - 1)
    return _month_start_rd(lunation + 1) - _month_start_rd(lunation)


@dataclass(frozen=True, order=True)
class KaraiteDate:
    """A date in the Karaite astronomical-estimate calendar."""

    year: int
    month: int
    day: int

    def __post_init__(self) -> None:
        if not 1 <= self.month <= months_in_year(self.year):
            raise ValueError(f"month out of range: {self.month}")
        if not 1 <= self.day <= last_day_of_month(self.year, self.month):
            raise ValueError(f"day out of range: {self.day}")

    def to_rd(self) -> int:
        """Return the Rata Die day count for this date."""
        lunation = _aviv_lunation(self.year) + (self.month - 1)
        return _month_start_rd(lunation) + self.day - 1

    @classmethod
    def from_rd(cls, rd: int) -> KaraiteDate:
        """Reconstruct a Karaite date from an RD value."""
        lunation = _estimate_lunation(rd)
        while _month_start_rd(lunation) > rd:
            lunation -= 1
        while _month_start_rd(lunation + 1) <= rd:
            lunation += 1
        year = GregorianDate.from_rd(rd).year + _AM_OFFSET
        while _aviv_lunation(year) > lunation:
            year -= 1
        while _aviv_lunation(year + 1) <= lunation:
            year += 1
        month = lunation - _aviv_lunation(year) + 1
        day = rd - _month_start_rd(lunation) + 1
        return cls(year, month, day)
