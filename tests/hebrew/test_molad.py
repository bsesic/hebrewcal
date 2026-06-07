"""Tests for the molad and calendar-elapsed-days computation."""

from __future__ import annotations

from hebrewcal.hebrew.molad import (
    HALAKIM_PER_DAY,
    HALAKIM_PER_HOUR,
    calendar_elapsed_days,
    molad_parts,
)


def test_halakim_constants() -> None:
    assert HALAKIM_PER_HOUR == 1080
    assert HALAKIM_PER_DAY == 25920  # 1080 * 24


def test_elapsed_days_monotonic() -> None:
    # Elapsed days must strictly increase year over year.
    prev = calendar_elapsed_days(1)
    for year in range(2, 50):
        cur = calendar_elapsed_days(year)
        assert cur > prev
        prev = cur


def test_molad_parts_within_a_day() -> None:
    # The fractional part of any molad is a valid number of halakim in a day.
    parts = molad_parts(5785, 7)  # molad of Tishri 5785
    assert 0 <= parts % HALAKIM_PER_DAY < HALAKIM_PER_DAY
