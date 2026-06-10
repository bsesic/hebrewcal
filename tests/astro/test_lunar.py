"""Tests for the true astronomical new moon."""

from __future__ import annotations

import datetime

from hebrewcal.astro.lunar import (
    MEAN_SYNODIC_MONTH,
    new_moon_at_or_after,
    new_moon_before,
    nth_new_moon,
)
from hebrewcal.calendars.gregorian import GregorianDate

TOL = datetime.timedelta(minutes=2)


def test_synodic_month_constant() -> None:
    assert abs(MEAN_SYNODIC_MONTH - 29.530588861) < 1e-9


def test_epoch_new_moon() -> None:
    # Meeus lunation 0: 2000-01-06 ~18:14 UTC.
    nm = nth_new_moon(0)
    assert nm.tzinfo is datetime.UTC
    expected = datetime.datetime(2000, 1, 6, 18, 14, 46, tzinfo=datetime.UTC)
    assert abs(nm - expected) <= TOL


def test_known_new_moons() -> None:
    # Cross-checked against an ephemeris (to ~ΔT).
    dec = new_moon_at_or_after(GregorianDate(2024, 12, 1))
    assert abs(dec - datetime.datetime(2024, 12, 1, 6, 22, 42, tzinfo=datetime.UTC)) <= TOL
    jan = new_moon_at_or_after(GregorianDate(2025, 1, 15))
    assert abs(jan - datetime.datetime(2025, 1, 29, 12, 37, 8, tzinfo=datetime.UTC)) <= TOL


def test_consecutive_interval_is_synodic() -> None:
    prev = nth_new_moon(300)
    for n in range(301, 320):
        cur = nth_new_moon(n)
        days = (cur - prev).total_seconds() / 86400
        assert 29.2 < days < 29.9  # the synodic month varies around 29.53
        prev = cur


def test_before_and_after_bracket_the_date() -> None:
    date = GregorianDate(2024, 12, 15)
    before = new_moon_before(date)
    after = new_moon_at_or_after(date)
    midnight = datetime.datetime(2024, 12, 15, tzinfo=datetime.UTC)
    assert before < midnight <= after
    # The new moon before 15 Dec 2024 is the 1 Dec 2024 one.
    assert before.month == 12 and before.day == 1
