"""The molad and Rosh Chodesh announcement (Shabbat Mevarchim)."""

from __future__ import annotations

import datetime
from dataclasses import dataclass

from hebrewcal.astro.molad import molad_moment
from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.hebrew.metonic import is_leap_year
from hebrewcal.hebrew.yeartype import last_day_of_month


@dataclass(frozen=True)
class MonthAnnouncement:
    """Information announced on Shabbat Mevarchim for an upcoming month."""

    molad: datetime.datetime
    rosh_chodesh: tuple[HebrewDate, ...]
    shabbat_mevarchim: HebrewDate


def _rosh_chodesh_days(year: int, month: int) -> tuple[HebrewDate, ...]:
    """Return the Rosh Chodesh day(s) for ``month`` (2 days if the previous month is long)."""
    if month == 7:  # Tishri begins with Rosh Hashanah, not Rosh Chodesh
        return ()
    prev = (13 if is_leap_year(year) else 12) if month == 1 else month - 1
    days: list[HebrewDate] = []
    if last_day_of_month(year, prev) == 30:
        days.append(HebrewDate(year, prev, 30))
    days.append(HebrewDate(year, month, 1))
    return tuple(days)


def month_announcement(year: int, month: int) -> MonthAnnouncement:
    """Return the molad, Rosh Chodesh day(s) and Shabbat Mevarchim for ``month``."""
    rc = _rosh_chodesh_days(year, month)
    first_rc = rc[0]
    prior = first_rc.to_rd() - 1
    # Shabbat Mevarchim is the Saturday on or before the day before Rosh Chodesh.
    shabbat = prior - ((prior % 7) + 1) % 7
    return MonthAnnouncement(
        molad=molad_moment(year, month),
        rosh_chodesh=rc,
        shabbat_mevarchim=HebrewDate.from_rd(shabbat),
    )
