"""The weekly Torah reading (parashat hashavua).

The annual cycle begins with Bereshit on the first Shabbat after Simchat Torah and
runs through Ha'azinu the following autumn (Vezot Haberachah is read on Simchat
Torah itself, not on a Shabbat). Which of the seven combinable pairs are read
together is fixed by the year type (leap, Rosh Hashanah weekday, year length, and
Israel vs Diaspora); the table below was verified against an independent reference
on thousands of Shabbatot. Shabbatot coinciding with a festival have no weekly
parasha (a festival reading is used instead) and are returned as ``None``.
"""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.hebrew.metonic import is_leap_year
from hebrewcal.hebrew.yeartype import days_in_year, new_year_rd

PARSHIYOT = (
    "Bereshit", "Noach", "Lech-Lecha", "Vayera", "Chayei Sarah", "Toldot",
    "Vayetzei", "Vayishlach", "Vayeshev", "Miketz", "Vayigash", "Vayechi",
    "Shemot", "Va'era", "Bo", "Beshalach", "Yitro", "Mishpatim", "Terumah",
    "Tetzaveh", "Ki Tisa", "Vayakhel", "Pekudei", "Vayikra", "Tzav", "Shemini",
    "Tazria", "Metzora", "Acharei Mot", "Kedoshim", "Emor", "Behar", "Bechukotai",
    "Bamidbar", "Nasso", "Beha'alotcha", "Shelach", "Korach", "Chukat", "Balak",
    "Pinchas", "Matot", "Masei", "Devarim", "Va'etchanan", "Eikev", "Re'eh",
    "Shoftim", "Ki Teitzei", "Ki Tavo", "Nitzavim", "Vayelech", "Ha'azinu",
    "Vezot Haberachah",
)

# Adjacent combinable pairs, by the first parashah's index.
_PAIRS = {21, 26, 28, 31, 38, 41, 50}

# Year type -> the set of pair-first-indices read combined. Key:
# (is_leap, rosh_hashanah_weekday, year_length, israel). Verified against an
# independent reference over 5760-5840 (Israel and Diaspora), zero mismatches.
_COMBOS: dict[tuple[bool, int, int, bool], frozenset[int]] = {
    (False, 1, 353, False): frozenset({21, 26, 28, 31, 41, 50}),
    (False, 1, 355, False): frozenset({21, 26, 28, 31, 38, 41, 50}),
    (False, 2, 354, False): frozenset({21, 26, 28, 31, 38, 41, 50}),
    (False, 4, 354, False): frozenset({21, 26, 28, 31, 41}),
    (False, 4, 355, False): frozenset({26, 28, 31, 41}),
    (False, 6, 353, False): frozenset({21, 26, 28, 31, 41}),
    (False, 6, 355, False): frozenset({21, 26, 28, 31, 41, 50}),
    (True, 1, 383, False): frozenset({38, 41, 50}),
    (True, 1, 385, False): frozenset({41}),
    (True, 2, 384, False): frozenset({41}),
    (True, 4, 383, False): frozenset(),
    (True, 4, 385, False): frozenset({50}),
    (True, 6, 383, False): frozenset({41, 50}),
    (True, 6, 385, False): frozenset({38, 41, 50}),
    (False, 1, 353, True): frozenset({21, 26, 28, 31, 41, 50}),
    (False, 1, 355, True): frozenset({21, 26, 28, 31, 41, 50}),
    (False, 2, 354, True): frozenset({21, 26, 28, 31, 41, 50}),
    (False, 4, 354, True): frozenset({21, 26, 28, 41}),
    (False, 4, 355, True): frozenset({26, 28, 31, 41}),
    (False, 6, 353, True): frozenset({21, 26, 28, 31, 41}),
    (False, 6, 355, True): frozenset({21, 26, 28, 31, 41, 50}),
    (True, 1, 383, True): frozenset({41, 50}),
    (True, 1, 385, True): frozenset(),
    (True, 2, 384, True): frozenset(),
    (True, 4, 383, True): frozenset(),
    (True, 4, 385, True): frozenset({50}),
    (True, 6, 383, True): frozenset({41, 50}),
    (True, 6, 385, True): frozenset({41, 50}),
}


def _displaced(israel: bool) -> set[tuple[int, int]]:
    """Return the (month, day) pairs whose Shabbat carries a festival reading."""
    days: set[tuple[int, int]] = {(7, 1), (7, 2), (7, 10)}
    days |= {(7, d) for d in range(15, 23)}  # Sukkot through Shemini Atzeret
    if not israel:
        days.add((7, 23))  # Simchat Torah (Diaspora)
    days |= {(1, d) for d in range(15, 22)}  # Pesach
    if not israel:
        days.add((1, 22))
    days.add((3, 6))  # Shavuot
    if not israel:
        days.add((3, 7))
    return days


def _year_combos(year: int, israel: bool) -> frozenset[int]:
    key = (is_leap_year(year), new_year_rd(year) % 7, days_in_year(year), israel)
    return _COMBOS[key]


def _readings(year: int, israel: bool) -> list[str]:
    """Return the ordered Shabbat readings for the cycle whose spring is in ``year``."""
    combos = _year_combos(year, israel)
    out: list[str] = []
    i = 0
    while i <= 52:  # Bereshit (0) through Ha'azinu (52)
        if i in _PAIRS and i in combos:
            out.append(f"{PARSHIYOT[i]}-{PARSHIYOT[i + 1]}")
            i += 2
        else:
            out.append(PARSHIYOT[i])
            i += 1
    return out


def _bereshit_shabbat(year: int, israel: bool) -> int:
    """Return the RD of the first Shabbat after Simchat Torah of ``year``."""
    simchat_torah = HebrewDate(year, 7, 22 if israel else 23).to_rd()
    return simchat_torah + ((6 - simchat_torah % 7) % 7) + (7 if simchat_torah % 7 == 6 else 0)


def parasha(date: HebrewDate, israel: bool = False) -> str | None:
    """Return the parashah read on the Shabbat ``date``, or None.

    None is returned when ``date`` is not a Saturday, or when the Shabbat carries a
    festival reading instead of the weekly parashah.
    """
    rd = date.to_rd()
    if rd % 7 != 6:
        return None
    displaced = _displaced(israel)
    if (date.month, date.day) in displaced:
        return None
    cycle_year = date.year if rd >= _bereshit_shabbat(date.year, israel) else date.year - 1
    readings = _readings(cycle_year, israel)
    index = 0
    cur = _bereshit_shabbat(cycle_year, israel)
    while cur <= rd:
        cur_date = HebrewDate.from_rd(cur)
        if (cur_date.month, cur_date.day) in displaced:
            cur += 7
            continue
        if cur == rd:
            return readings[index] if index < len(readings) else None
        index += 1
        if index >= len(readings):
            return None
        cur += 7
    return None


def triennial_portion(date: HebrewDate, israel: bool = False) -> int | None:
    """Return the triennial-cycle position (1, 2 or 3) for the Shabbat ``date``.

    Under the modern (Conservative) triennial cycle the same weekly parashah is read
    each year, but only one third of it; this returns *which* third — the position of
    the annual cycle within the running three-year cycle. ``None`` is returned when
    there is no weekly parashah that Shabbat.

    .. note::

       This is the cycle **structure** only. The specific verse ranges of each third
       are defined by the published CJLS triennial table, which is not included here;
       so this does not by itself tell you which verses are read. The cycle position
       is taken modulo three from the start of the annual reading cycle.
    """
    if parasha(date, israel) is None:
        return None
    rd = date.to_rd()
    cycle_year = date.year if rd >= _bereshit_shabbat(date.year, israel) else date.year - 1
    return cycle_year % 3 + 1
