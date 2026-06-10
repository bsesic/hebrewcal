"""Tests for the additional zmanim opinions."""

from __future__ import annotations

import datetime

from hebrewcal.astro.location import Location
from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.religious.zmanim import Zmanim

NEW_YORK = Location(40.7128, -74.0060, timezone="America/New_York")


def _z() -> Zmanim:
    return Zmanim(GregorianDate(2026, 6, 26), NEW_YORK)


def test_alot_degrees_configurable() -> None:
    z = _z()
    a16 = z.alot_hashachar()        # default 16.1
    a19 = z.alot_hashachar(19.8)    # a deeper (earlier) opinion
    assert a16 is not None and a19 is not None
    assert a19 < a16


def test_alot_fixed_minutes() -> None:
    z = _z()
    sr = z.sunrise()
    a = z.alot_hashachar_fixed(72)
    assert sr is not None and a is not None
    assert abs((sr - a) - datetime.timedelta(minutes=72)).total_seconds() < 1


def test_tzeit_variants_ordered() -> None:
    z = _z()
    ss = z.sunset()
    t_stars = z.tzeit_hakochavim()      # 8.5 degrees
    t_fixed = z.tzeit_fixed(42)
    t_rt = z.tzeit_rabbeinu_tam(72)
    assert ss is not None and t_stars is not None and t_fixed is not None and t_rt is not None
    assert ss < t_stars
    assert ss < t_fixed < t_rt
    assert abs((t_rt - ss) - datetime.timedelta(minutes=72)).total_seconds() < 1


def test_default_zmanim_unchanged() -> None:
    # The seasonal-hour methods still work with the configurable anchors.
    z = _z()
    assert z.sof_zman_shma_mga() is not None
    assert z.sof_zman_shma_gra() is not None
