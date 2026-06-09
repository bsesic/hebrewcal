"""Month and weekday name tables in several naming systems.

Month numbering is standard (Nisan = 1 ... Tishri = 7 ... Adar/Adar I = 12,
Adar II = 13). In a leap year month 12 is "Adar I" and month 13 is "Adar II";
in a common year month 12 is simply "Adar".
"""

from __future__ import annotations

from typing import Literal

from hebrewcal.hebrew.metonic import is_leap_year

MonthSystem = Literal["transliteration", "babylonian", "biblical", "hebrew"]

# Indexed by month number 1..13. Index 0 is unused.
_TRANSLITERATION = (
    "",
    "Nisan", "Iyyar", "Sivan", "Tammuz", "Av", "Elul",
    "Tishri", "Marheshvan", "Kislev", "Tevet", "Shevat", "Adar", "Adar II",
)
_BABYLONIAN = (
    "",
    "Nisanu", "Ayaru", "Simanu", "Du'uzu", "Abu", "Ululu",
    "Tashritu", "Arahsamnu", "Kislimu", "Tebetu", "Shabatu", "Addaru", "Addaru II",
)
# Biblical names exist only for some months; fall back to the transliteration.
_BIBLICAL = {
    1: "Aviv",
    2: "Ziv",
    7: "Ethanim",
    8: "Bul",
}

# Native Hebrew-script month names, indexed 1..13. Month 12 is plain Adar in a
# common year and Adar I in a leap year (handled below); month 13 is Adar II.
_HEBREW = (
    "",
    "ניסן", "אייר", "סיון", "תמוז", "אב", "אלול",
    "תשרי", "מרחשון", "כסלו", "טבת", "שבט", "אדר", "אדר ב׳",
)

_WEEKDAYS = (
    "Yom Rishon",    # 0 Sunday
    "Yom Sheni",     # 1 Monday
    "Yom Shlishi",   # 2 Tuesday
    "Yom Revi'i",    # 3 Wednesday
    "Yom Chamishi",  # 4 Thursday
    "Yom Shishi",    # 5 Friday
    "Shabbat",       # 6 Saturday
)

_WEEKDAYS_HEBREW = (
    "יום ראשון",   # 0 Sunday
    "יום שני",     # 1 Monday
    "יום שלישי",   # 2 Tuesday
    "יום רביעי",   # 3 Wednesday
    "יום חמישי",   # 4 Thursday
    "יום שישי",    # 5 Friday
    "שבת",         # 6 Saturday
)


def hebrew_month_name(
    year: int, month: int, system: MonthSystem = "transliteration"
) -> str:
    """Return the name of ``month`` in ``year`` for the given naming ``system``."""
    if not 1 <= month <= 13:
        raise ValueError(f"month out of range: {month}")
    if system == "transliteration":
        if month == 12 and is_leap_year(year):
            return "Adar I"
        return _TRANSLITERATION[month]
    if system == "babylonian":
        if month == 12 and is_leap_year(year):
            return "Addaru I"
        return _BABYLONIAN[month]
    if system == "biblical":
        if month == 12 and is_leap_year(year):
            return "Adar I"
        return _BIBLICAL.get(month, _TRANSLITERATION[month])
    if system == "hebrew":
        if month == 12 and is_leap_year(year):
            return "אדר א׳"
        return _HEBREW[month]
    raise ValueError(f"unknown naming system: {system!r}")


def weekday_name(weekday: int, hebrew: bool = False) -> str:
    """Return the weekday name (0 = Sunday ... 6 = Saturday).

    By default a transliteration is returned; pass ``hebrew=True`` for native
    Hebrew script.
    """
    if not 0 <= weekday <= 6:
        raise ValueError(f"weekday out of range: {weekday}")
    return _WEEKDAYS_HEBREW[weekday] if hebrew else _WEEKDAYS[weekday]
