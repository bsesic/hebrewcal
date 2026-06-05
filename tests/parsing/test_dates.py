"""Tests for Gregorian date parsing."""

from __future__ import annotations

import pytest

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.parsing.dates import parse_gregorian


def test_iso_8601() -> None:
    assert parse_gregorian("2026-06-26") == GregorianDate(2026, 6, 26)


def test_din_5008() -> None:
    assert parse_gregorian("26.06.2026") == GregorianDate(2026, 6, 26)


def test_slash_format() -> None:
    assert parse_gregorian("2026/06/26") == GregorianDate(2026, 6, 26)


def test_whitespace_tolerated() -> None:
    assert parse_gregorian("  2026-06-26  ") == GregorianDate(2026, 6, 26)


def test_ambiguous_or_invalid_raises() -> None:
    with pytest.raises(ValueError):
        parse_gregorian("not a date")
    with pytest.raises(ValueError):
        parse_gregorian("2026-13-01")  # month out of range
