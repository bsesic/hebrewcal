"""The molad expressed as a civil instant (a mean lunar conjunction).

The molad is the *mean* conjunction used by the Hebrew calendar, reckoned in
**Jerusalem mean time**, where the molad "day" begins at 18:00 the previous
evening. It can differ from the true astronomical new moon by up to ~14 hours;
this module exposes the molad for comparison rather than computing true syzygy.

The returned datetime is **naive** and represents Jerusalem mean time. It is
deliberately not tagged with the modern ``Asia/Jerusalem`` zone, whose standard
time (UTC+2) and daylight saving differ from mean solar time at Jerusalem.
"""

from __future__ import annotations

import datetime

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.hebrew.molad import HALAKIM_PER_DAY, molad_parts
from hebrewcal.hebrew.yeartype import HEBREW_EPOCH

# The synodic month used by the calendar: 29 days, 12 hours, 793 parts.
MOLAD_INTERVAL_PARTS: int = 29 * HALAKIM_PER_DAY + 12 * 1080 + 793

_SECONDS_PER_PART: float = 24 * 3600 / HALAKIM_PER_DAY  # 10/3 seconds


def molad_breakdown(year: int, month: int) -> tuple[int, int, int]:
    """Return (day_index, hours, parts) of the molad.

    ``day_index`` is the molad day counted from the Hebrew epoch; ``hours`` and
    ``parts`` are measured from 18:00 at the start of that day.
    """
    day_index, within = divmod(molad_parts(year, month), HALAKIM_PER_DAY)
    hours, parts = divmod(within, 1080)
    return day_index, hours, parts


def molad_moment(year: int, month: int) -> datetime.datetime:
    """Return the molad as a naive datetime in Jerusalem mean time."""
    day_index, within = divmod(molad_parts(year, month), HALAKIM_PER_DAY)
    g = GregorianDate.from_rd(HEBREW_EPOCH + day_index)
    # The Hebrew day begins at 18:00 the previous civil evening; the molad parts
    # are counted from there.
    start = datetime.datetime(g.year, g.month, g.day) - datetime.timedelta(hours=6)
    return start + datetime.timedelta(seconds=within * _SECONDS_PER_PART)
