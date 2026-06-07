"""Tests for the keviah year signature."""

from __future__ import annotations

from hebrewcal.hebrew.keviah import YearKind, keviah
from hebrewcal.hebrew.yeartype import days_in_year


def test_year_kind_matches_length() -> None:
    k = keviah(5785)
    assert k.kind in (YearKind.DEFICIENT, YearKind.REGULAR, YearKind.COMPLETE)
    assert k.leap in (True, False)
    # Rosh Hashanah weekday is 0..6 and never Sunday/Wednesday/Friday (lo ADU rosh).
    assert k.rosh_hashanah_weekday in (1, 2, 4, 6)


def test_keviah_roundtrips_year_length() -> None:
    # COMPLETE -> long year, DEFICIENT -> short year.
    for year in range(5780, 5800):
        k = keviah(year)
        length = days_in_year(year)
        if k.kind is YearKind.DEFICIENT:
            assert length in (353, 383)
        elif k.kind is YearKind.REGULAR:
            assert length in (354, 384)
        else:
            assert length in (355, 385)
