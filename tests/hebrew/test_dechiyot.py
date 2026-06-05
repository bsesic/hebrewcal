"""Tests for the four postponement rules expressed as year-length correction."""

from __future__ import annotations

from hebrewcal.hebrew.dechiyot import year_length_correction


def test_correction_is_in_known_set() -> None:
    # The correction is always 0, 1, or 2 days.
    for year in range(5700, 5800):
        assert year_length_correction(year) in (0, 1, 2)
