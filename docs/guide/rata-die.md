# Rata Die — the conversion pivot

## What it is

The **Rata Die (RD)** is a continuous integer count of days. By definition

> **RD 1 = Monday, 1 January 1** in the proleptic Gregorian calendar.

"Proleptic" means the Gregorian rules are extended backwards before 1582, so every date —
ancient, medieval or modern — maps to exactly one RD value, and vice versa. This single
number is the hub through which every calendar in `hebrewcal` converts.

```python
from hebrewcal.core.rata_die import RD_EPOCH, weekday_from_rd, add_days

RD_EPOCH          # 1
weekday_from_rd(1)  # 1  (Monday; see the weekday convention below)
add_days(739793, 7) # 739800
```

## The calendar contract

A calendar date is any value that implements two operations:

```python
date.to_rd() -> int          # date  -> day count
Calendar.from_rd(rd) -> date # day count -> date
```

This is captured by the `CalendarDate` protocol in `hebrewcal.core.calendar`. Because the
contract is so small, conversion is universal:

```python
from hebrewcal.core.calendar import convert
from hebrewcal.calendars.gregorian import GregorianDate
from hebrewcal.calendars.hebrew import HebrewDate

convert(GregorianDate(2024, 10, 3), HebrewDate)
# HebrewDate(year=5785, month=7, day=1)
```

The high-level helpers `to_gregorian`, `to_julian` and `to_hebrew` are thin wrappers
around `convert`; use whichever reads better.

## Weekdays

The `Weekday` enum numbers days with **Sunday = 0 … Saturday = 6**, matching
`weekday_from_rd`:

```python
>>> from hebrewcal import GregorianDate, weekday, Weekday
>>> weekday(GregorianDate(1867, 10, 31))
<Weekday.THURSDAY: 4>
>>> weekday(GregorianDate(1867, 10, 31)) is Weekday.THURSDAY
True
```

`weekday()` works for **any** calendar date, because it only needs `to_rd()`:

```python
>>> from hebrewcal import HebrewDate, weekday
>>> weekday(HebrewDate(5785, 7, 1)).name
'THURSDAY'
```

## Why an integer pivot?

- **Exactness.** Day arithmetic is plain integer arithmetic — no floating point, no
  rounding, no time-zone surprises.
- **Range.** RD is unbounded, so antiquity and the far future are handled identically.
- **Extensibility.** A future calendar (Karaite, Qumran, Samaritan, …) only needs
  `to_rd` / `from_rd` to interoperate with everything already here.

```{admonition} Relationship to other day counts
:class: note

RD equals Python's own proleptic Gregorian ordinal, so
`datetime.date(y, m, d).toordinal() == GregorianDate(y, m, d).to_rd()`. This makes the
Gregorian implementation trivially cross-checkable against the standard library.
```
