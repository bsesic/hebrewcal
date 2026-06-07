"""Tests for the gematria numeral converter."""

from __future__ import annotations

import pytest

from hebrewcal.numerals import from_hebrew_numeral, to_hebrew_numeral


def test_simple_values() -> None:
    assert to_hebrew_numeral(1) == "א׳"
    assert to_hebrew_numeral(10) == "י׳"
    assert to_hebrew_numeral(15) == "ט״ו"   # 9+6, not 10+5 (avoids the divine name)
    assert to_hebrew_numeral(16) == "ט״ז"   # 9+7, not 10+6


def test_hundreds_and_combinations() -> None:
    assert to_hebrew_numeral(123) == "קכ״ג"
    assert to_hebrew_numeral(248) == "רמ״ח"


def test_year_with_thousands() -> None:
    # 5785 -> ה׳תשפ״ה (the thousands 'ה followed by 785).
    assert to_hebrew_numeral(5785) == "ה׳תשפ״ה"


def test_round_trip() -> None:
    for n in (1, 7, 15, 16, 123, 248, 411, 785, 5785):
        assert from_hebrew_numeral(to_hebrew_numeral(n)) == n


def test_non_positive_rejected() -> None:
    with pytest.raises(ValueError):
        to_hebrew_numeral(0)
    with pytest.raises(ValueError):
        to_hebrew_numeral(-5)
