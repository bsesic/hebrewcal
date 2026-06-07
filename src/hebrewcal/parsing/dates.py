"""Parse Gregorian dates supplied in several textual formats.

Supported forms: ISO 8601 (``YYYY-MM-DD``), DIN 5008 (``DD.MM.YYYY``) and the
slash form (``YYYY/MM/DD``). The result is always a normalised
:class:`~hebrewcal.calendars.gregorian.GregorianDate`; ambiguous or invalid input
raises ``ValueError``.
"""

from __future__ import annotations

import re

from hebrewcal.calendars.gregorian import GregorianDate

_ISO = re.compile(r"^(?P<y>-?\d{1,6})-(?P<m>\d{1,2})-(?P<d>\d{1,2})$")
_SLASH = re.compile(r"^(?P<y>-?\d{1,6})/(?P<m>\d{1,2})/(?P<d>\d{1,2})$")
_DIN = re.compile(r"^(?P<d>\d{1,2})\.(?P<m>\d{1,2})\.(?P<y>-?\d{1,6})$")


def parse_gregorian(text: str) -> GregorianDate:
    """Parse ``text`` into a :class:`GregorianDate`.

    Raises ``ValueError`` if the input matches no known format or denotes an
    invalid calendar date.
    """
    cleaned = text.strip()
    for pattern in (_ISO, _SLASH, _DIN):
        match = pattern.match(cleaned)
        if match:
            year = int(match.group("y"))
            month = int(match.group("m"))
            day = int(match.group("d"))
            # GregorianDate validates ranges and raises ValueError on bad dates.
            return GregorianDate(year, month, day)
    raise ValueError(f"unrecognised date format: {text!r}")
