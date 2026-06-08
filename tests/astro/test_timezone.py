"""Tests for the RD/UTC-minutes <-> datetime bridge."""

from __future__ import annotations

import datetime

from hebrewcal.astro.timezone import local_datetime, utc_datetime
from hebrewcal.calendars.gregorian import GregorianDate


def test_utc_datetime_midnight() -> None:
    rd = GregorianDate(2026, 6, 26).to_rd()
    dt = utc_datetime(rd, 0.0)
    assert dt == datetime.datetime(2026, 6, 26, tzinfo=datetime.UTC)


def test_utc_datetime_minutes() -> None:
    rd = GregorianDate(2026, 6, 26).to_rd()
    dt = utc_datetime(rd, minutes=12 * 60)  # noon UTC
    assert dt == datetime.datetime(2026, 6, 26, 12, 0, tzinfo=datetime.UTC)


def test_minutes_can_exceed_a_day() -> None:
    # Minutes past midnight may roll into the next civil day (e.g. polar events).
    rd = GregorianDate(2026, 6, 26).to_rd()
    dt = utc_datetime(rd, minutes=25 * 60)
    assert dt == datetime.datetime(2026, 6, 27, 1, 0, tzinfo=datetime.UTC)


def test_local_datetime_zone() -> None:
    rd = GregorianDate(2026, 6, 26).to_rd()
    dt = local_datetime(rd, minutes=16 * 60, timezone="America/New_York")
    # 16:00 UTC on 2026-06-26 is 12:00 EDT (UTC-4).
    assert dt.hour == 12
    assert dt.utcoffset() == datetime.timedelta(hours=-4)
