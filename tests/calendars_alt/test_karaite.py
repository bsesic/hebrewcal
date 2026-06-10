"""Tests for the Karaite calendar (astronomical estimate of the observational calendar)."""

from __future__ import annotations

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars_alt.karaite import (
    KaraiteDate,
    _march_equinox_rd,
    last_day_of_month,
    months_in_year,
)


def test_round_trip() -> None:
    start = KaraiteDate(5780, 1, 1).to_rd()
    end = KaraiteDate(5795, 1, 1).to_rd()
    for rd in range(start, end, 9):
        assert KaraiteDate.from_rd(rd).to_rd() == rd


def test_month_lengths_are_29_or_30() -> None:
    for year in range(5780, 5800):
        for month in range(1, months_in_year(year) + 1):
            assert last_day_of_month(year, month) in (29, 30)


def test_months_in_year() -> None:
    for year in range(5780, 5800):
        assert months_in_year(year) in (12, 13)


def test_passover_on_or_after_equinox() -> None:
    # The aviv rule: the 15th of the first month is on or after the vernal equinox.
    for year in range(5780, 5800):
        passover = KaraiteDate(year, 1, 15).to_rd()
        equinox = _march_equinox_rd(year - 3760)
        assert passover >= equinox


def test_first_month_falls_in_spring() -> None:
    # Aviv (month 1) begins in March or April.
    for year in (5784, 5785, 5786):
        g = GregorianDate.from_rd(KaraiteDate(year, 1, 1).to_rd())
        assert g.month in (3, 4)


def test_close_to_rabbinic_in_common_years() -> None:
    # In a common (non-leap) year the estimate tracks the Rabbinic calendar closely.
    from hebrewcal.calendars.hebrew import HebrewDate
    from hebrewcal.conversion import to_gregorian

    karaite = to_gregorian(KaraiteDate(5785, 1, 1))
    rabbinic = to_gregorian(HebrewDate(5785, 1, 1))
    assert abs(karaite.to_rd() - rabbinic.to_rd()) <= 2
