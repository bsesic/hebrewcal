"""The abstract calendar interface and cross-calendar conversion.

Any calendar date is a value that can produce an RD (``to_rd``) and be rebuilt
from an RD (``from_rd``). That pair is the entire contract a calendar must meet
to interoperate with every other calendar in the library.
"""

from __future__ import annotations

from enum import IntEnum
from typing import Protocol, Self, TypeVar, runtime_checkable

from hebrewcal.core.rata_die import weekday_from_rd


class Weekday(IntEnum):
    """Day of week with Sunday = 0, matching ``weekday_from_rd``."""

    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6


@runtime_checkable
class CalendarDate(Protocol):
    """Structural type for any value that can produce a Rata Die day count."""

    def to_rd(self) -> int:
        """Return the Rata Die day count for this date."""
        ...


class _Convertible(CalendarDate, Protocol):
    """A calendar date that is both convertible to and constructible from RD."""

    @classmethod
    def from_rd(cls, rd: int) -> Self:  # pragma: no cover - protocol only
        ...


T = TypeVar("T", bound=_Convertible)


def convert(date: CalendarDate, target: type[T]) -> T:
    """Convert ``date`` to the ``target`` calendar by routing through RD."""
    return target.from_rd(date.to_rd())


def weekday(date: CalendarDate) -> Weekday:
    """Return the :class:`Weekday` of any calendar date."""
    return Weekday(weekday_from_rd(date.to_rd()))
