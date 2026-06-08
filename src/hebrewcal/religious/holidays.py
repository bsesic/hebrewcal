"""The holiday engine for the Hebrew year.

Each category contributes a list of :class:`Holiday` for a given Hebrew year;
:func:`holidays` aggregates and sorts them chronologically. Month numbering is the
library standard (Nisan = 1 ... Tishri = 7 ... Adar / Adar I = 12, Adar II = 13).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.core.rata_die import weekday_from_rd
from hebrewcal.hebrew.metonic import is_leap_year
from hebrewcal.hebrew.yeartype import last_day_of_month, last_month_of_year

_SHABBAT = 6  # weekday_from_rd: 0 = Sunday ... 6 = Saturday


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
    result += _minor(year, diaspora)
    result += _fasts(year, diaspora)
    result += _modern(year, diaspora)
    result += _minority(year, diaspora)
    result += rosh_chodesh(year)
    result.sort(key=lambda h: (h.date.to_rd(), h.name))
    return result


def holidays_on(date: HebrewDate, diaspora: bool = True) -> list[Holiday]:
    """Return the observances falling on the given Hebrew date."""
    return [h for h in holidays(date.year, diaspora) if h.date == date]


def _major(year: int, diaspora: bool) -> list[Holiday]:
    """Return the major festivals, honouring the diaspora second festival day."""
    out: list[Holiday] = []

    def add(name: str, month: int, day: int, category: Category = Category.MAJOR_FESTIVAL) -> None:
        out.append(Holiday(name, HebrewDate(year, month, day), category))

    # Tishri.
    add("Rosh Hashanah", 7, 1)
    add("Rosh Hashanah", 7, 2)
    add("Yom Kippur", 7, 10)
    add("Sukkot", 7, 15)
    if diaspora:
        add("Sukkot", 7, 16)
    for day in range(17 if diaspora else 16, 22):
        add("Sukkot", 7, day, Category.CHOL_HAMOED)
    add("Hoshana Rabbah", 7, 21, Category.MINOR_FESTIVAL)
    add("Shemini Atzeret", 7, 22)
    add("Simchat Torah", 7, 23 if diaspora else 22)

    # Nisan - Pesach (7 days in Israel, 8 in the Diaspora).
    add("Pesach", 1, 15)
    if diaspora:
        add("Pesach", 1, 16)
    for day in range(17 if diaspora else 16, 21):
        add("Pesach", 1, day, Category.CHOL_HAMOED)
    add("Pesach", 1, 21)
    if diaspora:
        add("Pesach", 1, 22)

    # Sivan - Shavuot (1 day in Israel, 2 in the Diaspora).
    add("Shavuot", 3, 6)
    if diaspora:
        add("Shavuot", 3, 7)
    return out


def _purim_month(year: int) -> int:
    """Return the month that carries Purim (Adar, or Adar II in a leap year)."""
    return 13 if is_leap_year(year) else 12


def _minor(year: int, diaspora: bool) -> list[Holiday]:
    """Return the minor (mostly rabbinic) festive days."""
    out: list[Holiday] = []

    def add(name: str, month: int, day: int) -> None:
        out.append(Holiday(name, HebrewDate(year, month, day), Category.MINOR_FESTIVAL))

    # Hanukkah: 25 Kislev for eight days. The run rolls into Tevet a day earlier when
    # Kislev is short, so build it by walking RD from 25 Kislev.
    start = HebrewDate(year, 9, 25).to_rd()
    for i in range(8):
        out.append(Holiday("Hanukkah", HebrewDate.from_rd(start + i), Category.MINOR_FESTIVAL))

    add("Tu BiShvat", 11, 15)

    purim_month = _purim_month(year)
    if is_leap_year(year):
        # Purim Katan / Shushan Purim Katan fall in Adar I.
        add("Purim Katan", 12, 14)
        add("Shushan Purim Katan", 12, 15)
    add("Purim", purim_month, 14)
    add("Shushan Purim", purim_month, 15)

    add("Pesach Sheni", 2, 14)
    add("Lag BaOmer", 2, 18)
    add("Tu B'Av", 5, 15)
    return out


def _postpone_if_shabbat(date: HebrewDate) -> HebrewDate:
    """Return the date, moved to Sunday if it falls on Shabbat."""
    if weekday_from_rd(date.to_rd()) == _SHABBAT:
        return HebrewDate.from_rd(date.to_rd() + 1)
    return date


def _fasts(year: int, diaspora: bool) -> list[Holiday]:
    """Return the public fasts, applying the postponement rules."""
    out: list[Holiday] = []
    purim_month = _purim_month(year)

    # These move to Sunday when they fall on Shabbat.
    for name, month, day in (
        ("Tzom Gedaliah", 7, 3),
        ("Shiva Asar B'Tammuz", 4, 17),
        ("Tisha B'Av", 5, 9),
    ):
        moved = _postpone_if_shabbat(HebrewDate(year, month, day))
        out.append(Holiday(name, moved, Category.FAST))

    # Asara B'Tevet is never postponed (it cannot fall on Shabbat).
    out.append(Holiday("Asara B'Tevet", HebrewDate(year, 10, 10), Category.FAST))

    # Ta'anit Esther: 13 Adar(II); if Shabbat, brought forward to Thursday (11 Adar).
    esther = HebrewDate(year, purim_month, 13)
    if weekday_from_rd(esther.to_rd()) == _SHABBAT:
        esther = HebrewDate.from_rd(esther.to_rd() - 2)
    out.append(Holiday("Ta'anit Esther", esther, Category.FAST))

    # Ta'anit Bechorot: 14 Nisan, brought forward to Thursday 12 Nisan if on Shabbat.
    bechorot = HebrewDate(year, 1, 14)
    if weekday_from_rd(bechorot.to_rd()) == _SHABBAT:
        bechorot = HebrewDate.from_rd(bechorot.to_rd() - 2)
    out.append(Holiday("Ta'anit Bechorot", bechorot, Category.FAST))
    return out


def _modern(year: int, diaspora: bool) -> list[Holiday]:
    """Return the modern Israeli days, applying the statutory weekday adjustments.

    Weekdays use weekday_from_rd (0 = Sunday ... 6 = Saturday).
    """
    out: list[Holiday] = []

    # Yom HaShoah, 27 Nisan: Friday -> 26 Nisan (Thu); Sunday -> 28 Nisan (Mon).
    shoah = HebrewDate(year, 1, 27)
    wd = weekday_from_rd(shoah.to_rd())
    if wd == 5:  # Friday
        shoah = HebrewDate(year, 1, 26)
    elif wd == 0:  # Sunday
        shoah = HebrewDate(year, 1, 28)
    out.append(Holiday("Yom HaShoah", shoah, Category.MODERN))

    # Yom HaZikaron (4 Iyyar) and Yom HaAtzmaut (5 Iyyar), keyed off 5 Iyyar's weekday.
    # 5 Iyyar can only be Monday, Wednesday, Friday or Saturday (lo BaDU Pesach).
    wd5 = weekday_from_rd(HebrewDate(year, 2, 5).to_rd())
    if wd5 == 5:  # Friday -> Atzmaut Thu 4, Zikaron Wed 3
        zikaron, atzmaut = (year, 2, 3), (year, 2, 4)
    elif wd5 == 6:  # Saturday -> Atzmaut Thu 3, Zikaron Wed 2
        zikaron, atzmaut = (year, 2, 2), (year, 2, 3)
    elif wd5 == 1:  # Monday -> Zikaron Mon 5, Atzmaut Tue 6
        zikaron, atzmaut = (year, 2, 5), (year, 2, 6)
    else:  # Wednesday -> default Zikaron 4, Atzmaut 5
        zikaron, atzmaut = (year, 2, 4), (year, 2, 5)
    out.append(Holiday("Yom HaZikaron", HebrewDate(*zikaron), Category.MODERN))
    out.append(Holiday("Yom HaAtzmaut", HebrewDate(*atzmaut), Category.MODERN))

    out.append(Holiday("Yom Yerushalayim", HebrewDate(year, 2, 28), Category.MODERN))
    return out


def _minority(year: int, diaspora: bool) -> list[Holiday]:
    """Return communal feasts of specific Jewish communities."""
    return [
        # Sigd, Ethiopian Jewry: 29 Marheshvan, the 50th day after Yom Kippur.
        Holiday("Sigd", HebrewDate(year, 8, 29), Category.MINORITY),
        # Mimouna, North African communities: the day after Pesach ends (22 Nisan).
        Holiday("Mimouna", HebrewDate(year, 1, 22), Category.MINORITY),
    ]
