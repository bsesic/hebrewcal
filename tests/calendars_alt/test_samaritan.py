"""Tests for the Samaritan calendar (computed model)."""

from __future__ import annotations

from hebrewcal.calendars_alt.samaritan import SamaritanDate, last_day_of_month, months_in_year


def test_round_trip() -> None:
    start = SamaritanDate(5700, 1, 1).to_rd()
    end = SamaritanDate(5800, 1, 1).to_rd()
    for rd in range(start, end, 11):
        assert SamaritanDate.from_rd(rd).to_rd() == rd


def test_month_lengths_are_29_or_30() -> None:
    for year in range(5780, 5800):
        for month in range(1, months_in_year(year) + 1):
            assert last_day_of_month(year, month) in (29, 30)


def test_months_in_year() -> None:
    for year in range(5780, 5800):
        assert months_in_year(year) in (12, 13)


def test_year_length_in_range() -> None:
    for year in range(5780, 5800):
        length = SamaritanDate(year + 1, 1, 1).to_rd() - SamaritanDate(year, 1, 1).to_rd()
        assert length in (353, 354, 355, 383, 384, 385)
