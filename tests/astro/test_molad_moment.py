"""Tests for the molad expressed as a civil instant."""

from __future__ import annotations

import datetime

from hebrewcal.astro.molad import MOLAD_INTERVAL_PARTS, molad_breakdown, molad_moment


def test_molad_interval_constant() -> None:
    # The mean lunar month is exactly 29 days, 12 hours, 793 parts.
    assert MOLAD_INTERVAL_PARTS == 29 * 25920 + 12 * 1080 + 793


def test_consecutive_molads_differ_by_one_interval() -> None:
    # The civil molad instants are one synodic interval apart (to the second).
    a = molad_moment(5785, 7)
    b = molad_moment(5785, 8)
    seconds = (b - a).total_seconds()
    expected = MOLAD_INTERVAL_PARTS * (24 * 3600 / 25920)
    assert abs(seconds - expected) < 1.0


def test_breakdown_ranges() -> None:
    _, hours, parts = molad_breakdown(5785, 7)
    assert 0 <= hours < 24
    assert 0 <= parts < 1080


def test_molad_moment_is_naive_jerusalem_mean_time() -> None:
    # The molad is reckoned in Jerusalem mean time; the returned datetime is naive.
    m = molad_moment(5785, 7)
    assert isinstance(m, datetime.datetime)
    assert m.tzinfo is None
    # Sanity: the molad of Tishri 5785 falls in autumn 2024.
    assert m.year == 2024 and m.month == 10
