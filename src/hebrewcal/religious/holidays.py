"""The holiday engine for the Hebrew year.

Each category contributes a list of :class:`Holiday` for a given Hebrew year;
:func:`holidays` aggregates and sorts them chronologically. Month numbering is the
library standard (Nisan = 1 ... Tishri = 7 ... Adar / Adar I = 12, Adar II = 13).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.hebrew.metonic import is_leap_year
from hebrewcal.hebrew.yeartype import last_day_of_month, last_month_of_year


class Category(Enum):
    """The kind of observance."""

    MAJOR_FESTIVAL = "major_festival"
    CHOL_HAMOED = "chol_hamoed"
    MINOR_FESTIVAL = "minor_festival"
    FAST = "fast"
    MODERN = "modern"
    ROSH_CHODESH = "rosh_chodesh"
    SPECIAL_SHABBAT = "special_shabbat"
    MINORITY = "minority"


@dataclass(frozen=True)
class Holiday:
    """A single observance on a specific Hebrew date."""

    name: str
    date: HebrewDate
    category: Category


def rosh_chodesh(year: int) -> list[Holiday]:
    """Return the Rosh Chodesh days of the year (one or two per month, not Tishri).

    When the preceding month has 30 days, its 30th is the first of the two Rosh
    Chodesh days. The civil-year month order is Tishri ... Elul; 1 Tishri is Rosh
    Hashanah and is never labelled Rosh Chodesh.
    """
    out: list[Holiday] = []
    months = list(range(7, last_month_of_year(year) + 1)) + list(range(1, 7))
    for month in months:
        if month == 7:
            continue  # 1 Tishri is Rosh Hashanah
        prev = month - 1 if month != 1 else last_month_of_year(year)
        if last_day_of_month(year, prev) == 30:
            out.append(Holiday("Rosh Chodesh", HebrewDate(year, prev, 30), Category.ROSH_CHODESH))
        out.append(Holiday("Rosh Chodesh", HebrewDate(year, month, 1), Category.ROSH_CHODESH))
    return out


def holidays(year: int, diaspora: bool = True) -> list[Holiday]:
    """Return all observances of the Hebrew ``year``, sorted chronologically."""
    result: list[Holiday] = []
    result += _major(year, diaspora)
    result += rosh_chodesh(year)
    result.sort(key=lambda h: (h.date.to_rd(), h.name))
    return result


def holidays_on(date: HebrewDate, diaspora: bool = True) -> list[Holiday]:
    """Return the observances falling on the given Hebrew date."""
    return [h for h in holidays(date.year, diaspora) if h.date == date]


def _major(year: int, diaspora: bool) -> list[Holiday]:
    """Placeholder for the major festivals, implemented in Task 2."""
    return [
        Holiday("Rosh Hashanah", HebrewDate(year, 7, 1), Category.MAJOR_FESTIVAL),
        Holiday("Rosh Hashanah", HebrewDate(year, 7, 2), Category.MAJOR_FESTIVAL),
    ]


def _purim_month(year: int) -> int:
    """Return the month that carries Purim (Adar, or Adar II in a leap year)."""
    return 13 if is_leap_year(year) else 12
