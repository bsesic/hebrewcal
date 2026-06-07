"""The Anno Mundi (AM) era.

The AM year is the Hebrew calendar year number; conversion is computationally
exact and unambiguous. The library does NOT silently "correct" the well-known
discrepancy between the traditional reckoning and academic-historical chronology
for the Persian period (the "missing years"); instead it documents it and offers
the gap as data for academic use.
"""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate

# The traditional Hebrew chronology compresses the Persian period, making it
# roughly 165 years shorter than the academic-historical reckoning.
_MISSING_YEARS_GAP = 165

MISSING_YEARS_NOTICE = (
    "The traditional Anno Mundi reckoning differs from academic-historical "
    "chronology by about 165 years for the Persian period (the 'missing years'). "
    "hebrewcal computes AM years exactly and does not silently correct this "
    "discrepancy; consumers needing historical alignment should apply the gap "
    "explicitly. See the project specification for details."
)


def anno_mundi_year(date: HebrewDate) -> int:
    """Return the Anno Mundi year of a Hebrew date (identical to its year)."""
    return date.year


def traditional_vs_academic_gap() -> int:
    """Return the approximate year gap (~165) of the missing-years discrepancy."""
    return _MISSING_YEARS_GAP
