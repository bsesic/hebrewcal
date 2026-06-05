"""hebrewcal — a pure-Python library for the Hebrew calendar.

The library makes the Hebrew calendar usable programmatically and converts it
bidirectionally against the Gregorian and Julian calendars. Every computation is
performed locally; the library never issues network calls to any external service.

The whole design pivots on the Rata Die (RD) day count from Dershowitz & Reingold,
*Calendrical Calculations*: every calendar implements only ``to_rd`` and ``from_rd``,
and conversion between any two calendars always goes through RD.
"""

from __future__ import annotations

from importlib import metadata

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.calendars.julian import JulianDate
from hebrewcal.conversion import to_gregorian, to_hebrew, to_julian, weekday
from hebrewcal.core.calendar import Weekday

try:
    __version__ = metadata.version("hebrewcal")
except metadata.PackageNotFoundError:  # pragma: no cover - source checkout without install
    __version__ = "0.0.0.dev0"

__all__ = [
    "GregorianDate",
    "HebrewDate",
    "JulianDate",
    "Weekday",
    "__version__",
    "to_gregorian",
    "to_hebrew",
    "to_julian",
    "weekday",
]
