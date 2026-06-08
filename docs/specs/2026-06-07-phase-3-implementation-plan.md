# Phase 3 — Holidays — Implementation Plan

> **For implementers:** Execute task by task. Steps use checkbox (`- [ ]`) syntax. Each
> task is test-driven: write the failing test, watch it fail, implement the minimum to
> pass, run the gate (`flake8 && ruff check . && mypy && pytest`) and commit (chain with
> `&&` so a failing gate blocks the commit). Use `datetime.UTC`, not
> `datetime.timezone.utc`. Tests are type-checked under mypy strict — narrow `… | None`
> with explicit asserts before use.

**Goal:** A holiday engine for the Hebrew year — major and minor festivals (Israel vs
Diaspora), fasts with postponement, modern Israeli days, minority feasts, Rosh Chodesh,
the Omer count and the special Shabbatot — built on the calendar core, with no runtime
dependencies.

**Architecture:** Each category is a function `(_major / _minor / _fasts / _modern /
_minority / _special_shabbatot / rosh_chodesh)` that returns `list[Holiday]` for a Hebrew
year; `holidays(year, diaspora=True)` concatenates them and sorts chronologically by RD.
A `Holiday` records a name, a `HebrewDate` and a `Category`. Month numbering is the
library standard (Nisan = 1 … Tishri = 7 … Adar/Adar I = 12, Adar II = 13). In a leap
year Purim and its neighbours are in Adar II.

**Tech stack:** Python 3.11+, standard library only.

**Issue map:** Task 1 → #39 (model + engine + Rosh Chodesh) · Task 2 → #40 · Task 3 → #41 ·
Task 4 → #42 · Task 5 → #43 · Task 6 → #44 · Task 7 → #45 · Task 8 → #46 · Task 9 → #47.
(Rosh Chodesh is implemented with the engine in Task 1 because it is foundational and
purely date-driven; issue #41 then covers the minor *festivals*.)

**Conventions:** Branch `feature/phase-3-holidays` off `development`; commit per task; all
English; no attribution lines.

### Verified reference data (cross-checked against `pyluach`)

Holiday Hebrew dates for **5785** (a common year), with Israel/Diaspora differences and
the Tzom Gedaliah postponement (3 Tishri is Shabbat → 4 Tishri):

| Holiday | Hebrew date (m/d) | Notes |
|---------|-------------------|-------|
| Rosh Hashanah | 7/1, 7/2 | both |
| Tzom Gedaliah | 7/4 | postponed (3 Tishri = Sat) |
| Yom Kippur | 7/10 | |
| Sukkot | 7/15 … 7/21 | 7/15(+7/16 Diaspora) yom tov |
| Shemini Atzeret | 7/22 | |
| Simchat Torah | 7/22 Israel, 7/23 Diaspora | |
| Hanukkah | 9/25 … 10/2 | 8 days (Kislev 30 ⇒ long) |
| Asara B'Tevet | 10/10 | |
| Tu BiShvat | 11/15 | |
| Ta'anit Esther | 12/13 | |
| Purim | 12/14 | Shushan Purim 12/15 |
| Pesach | 1/15 … 1/21 (Israel), … 1/22 (Diaspora) | |
| Pesach Sheni | 2/14 | Lag BaOmer 2/18 |
| Shavuot | 3/6 (Israel), 3/6–3/7 (Diaspora) | |
| Shiva Asar B'Tammuz | 4/17 | |
| Tisha B'Av | 5/9 | |
| Tu B'Av | 5/15 | |

Leap-year **5784**: Purim Katan 12/14 (Adar I), Ta'anit Esther 13/11 (moved; 13 Adar II =
Sat), Purim 13/14, Shushan Purim 13/15. Tisha B'Av is observed on **10 Av** (postponed) in
5782, 5789, 5792.

Modern Israeli days — rules verified to reproduce the known 2024/2025 official dates:

| Year | Yom HaShoah | Yom HaZikaron | Yom HaAtzmaut | Yom Yerushalayim |
|------|-------------|---------------|---------------|------------------|
| 5784 | 28 Nisan (Mon, 2024-05-06) | 5 Iyyar (Mon, 2024-05-13) | 6 Iyyar (Tue, 2024-05-14) | 28 Iyyar (2024-06-05) |
| 5785 | 26 Nisan (Thu, 2025-04-24) | 2 Iyyar (Wed, 2025-04-30) | 3 Iyyar (Thu, 2025-05-01) | 28 Iyyar (2025-05-26) |
| 5786 | 27 Nisan (Tue, 2026-04-14) | 4 Iyyar (Tue, 2026-04-21) | 5 Iyyar (Wed, 2026-04-22) | 28 Iyyar (2026-05-15) |

---

## File Structure

| File | Responsibility |
|------|----------------|
| `src/hebrewcal/religious/holidays.py` | `Category`, `Holiday`, the category functions, `rosh_chodesh`, `holidays`, `holidays_on`. |
| `src/hebrewcal/religious/omer.py` | The Omer count. |
| `tests/religious/...` | One test module per concern, plus `test_reference_holidays.py`. |

---

## Task 1: Holiday model, engine and Rosh Chodesh  (issue #39)

**Files:** Create `src/hebrewcal/religious/holidays.py`; test `tests/religious/test_engine.py`.

- [ ] **Step 1: Failing test**

Create `tests/religious/__init__.py` (empty) and `tests/religious/test_engine.py`:

```python
"""Tests for the holiday model, engine and Rosh Chodesh."""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.religious.holidays import Category, Holiday, holidays, holidays_on, rosh_chodesh


def test_holiday_is_frozen_and_typed() -> None:
    h = Holiday("Test", HebrewDate(5785, 7, 1), Category.MAJOR_FESTIVAL)
    assert h.name == "Test"
    assert h.date == HebrewDate(5785, 7, 1)
    assert h.category is Category.MAJOR_FESTIVAL


def test_rosh_chodesh_two_days_when_prev_month_long() -> None:
    # Kislev 5785 has 30 days, so Rosh Chodesh Tevet is 30 Kislev + 1 Tevet.
    names = {(h.date.month, h.date.day) for h in rosh_chodesh(5785)}
    assert (9, 30) in names  # 30 Kislev
    assert (10, 1) in names  # 1 Tevet


def test_rosh_chodesh_excludes_tishri() -> None:
    # 1 Tishri is Rosh Hashanah, never labelled Rosh Chodesh.
    assert all(not (h.date.month == 7 and h.date.day == 1) for h in rosh_chodesh(5785))


def test_holidays_sorted_chronologically() -> None:
    days = holidays(5785)
    rds = [h.date.to_rd() for h in days]
    assert rds == sorted(rds)


def test_holidays_on_returns_matches() -> None:
    found = holidays_on(HebrewDate(5785, 7, 1))
    assert any(h.name == "Rosh Hashanah" for h in found)
```

- [ ] **Step 2: Run — expect failure** (`pytest tests/religious/test_engine.py`).

- [ ] **Step 3: Implement `holidays.py`** (model, engine, Rosh Chodesh, and the major
festivals provider so `holidays_on` can find Rosh Hashanah):

```python
"""The holiday engine for the Hebrew year.

Each category contributes a list of :class:`Holiday` for a given Hebrew year;
:func:`holidays` aggregates and sorts them chronologically. Month numbering is the
library standard (Nisan = 1 ... Tishri = 7 ... Adar / Adar I = 12, Adar II = 13).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.hebrew.metonic import is_leap_year
from hebrewcal.hebrew.yeartype import last_day_of_month, last_month_of_year


class Category(Enum):
    """The kind of observance."""

    MAJOR_FESTIVAL = "major_festival"
    CHOL_HAMOED = "chol_hamoed"
    MINOR_FESTIVAL = "minor_festival"
    FAST = "fast"
    MODERN = "modern"
    ROSH_CHODESH = "rosh_chodesh"
    SPECIAL_SHABBAT = "special_shabbat"
    MINORITY = "minority"


@dataclass(frozen=True)
class Holiday:
    """A single observance on a specific Hebrew date."""

    name: str
    date: HebrewDate
    category: Category


def rosh_chodesh(year: int) -> list[Holiday]:
    """Return the Rosh Chodesh days of the year (one or two per month, not Tishri).

    When the preceding month has 30 days, its 30th is the first of the two Rosh
    Chodesh days. The civil-year month order is Tishri … Elul; 1 Tishri is Rosh
    Hashanah and is never labelled Rosh Chodesh.
    """
    out: list[Holiday] = []
    months = list(range(7, last_month_of_year(year) + 1)) + list(range(1, 7))
    for month in months:
        if month == 7:
            continue  # 1 Tishri is Rosh Hashanah
        prev = month - 1 if month != 1 else last_month_of_year(year)
        if last_day_of_month(year, prev) == 30:
            out.append(Holiday("Rosh Chodesh", HebrewDate(year, prev, 30), Category.ROSH_CHODESH))
        out.append(Holiday("Rosh Chodesh", HebrewDate(year, month, 1), Category.ROSH_CHODESH))
    return out


def holidays(year: int, diaspora: bool = True) -> list[Holiday]:
    """Return all observances of the Hebrew ``year``, sorted chronologically."""
    result: list[Holiday] = []
    result += _major(year, diaspora)
    result += rosh_chodesh(year)
    result.sort(key=lambda h: (h.date.to_rd(), h.name))
    return result


def holidays_on(date: HebrewDate, diaspora: bool = True) -> list[Holiday]:
    """Return the observances falling on the given Hebrew date."""
    return [h for h in holidays(date.year, diaspora) if h.date == date]


def _major(year: int, diaspora: bool) -> list[Holiday]:
    """Placeholder for the major festivals, implemented in Task 2."""
    return [Holiday("Rosh Hashanah", HebrewDate(year, 7, 1), Category.MAJOR_FESTIVAL),
            Holiday("Rosh Hashanah", HebrewDate(year, 7, 2), Category.MAJOR_FESTIVAL)]


# Helper retained for later tasks.
def _purim_month(year: int) -> int:
    """Return the month that carries Purim (Adar, or Adar II in a leap year)."""
    return 13 if is_leap_year(year) else 12
```

- [ ] **Step 4: Run — expect pass.**
- [ ] **Step 5: Gate + commit** — `… && git commit -m "feat(religious): add holiday model, engine and Rosh Chodesh\n\nCloses #39"`.

---

## Task 2: Major festivals (Israel vs Diaspora)  (issue #40)

**Files:** Modify `holidays.py` (`_major`); test `tests/religious/test_major.py`.

- [ ] **Step 1: Failing test**

```python
"""Tests for the major festivals."""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.religious.holidays import holidays_on


def _names(year: int, m: int, d: int, diaspora: bool) -> set[str]:
    return {h.name for h in holidays_on(HebrewDate(year, m, d), diaspora)}


def test_yom_kippur() -> None:
    assert "Yom Kippur" in _names(5785, 7, 10, True)


def test_simchat_torah_israel_vs_diaspora() -> None:
    # Israel: Simchat Torah on 22 Tishri (with Shemini Atzeret). Diaspora: 23 Tishri.
    assert "Simchat Torah" in _names(5785, 7, 22, False)   # Israel
    assert "Simchat Torah" not in _names(5785, 7, 22, True)  # Diaspora
    assert "Simchat Torah" in _names(5785, 7, 23, True)      # Diaspora


def test_pesach_eighth_day_diaspora_only() -> None:
    assert "Pesach" in _names(5785, 1, 22, True)    # 8th day, Diaspora
    assert "Pesach" not in _names(5785, 1, 22, False)  # Israel has 7 days


def test_shavuot_second_day_diaspora_only() -> None:
    assert "Shavuot" in _names(5785, 3, 7, True)
    assert "Shavuot" not in _names(5785, 3, 7, False)


def test_sukkot_and_shemini_atzeret() -> None:
    assert "Sukkot" in _names(5785, 7, 15, True)
    assert "Shemini Atzeret" in _names(5785, 7, 22, True)
```

- [ ] **Step 2: Run — expect failure** (Simchat Torah / 8th-day rules not yet present).

- [ ] **Step 3: Implement `_major`** — replace the placeholder:

```python
def _major(year: int, diaspora: bool) -> list[Holiday]:
    """Return the major festivals, honouring the diaspora second festival day."""
    out: list[Holiday] = []

    def add(name: str, month: int, day: int, category: Category = Category.MAJOR_FESTIVAL) -> None:
        out.append(Holiday(name, HebrewDate(year, month, day), category))

    # Tishri.
    add("Rosh Hashanah", 7, 1)
    add("Rosh Hashanah", 7, 2)
    add("Yom Kippur", 7, 10)
    add("Sukkot", 7, 15)
    if diaspora:
        add("Sukkot", 7, 16)
    for day in range(16 if not diaspora else 17, 22):
        add("Sukkot", 7, day, Category.CHOL_HAMOED)
    add("Hoshana Rabbah", 7, 21, Category.MINOR_FESTIVAL)
    add("Shemini Atzeret", 7, 22)
    if diaspora:
        add("Simchat Torah", 7, 23)
    else:
        add("Simchat Torah", 7, 22)

    # Nisan — Pesach (7 days in Israel, 8 in the Diaspora).
    add("Pesach", 1, 15)
    if diaspora:
        add("Pesach", 1, 16)
    for day in range(16 if not diaspora else 17, 21):
        add("Pesach", 1, day, Category.CHOL_HAMOED)
    add("Pesach", 1, 21)
    if diaspora:
        add("Pesach", 1, 22)

    # Sivan — Shavuot (1 day in Israel, 2 in the Diaspora).
    add("Shavuot", 3, 6)
    if diaspora:
        add("Shavuot", 3, 7)
    return out
```

- [ ] **Step 4: Run — expect pass.**
- [ ] **Step 5: Gate + commit** — `Closes #40`.

---

## Task 3: Minor festivals  (issue #41)

**Files:** Modify `holidays.py` (add `_minor`, wire into `holidays`); test
`tests/religious/test_minor.py`.

- [ ] **Step 1: Failing test**

```python
"""Tests for the minor festivals."""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.religious.holidays import holidays_on


def _names(year: int, m: int, d: int) -> set[str]:
    return {h.name for h in holidays_on(HebrewDate(year, m, d))}


def test_hanukkah_eight_days_common_year() -> None:
    # 5785: 25 Kislev .. 2 Tevet (Kislev is 30 days).
    assert "Hanukkah" in _names(5785, 9, 25)
    assert "Hanukkah" in _names(5785, 10, 2)


def test_purim_common_year() -> None:
    assert "Purim" in _names(5785, 12, 14)
    assert "Shushan Purim" in _names(5785, 12, 15)


def test_purim_leap_year_in_adar_ii() -> None:
    assert "Purim" in _names(5784, 13, 14)
    assert "Purim Katan" in _names(5784, 12, 14)


def test_other_minor_days() -> None:
    assert "Tu BiShvat" in _names(5785, 11, 15)
    assert "Pesach Sheni" in _names(5785, 2, 14)
    assert "Lag BaOmer" in _names(5785, 2, 18)
    assert "Tu B'Av" in _names(5785, 5, 15)
```

- [ ] **Step 2: Run — expect failure.**

- [ ] **Step 3: Implement `_minor`** and add `result += _minor(year, diaspora)` to
`holidays`:

```python
def _minor(year: int, diaspora: bool) -> list[Holiday]:
    """Return the minor (mostly rabbinic) festive days."""
    out: list[Holiday] = []

    def add(name: str, month: int, day: int) -> None:
        out.append(Holiday(name, HebrewDate(year, month, day), Category.MINOR_FESTIVAL))

    # Hanukkah: 25 Kislev for eight days. The 6th day is 30 Kislev only when Kislev is
    # long; otherwise the run rolls into Tevet a day earlier. Build it by walking RD.
    start = HebrewDate(year, 9, 25).to_rd()
    for i in range(8):
        d = HebrewDate.from_rd(start + i)
        out.append(Holiday("Hanukkah", d, Category.MINOR_FESTIVAL))

    add("Tu BiShvat", 11, 15)

    purim_month = _purim_month(year)
    if is_leap_year(year):
        # Purim Katan / Shushan Purim Katan fall in Adar I.
        add("Purim Katan", 12, 14)
        add("Shushan Purim Katan", 12, 15)
    add("Purim", purim_month, 14)
    add("Shushan Purim", purim_month, 15)

    add("Pesach Sheni", 2, 14)
    add("Lag BaOmer", 2, 18)
    add("Tu B'Av", 5, 15)
    return out
```

- [ ] **Step 4: Run — expect pass.**  - [ ] **Step 5: Gate + commit** — `Closes #41`.

---

## Task 4: Fast days with postponement  (issue #42)

**Files:** Modify `holidays.py` (add `_fasts`, wire in); test `tests/religious/test_fasts.py`.

- [ ] **Step 1: Failing test**

```python
"""Tests for the public fasts and their postponement rules."""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.religious.holidays import holidays_on


def _names(year: int, m: int, d: int) -> set[str]:
    return {h.name for h in holidays_on(HebrewDate(year, m, d))}


def test_tzom_gedaliah_postponed_when_on_shabbat() -> None:
    # 5785: 3 Tishri is Shabbat, so the fast is on 4 Tishri.
    assert "Tzom Gedaliah" in _names(5785, 7, 4)
    assert "Tzom Gedaliah" not in _names(5785, 7, 3)


def test_tisha_bav_postponed() -> None:
    # 5782/5789/5792: 9 Av is Shabbat, observed on 10 Av.
    assert "Tisha B'Av" in _names(5782, 5, 10)
    assert "Tisha B'Av" not in _names(5782, 5, 9)


def test_taanit_esther_moved_when_13_adar_is_shabbat() -> None:
    # 5784 (leap): 13 Adar II is Shabbat, so Ta'anit Esther is on 11 Adar II (Thursday).
    assert "Ta'anit Esther" in _names(5784, 13, 11)


def test_asara_btevet_never_postponed() -> None:
    assert "Asara B'Tevet" in _names(5785, 10, 10)
```

- [ ] **Step 2: Run — expect failure.**

- [ ] **Step 3: Implement `_fasts`** and wire `result += _fasts(year, diaspora)`:

```python
from hebrewcal.core.rata_die import weekday_from_rd  # add to the imports

_SHABBAT = 6  # weekday_from_rd: 0 = Sunday ... 6 = Saturday


def _postpone_if_shabbat(date: HebrewDate) -> HebrewDate:
    """Return the date, moved to Sunday if it falls on Shabbat."""
    if weekday_from_rd(date.to_rd()) == _SHABBAT:
        return HebrewDate.from_rd(date.to_rd() + 1)
    return date


def _fasts(year: int, diaspora: bool) -> list[Holiday]:
    """Return the public fasts, applying the postponement rules."""
    out: list[Holiday] = []
    purim_month = _purim_month(year)

    # These move to Sunday when they fall on Shabbat.
    for name, month, day in (
        ("Tzom Gedaliah", 7, 3),
        ("Shiva Asar B'Tammuz", 4, 17),
        ("Tisha B'Av", 5, 9),
    ):
        out.append(Holiday(name, _postpone_if_shabbat(HebrewDate(year, month, day)), Category.FAST))

    # Asara B'Tevet is observed on its day even on Friday and is never postponed
    # (it cannot fall on Shabbat).
    out.append(Holiday("Asara B'Tevet", HebrewDate(year, 10, 10), Category.FAST))

    # Ta'anit Esther: 13 Adar(II); if that is Shabbat, it is brought forward to the
    # preceding Thursday (11 Adar).
    esther = HebrewDate(year, purim_month, 13)
    if weekday_from_rd(esther.to_rd()) == _SHABBAT:
        esther = HebrewDate.from_rd(esther.to_rd() - 2)
    out.append(Holiday("Ta'anit Esther", esther, Category.FAST))

    # Ta'anit Bechorot: 14 Nisan, brought forward to Thursday 12 Nisan if on Shabbat.
    bechorot = HebrewDate(year, 1, 14)
    if weekday_from_rd(bechorot.to_rd()) == _SHABBAT:
        bechorot = HebrewDate.from_rd(bechorot.to_rd() - 2)
    out.append(Holiday("Ta'anit Bechorot", bechorot, Category.FAST))
    return out
```

- [ ] **Step 4: Run — expect pass.**  - [ ] **Step 5: Gate + commit** — `Closes #42`.

---

## Task 5: Modern Israeli days  (issue #43)

**Files:** Modify `holidays.py` (add `_modern`, wire in); test
`tests/religious/test_modern.py`.

- [ ] **Step 1: Failing test** (expected Hebrew dates from the verified table above):

```python
"""Tests for the modern Israeli days and their adjustment rules."""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.religious.holidays import holidays_on


def _names(year: int, m: int, d: int) -> set[str]:
    return {h.name for h in holidays_on(HebrewDate(year, m, d))}


def test_5784_monday_rule() -> None:
    # 5 Iyyar 5784 is Monday: Zikaron 5 Iyyar, Atzmaut 6 Iyyar; Shoah 28 Nisan.
    assert "Yom HaShoah" in _names(5784, 1, 28)
    assert "Yom HaZikaron" in _names(5784, 2, 5)
    assert "Yom HaAtzmaut" in _names(5784, 2, 6)


def test_5785_friday_saturday_rule() -> None:
    # 5 Iyyar 5785 is Saturday: Atzmaut Thursday 3 Iyyar, Zikaron Wednesday 2 Iyyar;
    # 27 Nisan is Friday so Shoah moves to 26 Nisan.
    assert "Yom HaShoah" in _names(5785, 1, 26)
    assert "Yom HaZikaron" in _names(5785, 2, 2)
    assert "Yom HaAtzmaut" in _names(5785, 2, 3)


def test_5786_no_adjustment() -> None:
    # 5 Iyyar 5786 is Wednesday: default placement; 27 Nisan Tuesday (no move).
    assert "Yom HaShoah" in _names(5786, 1, 27)
    assert "Yom HaZikaron" in _names(5786, 2, 4)
    assert "Yom HaAtzmaut" in _names(5786, 2, 5)


def test_yom_yerushalayim_fixed() -> None:
    assert "Yom Yerushalayim" in _names(5785, 2, 28)
```

- [ ] **Step 2: Run — expect failure.**

- [ ] **Step 3: Implement `_modern`** and wire `result += _modern(year, diaspora)`:

```python
def _modern(year: int, diaspora: bool) -> list[Holiday]:
    """Return the modern Israeli days, applying the statutory weekday adjustments.

    Weekdays use weekday_from_rd (0 = Sunday ... 6 = Saturday).
    """
    out: list[Holiday] = []

    # Yom HaShoah, 27 Nisan: Friday -> 26 Nisan (Thu); Sunday -> 28 Nisan (Mon).
    shoah = HebrewDate(year, 1, 27)
    wd = weekday_from_rd(shoah.to_rd())
    if wd == 5:        # Friday
        shoah = HebrewDate(year, 1, 26)
    elif wd == 0:      # Sunday
        shoah = HebrewDate(year, 1, 28)
    out.append(Holiday("Yom HaShoah", shoah, Category.MODERN))

    # Yom HaZikaron (4 Iyyar) and Yom HaAtzmaut (5 Iyyar), keyed off 5 Iyyar's weekday.
    # 5 Iyyar can only be Mon, Wed, Fri or Sat (lo BaDU Pesach).
    wd5 = weekday_from_rd(HebrewDate(year, 2, 5).to_rd())
    if wd5 == 5:       # Friday -> Atzmaut Thu 4, Zikaron Wed 3
        zikaron, atzmaut = (year, 2, 3), (year, 2, 4)
    elif wd5 == 6:     # Saturday -> Atzmaut Thu 3, Zikaron Wed 2
        zikaron, atzmaut = (year, 2, 2), (year, 2, 3)
    elif wd5 == 1:     # Monday -> Zikaron Mon 5, Atzmaut Tue 6
        zikaron, atzmaut = (year, 2, 5), (year, 2, 6)
    else:              # Wednesday -> default Zikaron 4, Atzmaut 5
        zikaron, atzmaut = (year, 2, 4), (year, 2, 5)
    out.append(Holiday("Yom HaZikaron", HebrewDate(*zikaron), Category.MODERN))
    out.append(Holiday("Yom HaAtzmaut", HebrewDate(*atzmaut), Category.MODERN))

    out.append(Holiday("Yom Yerushalayim", HebrewDate(year, 2, 28), Category.MODERN))
    return out
```

- [ ] **Step 4: Run — expect pass.** These reproduce the known 2024/2025/2026 dates.
- [ ] **Step 5: Gate + commit** — `Closes #43`.

```{admonition} Verify against an authority
The adjustment rules are the post-2004 Knesset rules and were cross-checked against the
published 2024 and 2025 dates. If extending to years before the modern era, guard the
modern days behind a minimum year if desired (not required here).
```

---

## Task 6: Minority and communal feasts  (issue #44)

**Files:** Modify `holidays.py` (add `_minority`, wire in); test
`tests/religious/test_minority.py`.

- [ ] **Step 1: Failing test**

```python
"""Tests for minority / communal feasts."""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.religious.holidays import Category, holidays_on


def test_sigd() -> None:
    # Sigd: 29 Marheshvan (50 days after Yom Kippur), Ethiopian Jewry.
    found = holidays_on(HebrewDate(5785, 8, 29))
    assert any(h.name == "Sigd" and h.category is Category.MINORITY for h in found)


def test_mimouna() -> None:
    # Mimouna: the day after Pesach, 22 Nisan.
    found = holidays_on(HebrewDate(5785, 1, 22))
    assert any(h.name == "Mimouna" for h in found)
```

- [ ] **Step 2: Run — expect failure.**

- [ ] **Step 3: Implement `_minority`** and wire `result += _minority(year, diaspora)`:

```python
def _minority(year: int, diaspora: bool) -> list[Holiday]:
    """Return communal feasts of specific Jewish communities."""
    return [
        # Sigd, Ethiopian Jewry: 29 Marheshvan, the 50th day after Yom Kippur.
        Holiday("Sigd", HebrewDate(year, 8, 29), Category.MINORITY),
        # Mimouna, North African communities: the day after Pesach ends (22 Nisan).
        Holiday("Mimouna", HebrewDate(year, 1, 22), Category.MINORITY),
    ]
```

- [ ] **Step 4: Run — expect pass.**  - [ ] **Step 5: Gate + commit** — `Closes #44`.

---

## Task 7: The Omer count  (issue #45)

**Files:** Create `src/hebrewcal/religious/omer.py`; test `tests/religious/test_omer.py`.

- [ ] **Step 1: Failing test**

```python
"""Tests for the Omer count."""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.religious.omer import omer_count, omer_week_day


def test_first_and_last_day() -> None:
    assert omer_count(HebrewDate(5785, 1, 16)) == 1     # 16 Nisan = day 1
    assert omer_count(HebrewDate(5785, 3, 5)) == 49     # 5 Sivan = day 49


def test_outside_the_count() -> None:
    assert omer_count(HebrewDate(5785, 1, 15)) is None   # 15 Nisan, before
    assert omer_count(HebrewDate(5785, 3, 6)) is None    # 6 Sivan, Shavuot


def test_week_and_day_breakdown() -> None:
    # Lag BaOmer is day 33 = 4 weeks and 5 days.
    assert omer_count(HebrewDate(5785, 2, 18)) == 33
    assert omer_week_day(HebrewDate(5785, 2, 18)) == (4, 5)
```

- [ ] **Step 2: Run — expect failure.**

- [ ] **Step 3: Implement `omer.py`**

```python
"""Sefirat HaOmer — the count of the Omer.

The count runs for 49 days, from 16 Nisan (day 1) to 5 Sivan (day 49); Shavuot
falls on the next day (6 Sivan).
"""

from __future__ import annotations

from hebrewcal.calendars.hebrew import HebrewDate


def omer_count(date: HebrewDate) -> int | None:
    """Return the Omer day (1-49) for ``date``, or None if outside the count."""
    start = HebrewDate(date.year, 1, 16).to_rd()
    day = date.to_rd() - start + 1
    return day if 1 <= day <= 49 else None


def omer_week_day(date: HebrewDate) -> tuple[int, int] | None:
    """Return (weeks, days) of the Omer for ``date``, or None outside the count."""
    count = omer_count(date)
    if count is None:
        return None
    return divmod(count, 7)[0], count % 7
```

- [ ] **Step 4: Run — expect pass.**  - [ ] **Step 5: Gate + commit** — `Closes #45`.

---

## Task 8: Special Shabbatot  (issue #46)

**Files:** Modify `holidays.py` (add `_special_shabbatot`, wire in); test
`tests/religious/test_special_shabbatot.py`.

- [ ] **Step 1: Failing test** (structural: each falls on Saturday and in the right window)

```python
"""Tests for the special Shabbatot."""

from __future__ import annotations

from hebrewcal.core.rata_die import weekday_from_rd
from hebrewcal.religious.holidays import Category, holidays


def _specials(year: int) -> dict[str, int]:
    return {
        h.name: h.date.to_rd()
        for h in holidays(year)
        if h.category is Category.SPECIAL_SHABBAT
    }


def test_all_on_saturday() -> None:
    for rd in _specials(5785).values():
        assert weekday_from_rd(rd) == 6  # Saturday


def test_expected_set_present() -> None:
    names = set(_specials(5785))
    for name in (
        "Shabbat Shekalim",
        "Shabbat Zachor",
        "Shabbat Parah",
        "Shabbat HaChodesh",
        "Shabbat HaGadol",
        "Shabbat Shuvah",
        "Shabbat Chazon",
        "Shabbat Nachamu",
    ):
        assert name in names


def test_hagadol_is_before_pesach() -> None:
    from hebrewcal.calendars.hebrew import HebrewDate

    specials = _specials(5785)
    assert specials["Shabbat HaGadol"] < HebrewDate(5785, 1, 15).to_rd()
    assert HebrewDate(5785, 1, 15).to_rd() - specials["Shabbat HaGadol"] <= 7
```

- [ ] **Step 2: Run — expect failure.**

- [ ] **Step 3: Implement `_special_shabbatot`** and wire it in:

```python
def _shabbat_on_or_before(rd: int) -> int:
    """Return the RD of the Saturday on or immediately before ``rd``."""
    return rd - ((rd % 7) + 1) % 7


def _shabbat_before(rd: int) -> int:
    """Return the RD of the Saturday strictly before ``rd``."""
    return _shabbat_on_or_before(rd - 1)


def _shabbat_after(rd: int) -> int:
    """Return the RD of the first Saturday strictly after ``rd``."""
    return _shabbat_on_or_before(rd + 7)


def _special_shabbatot(year: int, diaspora: bool) -> list[Holiday]:
    """Return the named special Sabbaths of the year."""
    out: list[Holiday] = []

    def add(name: str, rd: int) -> None:
        out.append(Holiday(name, HebrewDate.from_rd(rd), Category.SPECIAL_SHABBAT))

    purim_month = _purim_month(year)
    rosh_chodesh_adar = HebrewDate(year, purim_month, 1).to_rd()
    rosh_chodesh_nisan = HebrewDate(year, 1, 1).to_rd()
    purim = HebrewDate(year, purim_month, 14).to_rd()
    pesach = HebrewDate(year, 1, 15).to_rd()
    tisha_bav = HebrewDate(year, 5, 9).to_rd()

    add("Shabbat Shekalim", _shabbat_on_or_before(rosh_chodesh_adar))
    add("Shabbat Zachor", _shabbat_before(purim))
    add("Shabbat Parah", _shabbat_before(_shabbat_on_or_before(rosh_chodesh_nisan)))
    add("Shabbat HaChodesh", _shabbat_on_or_before(rosh_chodesh_nisan))
    add("Shabbat HaGadol", _shabbat_before(pesach))
    add("Shabbat Shuvah", _shabbat_after(HebrewDate(year, 7, 1).to_rd()))
    add("Shabbat Chazon", _shabbat_before(tisha_bav))
    add("Shabbat Nachamu", _shabbat_after(tisha_bav))
    return out
```

- [ ] **Step 4: Run — expect pass.** If `Shabbat Parah`/`Shekalim` placement disagrees with
a published luach for a given year, adjust the relation (Parah is the Shabbat before
HaChodesh); the test pins them to Saturdays and HaGadol to the week before Pesach.
- [ ] **Step 5: Gate + commit** — `Closes #46`.

---

## Task 9: Holiday reference-validation suite  (issue #47)

**Files:** Create `tests/religious/test_reference_holidays.py`.

- [ ] **Step 1: Write the validation tests** using verified Gregorian dates:

```python
"""Cross-checked reference dates for holidays (verified against pyluach)."""

from __future__ import annotations

from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars.hebrew import HebrewDate
from hebrewcal.conversion import to_gregorian
from hebrewcal.religious.holidays import holidays


def _greg(year: int, name: str, diaspora: bool = True) -> set[tuple[int, int, int]]:
    out = set()
    for h in holidays(year, diaspora):
        if h.name == name:
            g = to_gregorian(h.date)
            out.add((g.year, g.month, g.day))
    return out


def test_rosh_hashanah_5785() -> None:
    assert (2024, 10, 3) in _greg(5785, "Rosh Hashanah")


def test_yom_kippur_5785() -> None:
    assert _greg(5785, "Yom Kippur") == {(2024, 10, 12)}


def test_hanukkah_first_day_5785() -> None:
    assert (2024, 12, 26) in _greg(5785, "Hanukkah")


def test_purim_5785() -> None:
    assert _greg(5785, "Purim") == {(2025, 3, 14)}


def test_pesach_first_day_5785() -> None:
    assert (2025, 4, 13) in _greg(5785, "Pesach")


def test_yom_haatzmaut_2025() -> None:
    # 5785: moved to Thursday 1 May 2025.
    assert _greg(5785, "Yom HaAtzmaut") == {(2025, 5, 1)}


def test_diaspora_vs_israel_pesach_length() -> None:
    israel = [h for h in holidays(5785, diaspora=False) if h.name == "Pesach"]
    diaspora = [h for h in holidays(5785, diaspora=True) if h.name == "Pesach"]
    assert len(diaspora) == len(israel) + 1  # the eighth day
```

- [ ] **Step 2: Run — expect pass** (`pytest tests/religious/test_reference_holidays.py`).
  If a date differs, re-verify against an external reference and correct only the
  expected value — not the rules.
- [ ] **Step 3: Full gate with coverage and commit** — `Closes #47`.

---

## Phase 3 completion

- [ ] All nine issues (#39–#47) closed.
- [ ] PR `feature/phase-3-holidays` → `development`; green CI; merge; delete branch.
- [ ] Update `CHANGELOG.md` `[Unreleased]` and add a `guide/holidays.md` documentation
      page plus API-reference entries.
- [ ] Manually close issues not auto-closed (merges target `development`).
- [ ] **This completes the MVP (Phases 1–3).** Consider a 0.3.0 release afterwards.

---

## Notes on correctness and references

- Classical festivals, fasts (incl. postponement), Hanukkah, Purim (incl. leap-year Adar
  II and Ta'anit Esther advance) and the Omer were verified against `pyluach`.
- Modern Israeli days are not in `pyluach`; their adjustment rules were verified to
  reproduce the published 2024 and 2025 official dates.
- Weekdays use `weekday_from_rd` (0 = Sunday … 6 = Saturday).
- Special Shabbatot are computed by their relation to Rosh Chodesh / festivals and pinned
  to Saturdays; a published luach is the reference for any year-specific dispute.
