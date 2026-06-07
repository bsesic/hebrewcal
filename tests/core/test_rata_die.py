"""Tests for the Rata Die core."""

from __future__ import annotations

from hebrewcal.core.rata_die import RD_EPOCH, add_days, weekday_from_rd


def test_epoch_is_one() -> None:
    assert RD_EPOCH == 1


def test_weekday_of_rd_one_is_monday() -> None:
    # RD 1 = Monday, 1 January 1 (proleptic Gregorian). 0 = Sunday ... 6 = Saturday.
    assert weekday_from_rd(1) == 1


def test_weekday_cycle() -> None:
    assert weekday_from_rd(0) == 0  # Sunday
    assert weekday_from_rd(7) == 0
    assert weekday_from_rd(6) == 6  # Saturday


def test_add_days() -> None:
    assert add_days(10, 5) == 15
    assert add_days(10, -3) == 7
