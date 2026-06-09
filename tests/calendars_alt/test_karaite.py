"""Tests for the Karaite calendar (computed approximation)."""

from __future__ import annotations

from hebrewcal.calendars_alt.karaite import KaraiteDate, last_day_of_month, months_in_year


def test_round_trip() -> None:
    start = KaraiteDate(5700, 1, 1).to_rd()
    end = KaraiteDate(5800, 1, 1).to_rd()
    for rd in range(start, end, 11):
        assert KaraiteDate.from_rd(rd).to_rd() == rd


def test_month_lengths_are_29_or_30() -> None:
    for year in range(5780, 5800):
        for month in range(1, months_in_year(year) + 1):
            assert last_day_of_month(year, month) in (29, 30)


def test_one_day_sighting_lag_vs_samaritan() -> None:
    # The Karaite model lags the mean conjunction by one day relative to the
    # Samaritan (no-lag) model with the same epoch.
    from hebrewcal.calendars_alt.samaritan import SamaritanDate

    assert KaraiteDate(5785, 1, 1).to_rd() == SamaritanDate(5785, 1, 1).to_rd() + 1
