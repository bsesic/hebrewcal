"""Tests for the halachic times."""

from __future__ import annotations

from hebrewcal.astro.location import Location
from hebrewcal.astro.solar import solar_noon
from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.religious.zmanim import Zmanim

NEW_YORK = Location(40.7128, -74.0060, timezone="America/New_York")


def test_ordering() -> None:
    z = Zmanim(GregorianDate(2026, 6, 26), NEW_YORK)
    raw = [
        z.alot_hashachar(),
        z.misheyakir(),
        z.sunrise(),
        z.sof_zman_shma_gra(),
        z.sof_zman_tefilla_gra(),
        z.chatzot(),
        z.mincha_gedola(),
        z.mincha_ketana(),
        z.plag_hamincha(),
        z.sunset(),
        z.tzeit_hakochavim(),
    ]
    times = [t for t in raw if t is not None]
    assert len(times) == len(raw)
    assert times == sorted(times)


def test_mga_earlier_than_gra_for_shma() -> None:
    # The MGA deadline (longer day) is earlier than the GRA deadline.
    z = Zmanim(GregorianDate(2026, 6, 26), NEW_YORK)
    mga = z.sof_zman_shma_mga()
    gra = z.sof_zman_shma_gra()
    assert mga is not None and gra is not None
    assert mga < gra


def test_chatzot_is_solar_noon() -> None:
    z = Zmanim(GregorianDate(2026, 6, 26), NEW_YORK)
    assert z.chatzot() == solar_noon(GregorianDate(2026, 6, 26), NEW_YORK)
