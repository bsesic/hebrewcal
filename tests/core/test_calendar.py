"""Tests for the abstract calendar interface and conversion helper."""

from __future__ import annotations

from dataclasses import dataclass

from hebrewcal.core.calendar import Weekday, convert, weekday


@dataclass(frozen=True)
class _StubDate:
    """A trivial calendar where the RD value is the day number itself."""

    rd: int

    def to_rd(self) -> int:
        return self.rd

    @classmethod
    def from_rd(cls, rd: int) -> _StubDate:
        return cls(rd)


def test_convert_round_trips_through_rd() -> None:
    source = _StubDate(737000)
    result = convert(source, _StubDate)
    assert result == source


def test_weekday_returns_enum() -> None:
    # RD 1 is a Monday.
    assert weekday(_StubDate(1)) is Weekday.MONDAY


def test_weekday_enum_values() -> None:
    assert Weekday.SUNDAY.value == 0
    assert Weekday.SATURDAY.value == 6
