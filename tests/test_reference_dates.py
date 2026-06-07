"""Cross-checked reference dates and round-trip properties for all calendars.

The Gregorian RD values are cross-checked against the Python standard library's
proleptic Gregorian ordinal, which is independent of this library's arithmetic.
The Hebrew/Gregorian correspondences are well-known fixed points.
"""

from __future__ import annotations

import datetime

import pytest

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.calendars.julian import JulianDate
from hebrewcal.conversion import to_gregorian, to_hebrew


@pytest.mark.parametrize("ordinal", [1, 1000, 100000, 700000, 710347, 739428])
def test_gregorian_matches_stdlib(ordinal: int) -> None:
    d = datetime.date.fromordinal(ordinal)
    g = GregorianDate(d.year, d.month, d.day)
    assert g.to_rd() == ordinal
    assert GregorianDate.from_rd(ordinal) == g


@pytest.mark.parametrize(
    "greg,heb",
    [
        ((2024, 10, 3), (5785, 7, 1)),    # 1 Tishri 5785
        ((1867, 10, 31), (5628, 8, 2)),   # roadmap acceptance example
        ((2026, 6, 26), (5786, 4, 11)),   # cross-checked fixed point
    ],
)
def test_known_hebrew_correspondences(
    greg: tuple[int, int, int], heb: tuple[int, int, int]
) -> None:
    g = GregorianDate(*greg)
    h = to_hebrew(g)
    assert (h.year, h.month, h.day) == heb
    assert to_gregorian(HebrewDate(*heb)) == g


def test_hebrew_full_range_round_trip() -> None:
    start = HebrewDate(5700, 7, 1).to_rd()
    end = HebrewDate(5820, 7, 1).to_rd()
    for rd in range(start, end, 7):  # sample weekly to keep the test fast
        assert HebrewDate.from_rd(rd).to_rd() == rd


def test_julian_gregorian_reform_alignment() -> None:
    assert JulianDate(1582, 10, 4).to_rd() + 1 == GregorianDate(1582, 10, 15).to_rd()


@pytest.mark.parametrize("rd", [-200000, -1373427, -1000, 0, 1, 500000, 739428])
def test_all_calendars_round_trip(rd: int) -> None:
    assert GregorianDate.from_rd(rd).to_rd() == rd
    assert JulianDate.from_rd(rd).to_rd() == rd
    assert HebrewDate.from_rd(rd).to_rd() == rd
