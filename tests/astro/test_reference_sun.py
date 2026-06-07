"""Cross-checked reference values and invariants for the solar computations.

The reference sunrise/sunset times were cross-checked against NOAA's solar
calculator and the `astral` package while writing the implementation; they are
asserted here to a 2-minute tolerance, well above the ~20-second agreement.
"""

from __future__ import annotations

import datetime

import pytest

from hebrewcal.astro.location import Location
from hebrewcal.astro.solar import dawn, dusk, sunrise, sunset
from hebrewcal.calendars.gregorian import GregorianDate

TOL = datetime.timedelta(minutes=2)

CASES = [
    # location, date, (rise_h, rise_m), (set_h, set_m)
    (Location(40.7128, -74.0060, timezone="America/New_York"), (2026, 6, 26), (5, 27), (20, 31)),
    (Location(31.7683, 35.2137, timezone="Asia/Jerusalem"), (2026, 6, 26), (5, 36), (19, 48)),
    (Location(51.5074, -0.1278, timezone="Europe/London"), (2026, 3, 20), (6, 4), (18, 13)),
]


@pytest.mark.parametrize("loc,date,rise_hm,set_hm", CASES)
def test_reference_sunrise_sunset(
    loc: Location,
    date: tuple[int, int, int],
    rise_hm: tuple[int, int],
    set_hm: tuple[int, int],
) -> None:
    g = GregorianDate(*date)
    rise = sunrise(g, loc)
    set_ = sunset(g, loc)
    assert rise is not None and set_ is not None
    expected_rise = rise.replace(hour=rise_hm[0], minute=rise_hm[1], second=0, microsecond=0)
    expected_set = set_.replace(hour=set_hm[0], minute=set_hm[1], second=0, microsecond=0)
    assert abs(rise - expected_rise) <= TOL
    assert abs(set_ - expected_set) <= TOL


def test_twilight_strict_ordering() -> None:
    loc = Location(40.7128, -74.0060, timezone="America/New_York")
    g = GregorianDate(2026, 6, 26)
    raw = [
        dawn(g, loc, 18.0),
        dawn(g, loc, 12.0),
        dawn(g, loc, 6.0),
        sunrise(g, loc),
        sunset(g, loc),
        dusk(g, loc, 6.0),
        dusk(g, loc, 12.0),
        dusk(g, loc, 18.0),
    ]
    times = [t for t in raw if t is not None]
    assert len(times) == len(raw)  # none of the events were None
    assert times == sorted(times)


def test_southern_hemisphere_winter_sun() -> None:
    # Sydney in late June (winter): the sun rises after 06:30 and sets before 17:30.
    loc = Location(-33.8688, 151.2093, timezone="Australia/Sydney")
    g = GregorianDate(2026, 6, 26)
    rise = sunrise(g, loc)
    set_ = sunset(g, loc)
    assert rise is not None and set_ is not None
    assert rise.hour == 7 or (rise.hour == 6 and rise.minute >= 30)
    assert set_.hour == 16 or (set_.hour == 17 and set_.minute <= 30)
