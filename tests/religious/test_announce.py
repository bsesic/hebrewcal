"""Tests for the molad / Rosh Chodesh announcement."""

from __future__ import annotations

from hebrewcal.core.rata_die import weekday_from_rd
from hebrewcal.religious.announce import month_announcement


def test_announcement_fields() -> None:
    # Announcing the month of Kislev 5785.
    a = month_announcement(5785, 9)
    assert a.molad.year == 2024
    assert len(a.rosh_chodesh) in (1, 2)
    # Shabbat Mevarchim is a Saturday.
    assert weekday_from_rd(a.shabbat_mevarchim.to_rd()) == 6


def test_shabbat_mevarchim_before_rosh_chodesh() -> None:
    a = month_announcement(5785, 9)
    assert a.shabbat_mevarchim.to_rd() < a.rosh_chodesh[0].to_rd()
