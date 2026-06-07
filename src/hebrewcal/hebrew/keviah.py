"""The keviah — the compact signature classifying a Hebrew year.

A year is classified by three facts: whether it is a leap year, the weekday of
Rosh Hashanah, and whether it is deficient (chaser), regular (kesidran), or
complete (shalem). Those three determine the entire layout of the year.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from hebrewcal.core.rata_die import weekday_from_rd
from hebrewcal.hebrew.metonic import is_leap_year
from hebrewcal.hebrew.yeartype import days_in_year, new_year_rd


class YearKind(Enum):
    """Whether a year is deficient, regular, or complete."""

    DEFICIENT = "deficient"
    REGULAR = "regular"
    COMPLETE = "complete"


@dataclass(frozen=True)
class Keviah:
    """The signature of a Hebrew year."""

    leap: bool
    rosh_hashanah_weekday: int
    kind: YearKind


def keviah(year: int) -> Keviah:
    """Return the :class:`Keviah` signature of the Hebrew ``year``."""
    length = days_in_year(year)
    if length in (353, 383):
        kind = YearKind.DEFICIENT
    elif length in (354, 384):
        kind = YearKind.REGULAR
    else:
        kind = YearKind.COMPLETE
    return Keviah(
        leap=is_leap_year(year),
        rosh_hashanah_weekday=weekday_from_rd(new_year_rd(year)),
        kind=kind,
    )
