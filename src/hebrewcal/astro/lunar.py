"""The true astronomical new moon (lunar conjunction / syzygy).

This computes the *true* new moon using the periodic terms of Meeus,
*Astronomical Algorithms* (2nd ed.), chapter 49 — distinct from the calendar's
*mean* conjunction (the molad). The two can differ by up to about 14 hours.

The instants are returned as timezone-aware UTC datetimes. The underlying value is
in Terrestrial Time (TT); the difference from UTC is ΔT (a few tens of seconds in
the modern era, ~70 s around 2024), which is well within the intended use
(academic comparison with the molad). The implementation agrees with an
independent ephemeris to ~1 minute.
"""

from __future__ import annotations

import datetime
import math

from hebrewcal.astro.timezone import utc_datetime
from hebrewcal.calendars.gregorian import GregorianDate

# The mean synodic month, in days (Meeus 49.1).
MEAN_SYNODIC_MONTH: float = 29.530588861

_JD_TO_RD: float = 1721424.5

# Additional ("planetary") correction coefficients and the A1..A14 arguments.
_ADDITIONAL = (
    (0.000325, 299.77, 0.107408, -0.009173),
    (0.000165, 251.88, 0.016321, 0.0),
    (0.000164, 251.83, 26.651886, 0.0),
    (0.000126, 349.42, 36.412478, 0.0),
    (0.000110, 84.66, 18.206239, 0.0),
    (0.000062, 141.74, 53.303771, 0.0),
    (0.000060, 207.14, 2.453732, 0.0),
    (0.000056, 154.84, 7.306860, 0.0),
    (0.000047, 34.52, 27.261239, 0.0),
    (0.000042, 207.19, 0.121824, 0.0),
    (0.000040, 291.34, 1.844379, 0.0),
    (0.000037, 161.72, 24.198154, 0.0),
    (0.000035, 239.56, 25.513099, 0.0),
    (0.000023, 331.55, 3.592518, 0.0),
)


def _new_moon_jde(n: int) -> float:
    """Return the Julian Ephemeris Day (TT) of the ``n``-th new moon.

    ``n`` is the lunation number of Meeus (n = 0 is the new moon of
    2000 January 6); negative values are valid.
    """
    k = float(n)
    t = k / 1236.85
    jde = (
        2451550.09766
        + 29.530588861 * k
        + 0.00015437 * t**2
        - 0.000000150 * t**3
        + 0.00000000073 * t**4
    )
    sun_m = 2.5534 + 29.10535670 * k - 0.0000014 * t**2 - 0.00000011 * t**3
    moon_m = (
        201.5643
        + 385.81693528 * k
        + 0.0107582 * t**2
        + 0.00001238 * t**3
        - 0.000000058 * t**4
    )
    f = (
        160.7108
        + 390.67050284 * k
        - 0.0016118 * t**2
        - 0.00000227 * t**3
        + 0.000000011 * t**4
    )
    omega = 124.7746 - 1.56375588 * k + 0.0020672 * t**2 + 0.00000215 * t**3
    e = 1.0 - 0.002516 * t - 0.0000074 * t**2

    sm = math.radians(sun_m)
    mm = math.radians(moon_m)
    fr = math.radians(f)
    om = math.radians(omega)

    correction = (
        -0.40720 * math.sin(mm)
        + 0.17241 * e * math.sin(sm)
        + 0.01608 * math.sin(2 * mm)
        + 0.01039 * math.sin(2 * fr)
        + 0.00739 * e * math.sin(mm - sm)
        - 0.00514 * e * math.sin(mm + sm)
        + 0.00208 * e * e * math.sin(2 * sm)
        - 0.00111 * math.sin(mm - 2 * fr)
        - 0.00057 * math.sin(mm + 2 * fr)
        + 0.00056 * e * math.sin(2 * mm + sm)
        - 0.00042 * math.sin(3 * mm)
        + 0.00042 * e * math.sin(sm + 2 * fr)
        + 0.00038 * e * math.sin(sm - 2 * fr)
        - 0.00024 * e * math.sin(2 * mm - sm)
        - 0.00017 * math.sin(om)
        - 0.00007 * math.sin(mm + 2 * sm)
        + 0.00004 * math.sin(2 * mm - 2 * fr)
        + 0.00004 * math.sin(3 * sm)
        + 0.00003 * math.sin(mm + sm - 2 * fr)
        + 0.00003 * math.sin(2 * mm + 2 * fr)
        - 0.00003 * math.sin(mm + sm + 2 * fr)
        + 0.00003 * math.sin(mm - sm + 2 * fr)
        - 0.00002 * math.sin(mm - sm - 2 * fr)
        - 0.00002 * math.sin(3 * mm + sm)
        + 0.00002 * math.sin(4 * mm)
    )
    additional = sum(
        coef * math.sin(math.radians(c0 + c1 * k + c2 * t**2))
        for coef, c0, c1, c2 in _ADDITIONAL
    )
    return jde + correction + additional


def _new_moon_rd(n: int) -> float:
    return _new_moon_jde(n) - _JD_TO_RD


def _to_datetime(jde: float) -> datetime.datetime:
    rd_float = jde - _JD_TO_RD
    rd = math.floor(rd_float)
    return utc_datetime(rd, day_fraction=rd_float - rd)


def _estimate_lunation(rd: int) -> int:
    year = 2000.0 + (rd + _JD_TO_RD - 2451545.0) / 365.25
    return round((year - 2000.0) * 12.3685)


def nth_new_moon(n: int) -> datetime.datetime:
    """Return the ``n``-th true new moon as a UTC datetime (n = 0 is 2000-01-06)."""
    return _to_datetime(_new_moon_jde(n))


def new_moon_at_or_after(date: GregorianDate) -> datetime.datetime:
    """Return the first true new moon at or after 00:00 UTC on ``date``."""
    rd = date.to_rd()
    n = _estimate_lunation(rd) - 2
    while _new_moon_rd(n) < rd:
        n += 1
    return _to_datetime(_new_moon_jde(n))


def new_moon_before(date: GregorianDate) -> datetime.datetime:
    """Return the last true new moon strictly before 00:00 UTC on ``date``."""
    rd = date.to_rd()
    n = _estimate_lunation(rd) + 2
    while _new_moon_rd(n) >= rd:
        n -= 1
    return _to_datetime(_new_moon_jde(n))
