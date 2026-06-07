"""Molad arithmetic and the calendar-elapsed-days function.

Time in the Hebrew calendar is measured in *halakim* (parts): there are 1080
parts in an hour and therefore 25920 in a day. A *helek* is one part. The molad
is the mean lunar conjunction; ``calendar_elapsed_days`` converts a year to the
number of days elapsed from the epoch to that year's Tishri, applying the
molad-zaken / lo-ADU portion of the postponement logic (Dershowitz & Reingold).
"""

from __future__ import annotations

HALAKIM_PER_HOUR: int = 1080
HALAKIM_PER_DAY: int = 24 * HALAKIM_PER_HOUR  # 25920


def months_until(year: int) -> int:
    """Return the number of months elapsed before Tishri of ``year``."""
    return (235 * year - 234) // 19


def molad_parts(year: int, month: int) -> int:
    """Return the molad of ``month`` in ``year`` as total parts since the epoch.

    ``month`` uses standard numbering (Tishri = 7). The returned value is an
    absolute parts count; ``value // HALAKIM_PER_DAY`` is the day and
    ``value % HALAKIM_PER_DAY`` the parts within that day.
    """
    months_elapsed = months_until(year) + (month - 7)
    return 12084 + 13753 * months_elapsed + 29 * HALAKIM_PER_DAY * months_elapsed


def calendar_elapsed_days(year: int) -> int:
    """Return days from the Hebrew epoch to Tishri 1 of ``year``.

    This is the value before year-length correction, with the molad-zaken
    adjustment already applied.
    """
    months_elapsed = months_until(year)
    parts_elapsed = 12084 + 13753 * months_elapsed
    day = 29 * months_elapsed + parts_elapsed // HALAKIM_PER_DAY
    # Molad-zaken / partial lo-ADU: if 3*(day+1) mod 7 < 3, postpone one day.
    if (3 * (day + 1)) % 7 < 3:
        return day + 1
    return day
