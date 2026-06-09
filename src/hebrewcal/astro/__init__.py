"""Astronomy and locations — pure Python, no dependencies.

Implements solar position, sunrise/sunset and twilight (Meeus / NOAA algorithms),
a geographic ``Location`` type, and time-zone handling via the standard-library
``zoneinfo`` module. This is the foundation for all time-of-day religious
calculations.

The most-used names are re-exported here for convenience.
"""

from __future__ import annotations

from hebrewcal.astro.location import Location
from hebrewcal.astro.molad import molad_breakdown, molad_moment
from hebrewcal.astro.solar import (
    ASTRONOMICAL_DEPRESSION,
    CIVIL_DEPRESSION,
    NAUTICAL_DEPRESSION,
    SUNRISE_SUNSET_DEPRESSION,
    dawn,
    dusk,
    equation_of_time,
    solar_declination,
    solar_noon,
    sunrise,
    sunset,
)
from hebrewcal.astro.timekeeping import julian_centuries, julian_day, julian_day_from_rd

__all__ = [
    "ASTRONOMICAL_DEPRESSION",
    "CIVIL_DEPRESSION",
    "NAUTICAL_DEPRESSION",
    "SUNRISE_SUNSET_DEPRESSION",
    "Location",
    "dawn",
    "dusk",
    "equation_of_time",
    "julian_centuries",
    "julian_day",
    "julian_day_from_rd",
    "molad_breakdown",
    "molad_moment",
    "solar_declination",
    "solar_noon",
    "sunrise",
    "sunset",
]
