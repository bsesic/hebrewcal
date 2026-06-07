# Quick start

This page walks through the most common tasks. Every example is runnable as-is and the
printed output is exactly what the current version produces.

## Import the public API

The package root re-exports the everyday surface:

```python
from hebrewcal import (
    GregorianDate,
    JulianDate,
    HebrewDate,
    Weekday,
    to_gregorian,
    to_julian,
    to_hebrew,
    weekday,
)
```

## Create dates

Each calendar has an immutable date type. Construction validates the date and raises
`ValueError` on impossible values (e.g. 30 Iyyar, a month that only has 29 days).

```python
GregorianDate(2026, 6, 26)
JulianDate(1582, 10, 4)
HebrewDate(5785, 7, 1)   # 1 Tishri 5785
```

```{admonition} Hebrew month numbering
:class: important

Months are numbered in the **standard** scheme: Nisan = 1, Iyyar = 2, …, **Tishri = 7**,
…, Adar (or Adar I in a leap year) = 12, Adar II = 13. The civil year begins at Tishri.
See {doc}`guide/names` for the full table.
```

## Convert between calendars

```python
>>> from hebrewcal import GregorianDate, HebrewDate, to_hebrew, to_gregorian, to_julian
>>> to_hebrew(GregorianDate(2024, 10, 3))
HebrewDate(year=5785, month=7, day=1)
>>> to_gregorian(HebrewDate(5785, 7, 1))
GregorianDate(year=2024, month=10, day=3)
>>> to_julian(GregorianDate(2026, 6, 26))
JulianDate(year=2026, month=6, day=13)
```

## Find the weekday

```python
>>> from hebrewcal import GregorianDate, weekday
>>> weekday(GregorianDate(1867, 10, 31))
<Weekday.THURSDAY: 4>
>>> weekday(GregorianDate(1867, 10, 31)).name
'THURSDAY'
```

## Work with the Rata Die day count

Every date exposes `to_rd()` and `from_rd()`:

```python
>>> from hebrewcal import GregorianDate
>>> GregorianDate(2026, 6, 26).to_rd()
739793
>>> GregorianDate.from_rd(739793)
GregorianDate(year=2026, month=6, day=26)
```

## Parse and format

```python
>>> from hebrewcal.parsing.dates import parse_gregorian
>>> parse_gregorian("26.06.2026")
GregorianDate(year=2026, month=6, day=26)

>>> from hebrewcal.formatting.dates import format_hebrew
>>> from hebrewcal import HebrewDate
>>> format_hebrew(HebrewDate(5785, 7, 1), style="named")
'1 Tishri 5785'
```

## Hebrew numerals (gematria)

```python
>>> from hebrewcal.numerals import to_hebrew_numeral, from_hebrew_numeral
>>> to_hebrew_numeral(5785)
'ה׳תשפ״ה'
>>> from_hebrew_numeral("ה׳תשפ״ה")
5785
```

Where to go next: the {doc}`guide/index` explains each subsystem in depth, and
{doc}`examples` collects longer, real-world snippets.
