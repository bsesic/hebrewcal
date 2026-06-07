"""Tests for the Location value type."""

from __future__ import annotations

import datetime

import pytest

from hebrewcal.astro.location import Location


def test_construct_and_fields() -> None:
    loc = Location(31.7683, 35.2137, elevation=754.0, timezone="Asia/Jerusalem")
    assert loc.latitude == 31.7683
    assert loc.longitude == 35.2137
    assert loc.elevation == 754.0
    assert loc.timezone == "Asia/Jerusalem"


def test_defaults() -> None:
    loc = Location(0.0, 0.0)
    assert loc.elevation == 0.0
    assert loc.timezone == "UTC"


def test_tzinfo_property() -> None:
    loc = Location(40.7128, -74.0060, timezone="America/New_York")
    assert loc.tzinfo.key == "America/New_York"
    instant = datetime.datetime(2026, 6, 26, 12, 0, tzinfo=datetime.UTC)
    assert instant.astimezone(loc.tzinfo).utcoffset() == datetime.timedelta(hours=-4)


def test_latitude_out_of_range() -> None:
    with pytest.raises(ValueError):
        Location(91.0, 0.0)
    with pytest.raises(ValueError):
        Location(-90.5, 0.0)


def test_longitude_out_of_range() -> None:
    with pytest.raises(ValueError):
        Location(0.0, 181.0)


def test_unknown_timezone() -> None:
    with pytest.raises(ValueError):
        Location(0.0, 0.0, timezone="Mars/Olympus_Mons")
