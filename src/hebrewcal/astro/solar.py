"""The solar position model and the events derived from it.

Implements the NOAA solar equations (after Meeus, *Astronomical Algorithms*) in
pure Python. Sunrise and sunset agree with reference implementations to within
about 15-20 seconds at mid latitudes after a two-pass refinement.
"""

from __future__ import annotations

import datetime
import math

from hebrewcal.astro.location import Location
from hebrewcal.astro.timekeeping import julian_centuries, julian_day, julian_day_from_rd
from hebrewcal.astro.timezone import local_datetime
from hebrewcal.calendars.gregorian import GregorianDate

# The standard sunrise/sunset solar depression: 50 arcminutes below the horizon,
# accounting for atmospheric refraction (34') and the solar semi-diameter (16').
SUNRISE_SUNSET_DEPRESSION: float = 0.8333


def _solar_terms(t: float) -> tuple[float, float]:
    """Return (declination_degrees, equation_of_time_minutes) for Julian century ``t``."""
    l0 = (280.46646 + t * (36000.76983 + t * 0.0003032)) % 360.0
    m = 357.52911 + t * (35999.05029 - 0.0001537 * t)
    e = 0.016708634 - t * (0.000042037 + 0.0000001267 * t)
    mr = math.radians(m)
    c = (
        math.sin(mr) * (1.914602 - t * (0.004817 + 0.000014 * t))
        + math.sin(2 * mr) * (0.019993 - 0.000101 * t)
        + math.sin(3 * mr) * 0.000289
    )
    true_long = l0 + c
    omega = math.radians(125.04 - 1934.136 * t)
    app_long = true_long - 0.00569 - 0.00478 * math.sin(omega)
    eps0 = 23.0 + (26.0 + (21.448 - t * (46.815 + t * (0.00059 - t * 0.001813))) / 60.0) / 60.0
    eps = eps0 + 0.00256 * math.cos(omega)
    declination = math.degrees(
        math.asin(math.sin(math.radians(eps)) * math.sin(math.radians(app_long)))
    )
    y = math.tan(math.radians(eps / 2.0)) ** 2
    l0r = math.radians(l0)
    eq_time = 4.0 * math.degrees(
        y * math.sin(2 * l0r)
        - 2 * e * math.sin(mr)
        + 4 * e * y * math.sin(mr) * math.cos(2 * l0r)
        - 0.5 * y * y * math.sin(4 * l0r)
        - 1.25 * e * e * math.sin(2 * mr)
    )
    return declination, eq_time


def solar_declination(year: int, month: int, day: int, day_fraction: float = 0.5) -> float:
    """Return the sun's declination in degrees for the given date (default local noon-ish)."""
    t = julian_centuries(julian_day(year, month, day, day_fraction))
    return _solar_terms(t)[0]


def equation_of_time(year: int, month: int, day: int, day_fraction: float = 0.5) -> float:
    """Return the equation of time in minutes for the given date."""
    t = julian_centuries(julian_day(year, month, day, day_fraction))
    return _solar_terms(t)[1]


def _event_minutes_utc(
    rd: int, latitude: float, longitude: float, depression: float, rising: bool
) -> float | None:
    """Return minutes past 00:00 UTC of a solar event, or None if it does not occur.

    Two passes: the first uses local-noon terms, the second refines using the
    terms at the event time itself, which brings agreement to ~15 seconds.
    """
    minutes = 720.0
    for _ in range(2):
        t = julian_centuries(julian_day_from_rd(rd, minutes / 1440.0))
        declination, eq_time = _solar_terms(t)
        lat_r = math.radians(latitude)
        dec_r = math.radians(declination)
        cos_h = math.cos(math.radians(90.0 + depression)) / (
            math.cos(lat_r) * math.cos(dec_r)
        ) - math.tan(lat_r) * math.tan(dec_r)
        if cos_h > 1.0 or cos_h < -1.0:
            return None
        hour_angle = math.degrees(math.acos(cos_h))
        noon = 720.0 - 4.0 * longitude - eq_time
        minutes = noon - 4.0 * hour_angle if rising else noon + 4.0 * hour_angle
    return minutes


def _solar_noon_minutes_utc(rd: int, longitude: float) -> float:
    """Return minutes past 00:00 UTC of solar noon."""
    minutes = 720.0
    for _ in range(2):
        t = julian_centuries(julian_day_from_rd(rd, minutes / 1440.0))
        _, eq_time = _solar_terms(t)
        minutes = 720.0 - 4.0 * longitude - eq_time
    return minutes


def sunrise(date: GregorianDate, location: Location) -> datetime.datetime | None:
    """Return the sunrise as a local datetime, or None if the sun does not rise."""
    minutes = _event_minutes_utc(
        date.to_rd(), location.latitude, location.longitude, SUNRISE_SUNSET_DEPRESSION, True
    )
    if minutes is None:
        return None
    return local_datetime(date.to_rd(), minutes=minutes, timezone=location.timezone)


def sunset(date: GregorianDate, location: Location) -> datetime.datetime | None:
    """Return the sunset as a local datetime, or None if the sun does not set."""
    minutes = _event_minutes_utc(
        date.to_rd(), location.latitude, location.longitude, SUNRISE_SUNSET_DEPRESSION, False
    )
    if minutes is None:
        return None
    return local_datetime(date.to_rd(), minutes=minutes, timezone=location.timezone)


def solar_noon(date: GregorianDate, location: Location) -> datetime.datetime:
    """Return solar noon as a local datetime."""
    minutes = _solar_noon_minutes_utc(date.to_rd(), location.longitude)
    return local_datetime(date.to_rd(), minutes=minutes, timezone=location.timezone)
