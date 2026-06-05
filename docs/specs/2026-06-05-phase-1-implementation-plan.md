# Phase 1 — Calendar Core, Conversion & Date Handling — Implementation Plan

> **For implementers:** Execute this plan task by task. Steps use checkbox (`- [ ]`)
> syntax for tracking. Each task is test-driven: write the failing test, watch it fail,
> implement the minimum to pass, watch it pass, commit. Run the lint gate
> (`flake8`, `ruff check .`, `mypy`) and `pytest` before every commit.

**Goal:** Build the calendrical core of `hebrewcal` — the Rata Die pivot, the Gregorian,
Julian and Hebrew calendars, bidirectional conversion, date parsing/formatting, the
gematria numeral converter, the month/day name tables, and the Anno Mundi era — all in
pure Python with no runtime dependencies.

**Architecture:** Every calendar reduces a date to an integer Rata Die (RD) day count and
reconstructs a date from it (`to_rd` / `from_rd`). RD 1 is Monday, 1 January 1 (proleptic
Gregorian). Conversion between any two calendars always goes through RD, so a new calendar
only needs those two functions. All algorithms follow Dershowitz & Reingold,
*Calendrical Calculations* (4th ed.).

**Tech stack:** Python 3.11+, standard library only. `dataclasses` for immutable date
value types, `typing.Protocol` for the calendar interface, `pytest` for tests.

**Issue map:** Task 1 → #8 · Task 2 → #9 · Task 3 → #10 · Task 4 → #11 · Task 5 → #12 ·
Task 6 → #13 · Task 7 → #14 · Task 8 → #15 · Task 9 → #16 · Task 10 → #18 · Task 11 → #19 ·
Task 12 → #20.

**Conventions for this phase:**
- Work on branch `feature/phase-1-core` off `development`. Optionally one sub-branch per
  task if you prefer smaller PRs; otherwise commit per task on the one branch.
- Month numbering is **Dershowitz & Reingold standard**: Nisan = 1, Iyyar = 2, Sivan = 3,
  Tammuz = 4, Av = 5, Elul = 6, Tishri = 7, Marheshvan = 8, Kislev = 9, Tevet = 10,
  Shevat = 11, Adar (or Adar I in leap years) = 12, Adar II = 13. The civil year begins at
  Tishri (month 7). This is documented in code and in the names module.
- All comments and docstrings in English. No attribution lines in commits.

---

## File Structure

| File | Responsibility |
|------|----------------|
| `src/hebrewcal/core/rata_die.py` | RD epoch constant, integer day arithmetic, weekday from RD. |
| `src/hebrewcal/core/calendar.py` | `CalendarDate` protocol, `convert()`, `Weekday` enum, shared errors. |
| `src/hebrewcal/calendars/gregorian.py` | `GregorianDate` dataclass, proleptic `to_rd`/`from_rd`, leap rule. |
| `src/hebrewcal/calendars/julian.py` | `JulianDate` dataclass, proleptic `to_rd`/`from_rd`, reform helper. |
| `src/hebrewcal/hebrew/metonic.py` | 19-year cycle, leap-year test, months-in-year. |
| `src/hebrewcal/hebrew/molad.py` | Molad moment, halakim/helek, elapsed days. |
| `src/hebrewcal/hebrew/dechiyot.py` | The four postponement rules → year-length correction. |
| `src/hebrewcal/hebrew/yeartype.py` | New-year RD, year length, month lengths, year classification. |
| `src/hebrewcal/hebrew/keviah.py` | Year-type signature (keviah). |
| `src/hebrewcal/calendars/hebrew.py` | `HebrewDate` dataclass, `to_rd`/`from_rd`. |
| `src/hebrewcal/conversion.py` | High-level conversion helpers and weekday lookup. |
| `src/hebrewcal/parsing/dates.py` | Parse ISO 8601, DIN 5008, and other Gregorian inputs. |
| `src/hebrewcal/formatting/dates.py` | Numeric and named output formatting. |
| `src/hebrewcal/numerals.py` | Integer ↔ Hebrew numeral (gematria) conversion. |
| `src/hebrewcal/names.py` | Month and weekday name tables (standard, Babylonian, biblical, transliteration). |
| `src/hebrewcal/eras/anno_mundi.py` | AM year helpers and documented missing-years notice. |
| `tests/...` | One test module per source module, plus `tests/test_reference_dates.py`. |

---

## Task 1: Rata Die core and the abstract Calendar interface  (issue #8)

**Files:**
- Create: `src/hebrewcal/core/rata_die.py`
- Create: `src/hebrewcal/core/calendar.py`
- Test: `tests/core/test_rata_die.py`
- Test: `tests/core/test_calendar.py`

- [ ] **Step 1: Write the failing test for RD weekday and arithmetic**

Create `tests/core/test_rata_die.py`:

```python
"""Tests for the Rata Die core."""

from __future__ import annotations

from hebrewcal.core.rata_die import RD_EPOCH, add_days, weekday_from_rd


def test_epoch_is_one() -> None:
    assert RD_EPOCH == 1


def test_weekday_of_rd_one_is_monday() -> None:
    # RD 1 = Monday, 1 January 1 (proleptic Gregorian). 0 = Sunday ... 6 = Saturday.
    assert weekday_from_rd(1) == 1


def test_weekday_cycle() -> None:
    assert weekday_from_rd(0) == 0  # Sunday
    assert weekday_from_rd(7) == 0
    assert weekday_from_rd(6) == 6  # Saturday


def test_add_days() -> None:
    assert add_days(10, 5) == 15
    assert add_days(10, -3) == 7
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `pytest tests/core/test_rata_die.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'hebrewcal.core.rata_die'`.

- [ ] **Step 3: Implement `rata_die.py`**

Create `src/hebrewcal/core/rata_die.py`:

```python
"""The Rata Die (RD) day count — the conversion pivot of the whole library.

RD is a continuous integer count of days. RD 1 is Monday, 1 January 1 in the
proleptic Gregorian calendar (Dershowitz & Reingold, *Calendrical Calculations*).
Every calendar converts to and from RD, so any two calendars are interconvertible
through it.
"""

from __future__ import annotations

# RD 1 = 1 January 1 (proleptic Gregorian). The epoch is kept explicit so the
# meaning of "day zero" is never ambiguous.
RD_EPOCH: int = 1


def weekday_from_rd(rd: int) -> int:
    """Return the day of week for an RD value.

    0 = Sunday, 1 = Monday, ..., 6 = Saturday. RD 1 is a Monday, so ``1 % 7 == 1``.
    """
    return rd % 7


def add_days(rd: int, days: int) -> int:
    """Return the RD value ``days`` after ``rd`` (``days`` may be negative)."""
    return rd + days
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest tests/core/test_rata_die.py -v`
Expected: PASS (4 tests).

- [ ] **Step 5: Write the failing test for the calendar interface**

Create `tests/core/test_calendar.py`:

```python
"""Tests for the abstract calendar interface and conversion helper."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from hebrewcal.core.calendar import Weekday, convert, weekday


@dataclass(frozen=True)
class _StubDate:
    """A trivial calendar where the RD value is the day number itself."""

    rd: int

    def to_rd(self) -> int:
        return self.rd

    @classmethod
    def from_rd(cls, rd: int) -> "_StubDate":
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
```

- [ ] **Step 6: Run the test to verify it fails**

Run: `pytest tests/core/test_calendar.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'hebrewcal.core.calendar'`.

- [ ] **Step 7: Implement `calendar.py`**

Create `src/hebrewcal/core/calendar.py`:

```python
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
```

- [ ] **Step 8: Add the package `__init__` files for test subpackages**

Create empty `tests/__init__.py` and `tests/core/__init__.py` (so pytest import mode is
unambiguous):

```python
```

(Both files are empty.)

- [ ] **Step 9: Run the tests to verify they pass**

Run: `pytest tests/core/ -v`
Expected: PASS (3 tests in `test_calendar.py`, 4 in `test_rata_die.py`).

- [ ] **Step 10: Run the full gate and commit**

```bash
flake8 && ruff check . && mypy && pytest -q
git add src/hebrewcal/core/rata_die.py src/hebrewcal/core/calendar.py tests/
git commit -m "feat(core): add Rata Die pivot and calendar interface

Implement the RD day count (RD 1 = Monday, 1 Jan 1 proleptic Gregorian),
weekday derivation, and the CalendarDate protocol with a convert() helper
that routes every conversion through RD.

Closes #8"
```

---

## Task 2: Proleptic Gregorian calendar  (issue #9)

**Files:**
- Create: `src/hebrewcal/calendars/gregorian.py`
- Test: `tests/calendars/test_gregorian.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/calendars/__init__.py` (empty) and `tests/calendars/test_gregorian.py`:

```python
"""Tests for the proleptic Gregorian calendar."""

from __future__ import annotations

import datetime

import pytest

from hebrewcal.calendars.gregorian import GregorianDate, is_leap_year


def test_epoch_round_trip() -> None:
    assert GregorianDate(1, 1, 1).to_rd() == 1
    assert GregorianDate.from_rd(1) == GregorianDate(1, 1, 1)


def test_known_rd_values() -> None:
    # Reference values cross-checked against datetime.date.toordinal().
    assert GregorianDate(1945, 11, 12).to_rd() == 710347
    assert GregorianDate(2026, 6, 26).to_rd() == 739793


def test_leap_year_rule() -> None:
    assert is_leap_year(2000) is True
    assert is_leap_year(1900) is False
    assert is_leap_year(2024) is True
    assert is_leap_year(2023) is False


def test_proleptic_negative_years() -> None:
    # Round trips must hold for years <= 0 (proleptic).
    for rd in (-100000, -365, 0, 1, 1000, 739428):
        assert GregorianDate.from_rd(rd).to_rd() == rd


def test_matches_stdlib_for_modern_dates() -> None:
    base = datetime.date(1, 1, 1).toordinal()  # stdlib proleptic Gregorian ordinal == RD
    for ord_ in (1, 100000, 700000, 739428):
        d = datetime.date.fromordinal(ord_)
        g = GregorianDate(d.year, d.month, d.day)
        assert g.to_rd() == ord_
        assert GregorianDate.from_rd(ord_) == g
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest tests/calendars/test_gregorian.py -v`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `gregorian.py`**

Create `src/hebrewcal/calendars/gregorian.py`:

```python
"""The proleptic Gregorian calendar.

Valid for all years, including years <= 0 (proleptic). The RD value matches the
Python standard-library proleptic Gregorian ordinal, which makes cross-checking
straightforward.
"""

from __future__ import annotations

from dataclasses import dataclass

from hebrewcal.core.rata_die import RD_EPOCH

_MONTH_LENGTHS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def is_leap_year(year: int) -> bool:
    """Return whether ``year`` is a Gregorian leap year."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def last_day_of_month(year: int, month: int) -> int:
    """Return the number of days in ``month`` of ``year``."""
    if month == 2 and is_leap_year(year):
        return 29
    return _MONTH_LENGTHS[month - 1]


@dataclass(frozen=True, order=True)
class GregorianDate:
    """A date in the proleptic Gregorian calendar."""

    year: int
    month: int
    day: int

    def __post_init__(self) -> None:
        if not 1 <= self.month <= 12:
            raise ValueError(f"month out of range: {self.month}")
        if not 1 <= self.day <= last_day_of_month(self.year, self.month):
            raise ValueError(f"day out of range: {self.day}")

    def to_rd(self) -> int:
        """Return the Rata Die day count for this date."""
        y = self.year
        if self.month <= 2:
            correction = 0
        elif is_leap_year(y):
            correction = -1
        else:
            correction = -2
        return (
            RD_EPOCH
            - 1
            + 365 * (y - 1)
            + (y - 1) // 4
            - (y - 1) // 100
            + (y - 1) // 400
            + (367 * self.month - 362) // 12
            + correction
            + self.day
        )

    @classmethod
    def from_rd(cls, rd: int) -> "GregorianDate":
        """Reconstruct a Gregorian date from an RD value."""
        year = _year_from_rd(rd)
        prior_days = rd - cls(year, 1, 1).to_rd()
        if rd < cls(year, 3, 1).to_rd():
            correction = 0
        elif is_leap_year(year):
            correction = 1
        else:
            correction = 2
        month = (12 * (prior_days + correction) + 373) // 367
        day = rd - cls(year, month, 1).to_rd() + 1
        return cls(year, month, day)


def _year_from_rd(rd: int) -> int:
    """Return the Gregorian year containing the given RD value."""
    d0 = rd - RD_EPOCH
    n400, d1 = divmod(d0, 146097)
    n100, d2 = divmod(d1, 36524)
    n4, d3 = divmod(d2, 1461)
    n1 = d3 // 365
    year = 400 * n400 + 100 * n100 + 4 * n4 + n1
    if n100 == 4 or n1 == 4:
        return year
    return year + 1
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `pytest tests/calendars/test_gregorian.py -v`
Expected: PASS (5 tests).

- [ ] **Step 5: Run the gate and commit**

```bash
flake8 && ruff check . && mypy && pytest -q
git add src/hebrewcal/calendars/gregorian.py tests/calendars/
git commit -m "feat(calendars): add proleptic Gregorian calendar

Closes #9"
```

---

## Task 3: Julian calendar with reform handling  (issue #10)

**Files:**
- Create: `src/hebrewcal/calendars/julian.py`
- Test: `tests/calendars/test_julian.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/calendars/test_julian.py`:

```python
"""Tests for the proleptic Julian calendar and the reform helper."""

from __future__ import annotations

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars.julian import (
    JULIAN_EPOCH,
    JulianDate,
    is_leap_year,
    last_gregorian_before_reform,
)


def test_epoch_value() -> None:
    # Julian 1 Jan 1 sits one day before the Gregorian epoch.
    assert JULIAN_EPOCH == -1
    assert JulianDate(1, 1, 1).to_rd() == -1


def test_leap_year_rule_handles_no_year_zero() -> None:
    assert is_leap_year(4) is True
    assert is_leap_year(3) is False
    assert is_leap_year(1900) is True  # Julian: every 4th year is leap
    assert is_leap_year(-1) is True    # proleptic: year -1 is leap (maps to BCE pattern)


def test_round_trip_including_proleptic() -> None:
    for rd in (-200000, -1, 0, 1, 700000, 739428):
        assert JulianDate.from_rd(rd).to_rd() == rd


def test_reform_offset_1582() -> None:
    # The 1582 reform: Julian Thursday 4 Oct 1582 was followed by
    # Gregorian Friday 15 Oct 1582 — the same RD, +10 day label difference.
    julian_last = JulianDate(1582, 10, 4)
    gregorian_first = GregorianDate(1582, 10, 15)
    assert julian_last.to_rd() + 1 == gregorian_first.to_rd()


def test_reform_helper() -> None:
    # The default reform cutover returns the last Gregorian date that is still
    # written using the Julian calendar in the given locale model.
    assert last_gregorian_before_reform() == GregorianDate(1582, 10, 4)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest tests/calendars/test_julian.py -v`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `julian.py`**

Create `src/hebrewcal/calendars/julian.py`:

```python
"""The proleptic Julian calendar with explicit reform handling.

The library never performs a silent Julian/Gregorian switch. Everything is
computed through RD; the historical 1582 (and later, regional) reform is exposed
as an explicit, configurable helper so callers decide when the cutover applies.
"""

from __future__ import annotations

from dataclasses import dataclass

from hebrewcal.calendars.gregorian import GregorianDate

# RD of Julian 1 January 1 == Gregorian 30 December 0 == -1.
JULIAN_EPOCH: int = -1

_MONTH_LENGTHS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def is_leap_year(year: int) -> bool:
    """Return whether ``year`` is a Julian leap year (proleptic, no year 0)."""
    if year > 0:
        return year % 4 == 0
    # There is no year 0; proleptically, leap years satisfy year % 4 == 3.
    return year % 4 == 3


def last_day_of_month(year: int, month: int) -> int:
    """Return the number of days in ``month`` of ``year``."""
    if month == 2 and is_leap_year(year):
        return 29
    return _MONTH_LENGTHS[month - 1]


@dataclass(frozen=True, order=True)
class JulianDate:
    """A date in the proleptic Julian calendar."""

    year: int
    month: int
    day: int

    def __post_init__(self) -> None:
        if self.year == 0:
            raise ValueError("Julian calendar has no year 0")
        if not 1 <= self.month <= 12:
            raise ValueError(f"month out of range: {self.month}")
        if not 1 <= self.day <= last_day_of_month(self.year, self.month):
            raise ValueError(f"day out of range: {self.day}")

    def to_rd(self) -> int:
        """Return the Rata Die day count for this date."""
        y = self.year + 1 if self.year < 0 else self.year
        if self.month <= 2:
            correction = 0
        elif is_leap_year(self.year):
            correction = -1
        else:
            correction = -2
        return (
            JULIAN_EPOCH
            - 1
            + 365 * (y - 1)
            + (y - 1) // 4
            + (367 * self.month - 362) // 12
            + correction
            + self.day
        )

    @classmethod
    def from_rd(cls, rd: int) -> "JulianDate":
        """Reconstruct a Julian date from an RD value."""
        approx = (4 * (rd - JULIAN_EPOCH) + 1464) // 1461
        year = approx - 1 if approx <= 0 else approx
        prior_days = rd - cls(year, 1, 1).to_rd()
        if rd < cls(year, 3, 1).to_rd():
            correction = 0
        elif is_leap_year(year):
            correction = 1
        else:
            correction = 2
        month = (12 * (prior_days + correction) + 373) // 367
        day = rd - cls(year, month, 1).to_rd() + 1
        return cls(year, month, day)


def last_gregorian_before_reform() -> GregorianDate:
    """Return the last Gregorian-labelled date before the 1582 papal cutover.

    The papal bull skipped from Julian Thursday 4 October 1582 to Gregorian
    Friday 15 October 1582. Adoption was regional and much later in many places;
    callers that need a different cutover should supply their own date. This
    helper exists so the default reference point is explicit, not implicit.
    """
    return GregorianDate(1582, 10, 4)
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `pytest tests/calendars/test_julian.py -v`
Expected: PASS (5 tests).

- [ ] **Step 5: Run the gate and commit**

```bash
flake8 && ruff check . && mypy && pytest -q
git add src/hebrewcal/calendars/julian.py tests/calendars/test_julian.py
git commit -m "feat(calendars): add proleptic Julian calendar with explicit reform helper

Closes #10"
```

---

## Task 4: Hebrew calendar arithmetic  (issue #11)

This task implements the Hebrew engine across five small modules. Build them in order;
each has its own tests.

**Files:**
- Create: `src/hebrewcal/hebrew/metonic.py`
- Create: `src/hebrewcal/hebrew/molad.py`
- Create: `src/hebrewcal/hebrew/dechiyot.py`
- Create: `src/hebrewcal/hebrew/yeartype.py`
- Create: `src/hebrewcal/hebrew/keviah.py`
- Test: `tests/hebrew/test_metonic.py`, `test_molad.py`, `test_dechiyot.py`,
  `test_yeartype.py`, `test_keviah.py`

- [ ] **Step 1: Write the failing tests for the Metonic cycle**

Create `tests/hebrew/__init__.py` (empty) and `tests/hebrew/test_metonic.py`:

```python
"""Tests for the 19-year Metonic cycle."""

from __future__ import annotations

from hebrewcal.hebrew.metonic import is_leap_year, months_in_year


def test_known_leap_years() -> None:
    # Verified with the rule: a year is leap iff (7*y + 1) % 19 < 7.
    assert is_leap_year(5782) is True
    assert is_leap_year(5784) is True
    assert is_leap_year(5787) is True
    assert is_leap_year(5783) is False
    assert is_leap_year(5785) is False
    assert is_leap_year(5786) is False


def test_leap_year_pattern_over_one_cycle() -> None:
    # Exactly 7 leap years occur in any 19 consecutive years.
    leaps = [y for y in range(5701, 5720) if is_leap_year(y)]
    assert len(leaps) == 7


def test_months_in_year() -> None:
    assert months_in_year(5784) == 13  # leap
    assert months_in_year(5785) == 12  # common
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest tests/hebrew/test_metonic.py -v`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `metonic.py`**

Create `src/hebrewcal/hebrew/metonic.py`:

```python
"""The 19-year Metonic cycle.

Seven of every nineteen Hebrew years are leap years (a 13th month, Adar I, is
inserted). A year ``y`` is leap iff ``(7 * y + 1) mod 19 < 7``.
"""

from __future__ import annotations


def is_leap_year(year: int) -> bool:
    """Return whether the Hebrew ``year`` is a leap (13-month) year."""
    return (7 * year + 1) % 19 < 7


def months_in_year(year: int) -> int:
    """Return the number of months in the Hebrew ``year`` (12 or 13)."""
    return 13 if is_leap_year(year) else 12
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `pytest tests/hebrew/test_metonic.py -v`
Expected: PASS (3 tests).

- [ ] **Step 5: Write the failing tests for molad / elapsed days**

Create `tests/hebrew/test_molad.py`:

```python
"""Tests for the molad and calendar-elapsed-days computation."""

from __future__ import annotations

from hebrewcal.hebrew.molad import (
    HALAKIM_PER_DAY,
    HALAKIM_PER_HOUR,
    calendar_elapsed_days,
    molad_parts,
)


def test_halakim_constants() -> None:
    assert HALAKIM_PER_HOUR == 1080
    assert HALAKIM_PER_DAY == 25920  # 1080 * 24


def test_elapsed_days_monotonic() -> None:
    # Elapsed days must strictly increase year over year.
    prev = calendar_elapsed_days(1)
    for year in range(2, 50):
        cur = calendar_elapsed_days(year)
        assert cur > prev
        prev = cur


def test_molad_parts_within_a_day() -> None:
    # The fractional part of any molad is a valid number of halakim in a day.
    parts = molad_parts(5785, 7)  # molad of Tishri 5785
    assert 0 <= parts % HALAKIM_PER_DAY < HALAKIM_PER_DAY
```

- [ ] **Step 6: Run the tests to verify they fail**

Run: `pytest tests/hebrew/test_molad.py -v`
Expected: FAIL — module not found.

- [ ] **Step 7: Implement `molad.py`**

Create `src/hebrewcal/hebrew/molad.py`:

```python
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
    """Return days from the Hebrew epoch to Tishri 1 of ``year`` before year-length
    correction, with the molad-zaken adjustment applied."""
    months_elapsed = months_until(year)
    parts_elapsed = 12084 + 13753 * months_elapsed
    day = 29 * months_elapsed + parts_elapsed // HALAKIM_PER_DAY
    # Molad-zaken / partial lo-ADU: if 3*(day+1) mod 7 < 3, postpone one day.
    if (3 * (day + 1)) % 7 < 3:
        return day + 1
    return day
```

- [ ] **Step 8: Run the tests to verify they pass**

Run: `pytest tests/hebrew/test_molad.py -v`
Expected: PASS (3 tests).

- [ ] **Step 9: Write the failing tests for the dechiyot (year-length correction)**

Create `tests/hebrew/test_dechiyot.py`:

```python
"""Tests for the four postponement rules expressed as year-length correction."""

from __future__ import annotations

from hebrewcal.hebrew.dechiyot import year_length_correction


def test_correction_is_in_known_set() -> None:
    # The correction is always 0, 1, or 2 days.
    for year in range(5700, 5800):
        assert year_length_correction(year) in (0, 1, 2)
```

- [ ] **Step 10: Run the test to verify it fails**

Run: `pytest tests/hebrew/test_dechiyot.py -v`
Expected: FAIL — module not found.

- [ ] **Step 11: Implement `dechiyot.py`**

Create `src/hebrewcal/hebrew/dechiyot.py`:

```python
"""The four postponement rules (dechiyot), expressed as a year-length correction.

Rosh Hashanah cannot fall on certain weekdays, and two cases adjust the length
of the year so that no year is illegally short or long. Together with the
molad-zaken adjustment inside ``calendar_elapsed_days`` these implement the
classical "four gates". The correction here adds 0, 1, or 2 days based on the
gap between consecutive years' elapsed-day counts (Dershowitz & Reingold).
"""

from __future__ import annotations

from hebrewcal.hebrew.molad import calendar_elapsed_days


def year_length_correction(year: int) -> int:
    """Return the 0, 1, or 2 day correction applied to ``year``'s new year."""
    ny0 = calendar_elapsed_days(year - 1)
    ny1 = calendar_elapsed_days(year)
    ny2 = calendar_elapsed_days(year + 1)
    if ny2 - ny1 == 356:
        # A year that would otherwise be 356 days long is postponed two days.
        return 2
    if ny1 - ny0 == 382:
        # A year that would otherwise be 382 days long is postponed one day.
        return 1
    return 0
```

- [ ] **Step 12: Run the test to verify it passes**

Run: `pytest tests/hebrew/test_dechiyot.py -v`
Expected: PASS.

- [ ] **Step 13: Write the failing tests for year type / month lengths**

Create `tests/hebrew/test_yeartype.py`:

```python
"""Tests for new-year RD, year length and month lengths."""

from __future__ import annotations

from hebrewcal.hebrew.yeartype import (
    days_in_year,
    last_day_of_month,
    last_month_of_year,
    new_year_rd,
)


def test_new_year_strictly_increases() -> None:
    prev = new_year_rd(5700)
    for year in range(5701, 5760):
        cur = new_year_rd(year)
        assert cur > prev
        prev = cur


def test_year_lengths_are_valid() -> None:
    # Common years: 353/354/355; leap years: 383/384/385.
    for year in range(5700, 5800):
        length = days_in_year(year)
        assert length in (353, 354, 355, 383, 384, 385)


def test_last_month_of_year() -> None:
    assert last_month_of_year(5784) == 13  # leap
    assert last_month_of_year(5785) == 12  # common


def test_tishri_and_nisan_lengths() -> None:
    # Tishri (7) always 30, Nisan (1) always 30, Iyyar (2) always 29.
    assert last_day_of_month(5785, 7) == 30
    assert last_day_of_month(5785, 1) == 30
    assert last_day_of_month(5785, 2) == 29
```

- [ ] **Step 14: Run the tests to verify they fail**

Run: `pytest tests/hebrew/test_yeartype.py -v`
Expected: FAIL — module not found.

- [ ] **Step 15: Implement `yeartype.py`**

Create `src/hebrewcal/hebrew/yeartype.py`:

```python
"""Hebrew year typing: new-year RD, year length, and month lengths.

The length of a Hebrew year (353/354/355 common, 383/384/385 leap) determines
whether Marheshvan is long (30) and whether Kislev is short (29), which is what
makes a year deficient, regular, or complete.
"""

from __future__ import annotations

from hebrewcal.hebrew.dechiyot import year_length_correction
from hebrewcal.hebrew.metonic import is_leap_year, months_in_year
from hebrewcal.hebrew.molad import calendar_elapsed_days

# RD of 1 Tishri AM 1 == fixed_from_julian(-3761, 10, 7).
HEBREW_EPOCH: int = -1373427


def last_month_of_year(year: int) -> int:
    """Return the last month number of ``year`` (12 common, 13 leap)."""
    return months_in_year(year)


def new_year_rd(year: int) -> int:
    """Return the RD of 1 Tishri of the Hebrew ``year`` (Rosh Hashanah)."""
    return HEBREW_EPOCH + calendar_elapsed_days(year) + year_length_correction(year)


def days_in_year(year: int) -> int:
    """Return the number of days in the Hebrew ``year``."""
    return new_year_rd(year + 1) - new_year_rd(year)


def is_long_marheshvan(year: int) -> bool:
    """Return whether Marheshvan has 30 days in ``year``."""
    return days_in_year(year) in (355, 385)


def is_short_kislev(year: int) -> bool:
    """Return whether Kislev has 29 days in ``year``."""
    return days_in_year(year) in (353, 383)


def last_day_of_month(year: int, month: int) -> int:
    """Return the number of days in ``month`` of the Hebrew ``year``."""
    if (
        month in (2, 4, 6, 10, 13)
        or (month == 8 and not is_long_marheshvan(year))
        or (month == 9 and is_short_kislev(year))
        or (month == 12 and not is_leap_year(year))
    ):
        return 29
    return 30
```

- [ ] **Step 16: Run the tests to verify they pass**

Run: `pytest tests/hebrew/test_yeartype.py -v`
Expected: PASS (4 tests).

- [ ] **Step 17: Write the failing tests for keviah**

Create `tests/hebrew/test_keviah.py`:

```python
"""Tests for the keviah year signature."""

from __future__ import annotations

from hebrewcal.hebrew.keviah import YearKind, keviah


def test_year_kind_matches_length() -> None:
    k = keviah(5785)
    assert k.kind in (YearKind.DEFICIENT, YearKind.REGULAR, YearKind.COMPLETE)
    assert k.leap in (True, False)
    # Rosh Hashanah weekday is 0..6 and never Sunday/Wednesday/Friday (lo ADU rosh).
    assert k.rosh_hashanah_weekday in (1, 2, 4, 6)


def test_keviah_roundtrips_year_length() -> None:
    # COMPLETE -> long year, DEFICIENT -> short year.
    from hebrewcal.hebrew.yeartype import days_in_year

    for year in range(5780, 5800):
        k = keviah(year)
        length = days_in_year(year)
        if k.kind is YearKind.DEFICIENT:
            assert length in (353, 383)
        elif k.kind is YearKind.REGULAR:
            assert length in (354, 384)
        else:
            assert length in (355, 385)
```

- [ ] **Step 18: Run the tests to verify they fail**

Run: `pytest tests/hebrew/test_keviah.py -v`
Expected: FAIL — module not found.

- [ ] **Step 19: Implement `keviah.py`**

Create `src/hebrewcal/hebrew/keviah.py`:

```python
"""The keviah — the compact signature classifying a Hebrew year.

A year is classified by three facts: whether it is a leap year, the weekday of
Rosh Hashanah, and whether it is deficient (chaser), regular (kesidran), or
complete (shalem). Those three determine the entire layout of the year.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from hebrewcal.core.rata_die import weekday_from_rd
from hebrewcal.hebrew.metonic import is_leap_year
from hebrewcal.hebrew.yeartype import days_in_year, new_year_rd


class YearKind(Enum):
    """Whether a year is deficient, regular, or complete."""

    DEFICIENT = "deficient"
    REGULAR = "regular"
    COMPLETE = "complete"


@dataclass(frozen=True)
class Keviah:
    """The signature of a Hebrew year."""

    leap: bool
    rosh_hashanah_weekday: int
    kind: YearKind


def keviah(year: int) -> Keviah:
    """Return the :class:`Keviah` signature of the Hebrew ``year``."""
    length = days_in_year(year)
    if length in (353, 383):
        kind = YearKind.DEFICIENT
    elif length in (354, 384):
        kind = YearKind.REGULAR
    else:
        kind = YearKind.COMPLETE
    return Keviah(
        leap=is_leap_year(year),
        rosh_hashanah_weekday=weekday_from_rd(new_year_rd(year)),
        kind=kind,
    )
```

- [ ] **Step 20: Run the tests to verify they pass**

Run: `pytest tests/hebrew/test_keviah.py -v`
Expected: PASS.

- [ ] **Step 21: Run the gate and commit**

```bash
flake8 && ruff check . && mypy && pytest -q
git add src/hebrewcal/hebrew/ tests/hebrew/
git commit -m "feat(hebrew): add Hebrew calendar arithmetic

Implement the Metonic cycle, molad/halakim, the dechiyot year-length
correction, year typing with month lengths, and the keviah signature.

Closes #11"
```

---

## Task 5: Hebrew calendar date type  (issue #12)

**Files:**
- Create: `src/hebrewcal/calendars/hebrew.py`
- Test: `tests/calendars/test_hebrew.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/calendars/test_hebrew.py`:

```python
"""Tests for the Hebrew date type and its RD conversion."""

from __future__ import annotations

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars.hebrew import HebrewDate


def test_round_trip_over_many_years() -> None:
    # Every day of several years must round-trip through RD.
    start = HebrewDate(5780, 7, 1).to_rd()
    end = HebrewDate(5790, 7, 1).to_rd()
    for rd in range(start, end):
        assert HebrewDate.from_rd(rd).to_rd() == rd


def test_known_correspondence() -> None:
    # 1 Tishri 5785 corresponds to 3 October 2024 (Gregorian).
    rd = HebrewDate(5785, 7, 1).to_rd()
    assert GregorianDate.from_rd(rd) == GregorianDate(2024, 10, 3)


def test_leap_year_has_adar_ii() -> None:
    # 5784 is a leap year: month 13 (Adar II) exists and day 30 of Adar I is valid.
    assert HebrewDate(5784, 13, 1).to_rd() > HebrewDate(5784, 12, 1).to_rd()


def test_invalid_day_rejected() -> None:
    import pytest

    with pytest.raises(ValueError):
        HebrewDate(5785, 2, 30)  # Iyyar has 29 days
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest tests/calendars/test_hebrew.py -v`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `hebrew.py`**

Create `src/hebrewcal/calendars/hebrew.py`:

```python
"""The Hebrew calendar date type.

Month numbering is standard (Nisan = 1 ... Tishri = 7 ... Adar/Adar I = 12,
Adar II = 13). The civil year begins at Tishri. Conversion to and from RD uses
the year-typing machinery in :mod:`hebrewcal.hebrew`.
"""

from __future__ import annotations

from dataclasses import dataclass

from hebrewcal.hebrew.yeartype import (
    last_day_of_month,
    last_month_of_year,
    new_year_rd,
)

_TISHRI = 7


@dataclass(frozen=True, order=True)
class HebrewDate:
    """A date in the Hebrew calendar."""

    year: int
    month: int
    day: int

    def __post_init__(self) -> None:
        if not 1 <= self.month <= last_month_of_year(self.year):
            raise ValueError(f"month out of range: {self.month}")
        if not 1 <= self.day <= last_day_of_month(self.year, self.month):
            raise ValueError(f"day out of range: {self.day}")

    def to_rd(self) -> int:
        """Return the Rata Die day count for this date."""
        if self.month < _TISHRI:
            # Months Nisan..Elul fall in the second half of the civil year.
            months_after_tishri = range(_TISHRI, last_month_of_year(self.year) + 1)
            months_before = range(1, self.month)
        else:
            months_after_tishri = range(_TISHRI, self.month)
            months_before = range(0, 0)  # empty
        days_before = sum(
            last_day_of_month(self.year, m) for m in months_after_tishri
        ) + sum(last_day_of_month(self.year, m) for m in months_before)
        return new_year_rd(self.year) + days_before + self.day - 1

    @classmethod
    def from_rd(cls, rd: int) -> "HebrewDate":
        """Reconstruct a Hebrew date from an RD value."""
        # Estimate the year, then correct by direct comparison.
        approx = (rd - new_year_rd(1)) // 366 + 1
        year = approx
        while new_year_rd(year + 1) <= rd:
            year += 1
        while new_year_rd(year) > rd:
            year -= 1
        # Determine the starting month: Nisan (1) if on/after 1 Nisan, else Tishri (7).
        start = 1 if rd >= cls(year, 1, 1).to_rd() else _TISHRI
        month = start
        while rd > cls(year, month, last_day_of_month(year, month)).to_rd():
            month += 1
        day = rd - cls(year, month, 1).to_rd() + 1
        return cls(year, month, day)
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `pytest tests/calendars/test_hebrew.py -v`
Expected: PASS (4 tests). The full-year round-trip is the key correctness check.

- [ ] **Step 5: Run the gate and commit**

```bash
flake8 && ruff check . && mypy && pytest -q
git add src/hebrewcal/calendars/hebrew.py tests/calendars/test_hebrew.py
git commit -m "feat(calendars): add Hebrew date type with RD conversion

Closes #12"
```

---

## Task 6: Cross-calendar conversion API  (issue #13)

**Files:**
- Create: `src/hebrewcal/conversion.py`
- Modify: `src/hebrewcal/__init__.py` (export the public surface)
- Test: `tests/test_conversion.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_conversion.py`:

```python
"""Tests for the high-level conversion API, including the roadmap acceptance case."""

from __future__ import annotations

import hebrewcal
from hebrewcal import (
    GregorianDate,
    HebrewDate,
    JulianDate,
    Weekday,
    to_gregorian,
    to_hebrew,
    to_julian,
    weekday,
)


def test_public_exports_exist() -> None:
    for name in (
        "GregorianDate",
        "JulianDate",
        "HebrewDate",
        "Weekday",
        "to_gregorian",
        "to_hebrew",
        "to_julian",
        "weekday",
    ):
        assert hasattr(hebrewcal, name)


def test_acceptance_1867_10_31() -> None:
    # "What Hebrew date and weekday corresponds to 1867-10-31?"
    g = GregorianDate(1867, 10, 31)
    h = to_hebrew(g)
    assert (h.year, h.month, h.day) == (5628, 8, 2)  # 2 Marheshvan 5628
    assert weekday(g) is Weekday.THURSDAY


def test_gregorian_julian_round_trip() -> None:
    g = GregorianDate(2026, 6, 26)
    j = to_julian(g)
    assert to_gregorian(j) == g


def test_hebrew_gregorian_round_trip() -> None:
    h = HebrewDate(5785, 7, 1)
    g = to_gregorian(h)
    assert to_hebrew(g) == h
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest tests/test_conversion.py -v`
Expected: FAIL — imports missing.

- [ ] **Step 3: Implement `conversion.py`**

Create `src/hebrewcal/conversion.py`:

```python
"""High-level, ergonomic conversion between the supported calendars.

Every function routes through RD via :func:`hebrewcal.core.calendar.convert`.
"""

from __future__ import annotations

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.calendars.julian import JulianDate
from hebrewcal.core.calendar import CalendarDate, Weekday, convert
from hebrewcal.core.calendar import weekday as _weekday


def to_gregorian(date: CalendarDate) -> GregorianDate:
    """Convert any supported date to a Gregorian date."""
    return convert(date, GregorianDate)


def to_julian(date: CalendarDate) -> JulianDate:
    """Convert any supported date to a Julian date."""
    return convert(date, JulianDate)


def to_hebrew(date: CalendarDate) -> HebrewDate:
    """Convert any supported date to a Hebrew date."""
    return convert(date, HebrewDate)


def weekday(date: CalendarDate) -> Weekday:
    """Return the weekday of any supported date."""
    return _weekday(date)
```

- [ ] **Step 4: Update the package exports**

Replace `src/hebrewcal/__init__.py` with:

```python
"""hebrewcal — a pure-Python library for the Hebrew calendar.

The library makes the Hebrew calendar usable programmatically and converts it
bidirectionally against the Gregorian and Julian calendars. Every computation is
performed locally; the library never issues network calls to any external service.

The whole design pivots on the Rata Die (RD) day count from Dershowitz & Reingold,
*Calendrical Calculations*: every calendar implements only ``to_rd`` and ``from_rd``,
and conversion between any two calendars always goes through RD.
"""

from __future__ import annotations

from importlib import metadata

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.calendars.julian import JulianDate
from hebrewcal.conversion import to_gregorian, to_hebrew, to_julian, weekday
from hebrewcal.core.calendar import Weekday

try:
    __version__ = metadata.version("hebrewcal")
except metadata.PackageNotFoundError:  # pragma: no cover - source checkout without install
    __version__ = "0.0.0.dev0"

__all__ = [
    "__version__",
    "GregorianDate",
    "JulianDate",
    "HebrewDate",
    "Weekday",
    "to_gregorian",
    "to_julian",
    "to_hebrew",
    "weekday",
]
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `pytest tests/test_conversion.py -v`
Expected: PASS (4 tests). If `test_acceptance_1867_10_31` fails on the Hebrew tuple,
recompute by hand from RD: do not change the algorithm — verify the expected value with an
independent reference and correct the test's expected tuple if (and only if) the reference
disagrees.

- [ ] **Step 6: Run the gate and commit**

```bash
flake8 && ruff check . && mypy && pytest -q
git add src/hebrewcal/conversion.py src/hebrewcal/__init__.py tests/test_conversion.py
git commit -m "feat: add cross-calendar conversion API

Closes #13"
```

---

## Task 7: Date input parsing  (issue #14)

**Files:**
- Create: `src/hebrewcal/parsing/dates.py`
- Test: `tests/parsing/test_dates.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/parsing/__init__.py` (empty) and `tests/parsing/test_dates.py`:

```python
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
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest tests/parsing/test_dates.py -v`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `dates.py`**

Create `src/hebrewcal/parsing/dates.py`:

```python
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
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `pytest tests/parsing/test_dates.py -v`
Expected: PASS (5 tests).

- [ ] **Step 5: Run the gate and commit**

```bash
flake8 && ruff check . && mypy && pytest -q
git add src/hebrewcal/parsing/dates.py tests/parsing/
git commit -m "feat(parsing): parse ISO 8601, DIN 5008 and slash-form Gregorian dates

Closes #14"
```

---

## Task 8: Date formatting  (issue #15)

This task depends on the name tables (Task 10). If executing strictly in order, do Task 10
first, then return here. The plan keeps formatting here for narrative flow; the
implementer may reorder Tasks 8 and 10.

**Files:**
- Create: `src/hebrewcal/formatting/dates.py`
- Test: `tests/formatting/test_dates.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/formatting/__init__.py` (empty) and `tests/formatting/test_dates.py`:

```python
"""Tests for date formatting."""

from __future__ import annotations

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.formatting.dates import format_gregorian, format_hebrew


def test_iso_format() -> None:
    assert format_gregorian(GregorianDate(2026, 6, 26), style="iso") == "2026-06-26"


def test_din_format() -> None:
    assert format_gregorian(GregorianDate(2026, 6, 26), style="din") == "26.06.2026"


def test_hebrew_named_format() -> None:
    # 1 Tishri 5785 with standard transliterated month name.
    text = format_hebrew(HebrewDate(5785, 7, 1), style="named")
    assert "Tishri" in text
    assert "5785" in text


def test_hebrew_leap_month_naming() -> None:
    # Month 12 in a leap year is "Adar I", month 13 is "Adar II".
    assert "Adar I" in format_hebrew(HebrewDate(5784, 12, 1), style="named")
    assert "Adar II" in format_hebrew(HebrewDate(5784, 13, 1), style="named")
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest tests/formatting/test_dates.py -v`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `dates.py`**

Create `src/hebrewcal/formatting/dates.py`:

```python
"""Render dates in numeric and named output formats."""

from __future__ import annotations

from typing import Literal

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.names import hebrew_month_name

GregorianStyle = Literal["iso", "din"]
HebrewStyle = Literal["named", "numeric"]


def format_gregorian(date: GregorianDate, style: GregorianStyle = "iso") -> str:
    """Format a Gregorian date as ISO 8601 or DIN 5008."""
    if style == "iso":
        return f"{date.year:04d}-{date.month:02d}-{date.day:02d}"
    if style == "din":
        return f"{date.day:02d}.{date.month:02d}.{date.year:04d}"
    raise ValueError(f"unknown style: {style!r}")


def format_hebrew(date: HebrewDate, style: HebrewStyle = "named") -> str:
    """Format a Hebrew date numerically or with a transliterated month name."""
    if style == "numeric":
        return f"{date.year}-{date.month:02d}-{date.day:02d}"
    if style == "named":
        name = hebrew_month_name(date.year, date.month, system="transliteration")
        return f"{date.day} {name} {date.year}"
    raise ValueError(f"unknown style: {style!r}")
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `pytest tests/formatting/test_dates.py -v`
Expected: PASS (4 tests). Requires `hebrewcal.names` from Task 10.

- [ ] **Step 5: Run the gate and commit**

```bash
flake8 && ruff check . && mypy && pytest -q
git add src/hebrewcal/formatting/dates.py tests/formatting/
git commit -m "feat(formatting): add numeric and named date formatting

Closes #15"
```

---

## Task 9: Hebrew numerals / gematria converter  (issue #16)

**Files:**
- Create: `src/hebrewcal/numerals.py`
- Test: `tests/test_numerals.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_numerals.py`:

```python
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
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest tests/test_numerals.py -v`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `numerals.py`**

Create `src/hebrewcal/numerals.py`:

```python
"""Convert between integers and Hebrew numerals (gematria).

Hebrew numerals are additive letter values. Conventions implemented here:
- 15 and 16 are written ט״ו and ט״ז (9+6, 9+7) to avoid spelling fragments of
  the divine name.
- A geresh (׳) marks a single-letter number; a gershayim (״) is inserted before
  the last letter of a multi-letter number.
- Thousands are written as the hundreds-or-less value followed by a geresh, then
  the remainder (e.g. 5785 -> ה׳תשפ״ה).
"""

from __future__ import annotations

GERESH = "׳"  # ׳
GERSHAYIM = "״"  # ״

# Letter values in descending order. Note 15/16 are handled specially below.
_VALUES: tuple[tuple[int, str], ...] = (
    (400, "ת"),  # ת
    (300, "ש"),  # ש
    (200, "ר"),  # ר
    (100, "ק"),  # ק
    (90, "צ"),   # צ
    (80, "פ"),   # פ
    (70, "ע"),   # ע
    (60, "ס"),   # ס
    (50, "נ"),   # נ
    (40, "מ"),   # מ
    (30, "ל"),   # ל
    (20, "כ"),   # כ
    (10, "י"),   # י
    (9, "ט"),    # ט
    (8, "ח"),    # ח
    (7, "ז"),    # ז
    (6, "ו"),    # ו
    (5, "ה"),    # ה
    (4, "ד"),    # ד
    (3, "ג"),    # ג
    (2, "ב"),    # ב
    (1, "א"),    # א
)
_LETTER_TO_VALUE = {letter: value for value, letter in _VALUES}


def _letters_for(value: int) -> str:
    """Return the bare letters (no punctuation) for 1..999."""
    out: list[str] = []
    remaining = value
    for amount, letter in _VALUES:
        # Special-case the tens-and-units 15 and 16.
        if remaining in (15, 16):
            out.append("ט")  # ט (9)
            out.append("ו" if remaining == 15 else "ז")  # ו / ז
            remaining = 0
            break
        while remaining >= amount:
            out.append(letter)
            remaining -= amount
    return "".join(out)


def _punctuate(letters: str) -> str:
    """Add geresh/gershayim to a bare letter string."""
    if len(letters) == 1:
        return letters + GERESH
    return letters[:-1] + GERSHAYIM + letters[-1]


def _sum_letters(letters: str, text: str) -> int:
    """Sum the values of bare numeral letters, raising on any non-letter."""
    total = 0
    for char in letters:
        value = _LETTER_TO_VALUE.get(char)
        if value is None:
            raise ValueError(f"not a Hebrew numeral: {text!r}")
        total += value
    return total


def to_hebrew_numeral(number: int) -> str:
    """Convert a positive integer to its Hebrew numeral string.

    Note: an exact multiple of 1000 with no remainder (e.g. 1000) is ambiguous in
    this additive notation and round-trips to its sub-1000 value; year-style
    numbers (a thousands group followed by a remainder, e.g. 5785) are
    unambiguous.
    """
    if number <= 0:
        raise ValueError("Hebrew numerals represent positive integers only")
    thousands, rest = divmod(number, 1000)
    parts: list[str] = []
    if thousands:
        parts.append(_letters_for(thousands) + GERESH)
    if rest:
        parts.append(_punctuate(_letters_for(rest)))
    return "".join(parts)


def from_hebrew_numeral(text: str) -> int:
    """Convert a Hebrew numeral string back to an integer."""
    cleaned = text.strip().replace(GERSHAYIM, "")
    thousands = 0
    geresh_index = cleaned.find(GERESH)
    if geresh_index != -1 and geresh_index != len(cleaned) - 1:
        # A geresh with letters after it separates the thousands group.
        thousands = _sum_letters(cleaned[:geresh_index], text)
        cleaned = cleaned[geresh_index + 1:]
    # Any remaining geresh is the single-number marker; drop it.
    cleaned = cleaned.replace(GERESH, "")
    total = thousands * 1000 + _sum_letters(cleaned, text)
    if total <= 0:
        raise ValueError(f"not a Hebrew numeral: {text!r}")
    return total
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `pytest tests/test_numerals.py -v`
Expected: PASS (5 tests). If the thousands round-trip fails, check that the geresh after
the thousands segment is the only geresh consumed as a thousands marker.

- [ ] **Step 5: Run the gate and commit**

```bash
flake8 && ruff check . && mypy && pytest -q
git add src/hebrewcal/numerals.py tests/test_numerals.py
git commit -m "feat: add Hebrew numeral (gematria) converter

Closes #16"
```

---

## Task 10: Month and day name tables  (issue #18)

**Files:**
- Create: `src/hebrewcal/names.py`
- Test: `tests/test_names.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_names.py`:

```python
"""Tests for month and weekday name tables."""

from __future__ import annotations

import pytest

from hebrewcal.names import hebrew_month_name, weekday_name


def test_standard_month_names() -> None:
    assert hebrew_month_name(5785, 7, system="transliteration") == "Tishri"
    assert hebrew_month_name(5785, 1, system="transliteration") == "Nisan"


def test_leap_year_adar_naming() -> None:
    # Month 12 in a leap year is Adar I; month 13 is Adar II.
    assert hebrew_month_name(5784, 12, system="transliteration") == "Adar I"
    assert hebrew_month_name(5784, 13, system="transliteration") == "Adar II"
    # In a common year month 12 is simply Adar.
    assert hebrew_month_name(5785, 12, system="transliteration") == "Adar"


def test_babylonian_and_biblical_systems() -> None:
    # Babylonian name of Tishri is Tashritu; a biblical name of Nisan is Aviv.
    assert hebrew_month_name(5785, 7, system="babylonian") == "Tashritu"
    assert hebrew_month_name(5785, 1, system="biblical") == "Aviv"


def test_weekday_names() -> None:
    # 0 = Sunday ... 6 = Saturday.
    assert weekday_name(0) == "Yom Rishon"
    assert weekday_name(1) == "Yom Sheni"
    assert weekday_name(6) == "Shabbat"


def test_unknown_system_rejected() -> None:
    with pytest.raises(ValueError):
        hebrew_month_name(5785, 7, system="klingon")
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest tests/test_names.py -v`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `names.py`**

Create `src/hebrewcal/names.py`:

```python
"""Month and weekday name tables in several naming systems.

Month numbering is standard (Nisan = 1 ... Tishri = 7 ... Adar/Adar I = 12,
Adar II = 13). In a leap year month 12 is "Adar I" and month 13 is "Adar II";
in a common year month 12 is simply "Adar".
"""

from __future__ import annotations

from typing import Literal

from hebrewcal.hebrew.metonic import is_leap_year

MonthSystem = Literal["transliteration", "babylonian", "biblical"]

# Indexed by month number 1..13. Index 0 is unused.
_TRANSLITERATION = (
    "",
    "Nisan", "Iyyar", "Sivan", "Tammuz", "Av", "Elul",
    "Tishri", "Marheshvan", "Kislev", "Tevet", "Shevat", "Adar", "Adar II",
)
_BABYLONIAN = (
    "",
    "Nisanu", "Ayaru", "Simanu", "Du'uzu", "Abu", "Ululu",
    "Tashritu", "Arahsamnu", "Kislimu", "Tebetu", "Shabatu", "Addaru", "Addaru II",
)
# Biblical names exist only for some months; fall back to the transliteration.
_BIBLICAL = {
    1: "Aviv",
    2: "Ziv",
    7: "Ethanim",
    8: "Bul",
}

_WEEKDAYS = (
    "Yom Rishon",   # 0 Sunday
    "Yom Sheni",    # 1 Monday
    "Yom Shlishi",  # 2 Tuesday
    "Yom Revi'i",   # 3 Wednesday
    "Yom Chamishi", # 4 Thursday
    "Yom Shishi",   # 5 Friday
    "Shabbat",      # 6 Saturday
)


def hebrew_month_name(year: int, month: int, system: MonthSystem = "transliteration") -> str:
    """Return the name of ``month`` in ``year`` for the given naming ``system``."""
    if not 1 <= month <= 13:
        raise ValueError(f"month out of range: {month}")
    if system == "transliteration":
        if month == 12 and is_leap_year(year):
            return "Adar I"
        return _TRANSLITERATION[month]
    if system == "babylonian":
        if month == 12 and is_leap_year(year):
            return "Addaru I"
        return _BABYLONIAN[month]
    if system == "biblical":
        if month == 12 and is_leap_year(year):
            return "Adar I"
        return _BIBLICAL.get(month, _TRANSLITERATION[month])
    raise ValueError(f"unknown naming system: {system!r}")


def weekday_name(weekday: int) -> str:
    """Return the Hebrew weekday name (0 = Sunday ... 6 = Saturday)."""
    if not 0 <= weekday <= 6:
        raise ValueError(f"weekday out of range: {weekday}")
    return _WEEKDAYS[weekday]
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `pytest tests/test_names.py -v`
Expected: PASS (5 tests).

- [ ] **Step 5: Run the gate and commit**

```bash
flake8 && ruff check . && mypy && pytest -q
git add src/hebrewcal/names.py tests/test_names.py
git commit -m "feat: add month and weekday name tables

Add standard transliteration, Babylonian and biblical month names with
leap-year Adar I/II handling, plus Hebrew weekday names.

Closes #18"
```

---

## Task 11: Anno Mundi era with documented missing-years handling  (issue #19)

**Files:**
- Create: `src/hebrewcal/eras/anno_mundi.py`
- Test: `tests/eras/test_anno_mundi.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/eras/__init__.py` (empty) and `tests/eras/test_anno_mundi.py`:

```python
"""Tests for the Anno Mundi era helpers."""

from __future__ import annotations

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.eras.anno_mundi import (
    MISSING_YEARS_NOTICE,
    anno_mundi_year,
    traditional_vs_academic_gap,
)


def test_am_year_is_hebrew_year() -> None:
    # AM year is simply the Hebrew year number.
    h = HebrewDate(5785, 7, 1)
    assert anno_mundi_year(h) == 5785


def test_missing_years_gap_constant() -> None:
    # The traditional reckoning is ~165 years short for the Persian period.
    assert traditional_vs_academic_gap() == 165


def test_notice_is_nonempty_and_documented() -> None:
    assert isinstance(MISSING_YEARS_NOTICE, str)
    assert "missing years" in MISSING_YEARS_NOTICE.lower()


def test_known_epoch_correspondence() -> None:
    # 1 Tishri AM 1 is, by this computation, 7 October 3761 BCE (Julian),
    # i.e. proleptic. Here we only assert the AM year of a modern Hebrew date.
    g = GregorianDate(2024, 10, 3)
    from hebrewcal.conversion import to_hebrew

    assert anno_mundi_year(to_hebrew(g)) == 5785
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest tests/eras/test_anno_mundi.py -v`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `anno_mundi.py`**

Create `src/hebrewcal/eras/anno_mundi.py`:

```python
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
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `pytest tests/eras/test_anno_mundi.py -v`
Expected: PASS (4 tests).

- [ ] **Step 5: Run the gate and commit**

```bash
flake8 && ruff check . && mypy && pytest -q
git add src/hebrewcal/eras/anno_mundi.py tests/eras/
git commit -m "feat(eras): add Anno Mundi era with documented missing-years notice

Closes #19"
```

---

## Task 12: Reference-date validation test suite  (issue #20)

**Files:**
- Create: `tests/test_reference_dates.py`

- [ ] **Step 1: Write the comprehensive reference test**

Create `tests/test_reference_dates.py`:

```python
"""Cross-checked reference dates and round-trip properties for all calendars.

The Gregorian RD values are cross-checked against the Python standard library's
proleptic Gregorian ordinal, which is independent of this library's arithmetic.
The Hebrew/Gregorian correspondences are well-known fixed points.
"""

from __future__ import annotations

import datetime

import pytest

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.calendars.julian import JulianDate
from hebrewcal.conversion import to_gregorian, to_hebrew


@pytest.mark.parametrize("ordinal", [1, 1000, 100000, 700000, 710347, 739428])
def test_gregorian_matches_stdlib(ordinal: int) -> None:
    d = datetime.date.fromordinal(ordinal)
    g = GregorianDate(d.year, d.month, d.day)
    assert g.to_rd() == ordinal
    assert GregorianDate.from_rd(ordinal) == g


@pytest.mark.parametrize(
    "greg,heb",
    [
        ((2024, 10, 3), (5785, 7, 1)),    # 1 Tishri 5785
        ((1867, 10, 31), (5628, 8, 2)),   # roadmap acceptance example
        ((2026, 6, 26), (5786, 4, 11)),   # cross-checked fixed point
    ],
)
def test_known_hebrew_correspondences(
    greg: tuple[int, int, int], heb: tuple[int, int, int]
) -> None:
    g = GregorianDate(*greg)
    h = to_hebrew(g)
    assert (h.year, h.month, h.day) == heb
    assert to_gregorian(HebrewDate(*heb)) == g


def test_hebrew_full_range_round_trip() -> None:
    start = HebrewDate(5700, 7, 1).to_rd()
    end = HebrewDate(5820, 7, 1).to_rd()
    for rd in range(start, end, 7):  # sample weekly to keep the test fast
        assert HebrewDate.from_rd(rd).to_rd() == rd


def test_julian_gregorian_reform_alignment() -> None:
    assert JulianDate(1582, 10, 4).to_rd() + 1 == GregorianDate(1582, 10, 15).to_rd()


@pytest.mark.parametrize("rd", [-200000, -1373427, -1000, 0, 1, 500000, 739428])
def test_all_calendars_round_trip(rd: int) -> None:
    assert GregorianDate.from_rd(rd).to_rd() == rd
    assert JulianDate.from_rd(rd).to_rd() == rd
    assert HebrewDate.from_rd(rd).to_rd() == rd
```

- [ ] **Step 2: Run the test**

Run: `pytest tests/test_reference_dates.py -v`
Expected: PASS. The three correspondences here were verified independently while writing
this plan (cross-checked against an external Hebrew-date reference and, for Gregorian RD,
against `datetime.date.toordinal()`). If a row nonetheless fails, do NOT change the
algorithm — re-verify the expected `(year, month, day)` against an independent reference
and correct only the expected tuple.

- [ ] **Step 3: Run the full suite with coverage and commit**

```bash
flake8 && ruff check . && mypy && pytest --cov --cov-report=term-missing
git add tests/test_reference_dates.py
git commit -m "test: add cross-checked reference-date validation suite

Closes #20"
```

---

## Phase 1 completion

- [ ] All twelve issues (#8–#16, #18, #19, #20) closed.
- [ ] Open a pull request `feature/phase-1-core` → `development`; reference all closed
      issues; wait for green CI; merge and delete the branch.
- [ ] Update `CHANGELOG.md` under `[Unreleased]` with the Phase 1 additions.
- [ ] Manually close any issues not auto-closed (merges target `development`, not the
      default branch).

---

## Notes on correctness and references

- All calendar arithmetic follows Dershowitz & Reingold, *Calendrical Calculations*
  (4th ed.). RD 1 = Monday, 1 January 1 (proleptic Gregorian).
- The Hebrew epoch RD is **-1373427** (1 Tishri AM 1).
- Gregorian RD values are independently checkable against
  `datetime.date.toordinal()` / `fromordinal()`, which use the same proleptic
  Gregorian ordinal as RD.
- Where a test embeds an expected Hebrew/Gregorian correspondence, the expected value is
  the thing to verify against an external reference — never the algorithm. The algorithms
  here are the standard published ones; a mismatch almost always means a mistyped expected
  value.
