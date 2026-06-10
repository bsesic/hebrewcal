"""Tests for the configurable yahrzeit conventions."""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.hebrew.metonic import is_leap_year
from hebrewcal.religious.yahrzeit import (
    AdarObservance,
    Month30Observance,
    yahrzeit,
)


def test_leap_years_for_fixtures() -> None:
    # Sanity for the fixtures below.
    assert not is_leap_year(5785)  # common
    assert is_leap_year(5787)      # leap


def test_plain_adar_adar_ii_vs_adar_i() -> None:
    death = HebrewDate(5785, 12, 7)  # 7 Adar of a common year
    assert yahrzeit(death, 5787).month == 13                       # default: Adar II
    assert yahrzeit(death, 5787, adar=AdarObservance.ADAR_II).month == 13
    assert yahrzeit(death, 5787, adar=AdarObservance.ADAR_I).month == 12


def test_adar_i_death_stays_adar_i() -> None:
    death = HebrewDate(5784, 12, 7)  # Adar I (5784 is leap)
    assert yahrzeit(death, 5787).month == 12   # Adar I in a leap year
    assert yahrzeit(death, 5785).month == 12   # plain Adar in a common year


def test_adar_ii_death() -> None:
    death = HebrewDate(5784, 13, 7)  # Adar II
    assert yahrzeit(death, 5787).month == 13   # Adar II in a leap year
    assert yahrzeit(death, 5785).month == 12   # plain Adar in a common year


def test_month30_options() -> None:
    death = HebrewDate(5783, 9, 30)  # 30 Kislev (Kislev long in 5783)
    # 5790 has a short (29-day) Kislev.
    assert yahrzeit(death, 5790) == HebrewDate(5790, 10, 1)   # default: 1 Tevet
    assert yahrzeit(death, 5790, month30=Month30Observance.FIRST_OF_NEXT) == HebrewDate(5790, 10, 1)
    assert yahrzeit(death, 5790, month30=Month30Observance.TWENTY_NINTH) == HebrewDate(5790, 9, 29)
    # In a year with a long Kislev it stays on 30 Kislev.
    assert yahrzeit(death, 5785) == HebrewDate(5785, 9, 30)


def test_simple_case_unchanged() -> None:
    assert yahrzeit(HebrewDate(5780, 10, 10), 5785) == HebrewDate(5785, 10, 10)
