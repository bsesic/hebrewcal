"""Alternative Jewish calendars: Karaite, Qumran and Samaritan.

Each plugs into the abstract Calendar interface without changes to the core. The
Samaritan and Karaite calendars are documented computed models (see their module
docstrings); the Qumran 364-day calendar is exact.
"""

from __future__ import annotations

from hebrewcal.calendars_alt.karaite import KaraiteDate
from hebrewcal.calendars_alt.qumran import QumranDate
from hebrewcal.calendars_alt.samaritan import SamaritanDate

__all__ = ["KaraiteDate", "QumranDate", "SamaritanDate"]
