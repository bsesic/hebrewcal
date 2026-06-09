"""Tests for yahrzeit calculation."""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.religious.yahrzeit import yahrzeit


def test_simple_yahrzeit() -> None:
    # Death on 10 Tevet 5780; yahrzeit in 5785 is 10 Tevet 5785.
    death = HebrewDate(5780, 10, 10)
    assert yahrzeit(death, 5785) == HebrewDate(5785, 10, 10)


def test_30_kislev_in_year_without_it() -> None:
    # Death on 30 Kislev 5783 (Kislev is long). In 5790 Kislev has 29 days, so the
    # yahrzeit moves to 1 Tevet; in 5785 (long Kislev) it stays on 30 Kislev.
    death = HebrewDate(5783, 9, 30)
    assert yahrzeit(death, 5790) == HebrewDate(5790, 10, 1)
    assert yahrzeit(death, 5785) == HebrewDate(5785, 9, 30)


def test_adar_ii_in_common_year() -> None:
    # Death in Adar II (leap year) -> in a common year observed in Adar (month 12).
    death = HebrewDate(5784, 13, 15)  # 15 Adar II 5784 (leap)
    assert yahrzeit(death, 5785).month == 12  # common year Adar
