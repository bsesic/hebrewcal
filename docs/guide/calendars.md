# Calendars and conversion

`hebrewcal` ships three calendars, each an immutable dataclass with `year`, `month` and
`day` fields, a `to_rd()` method and a `from_rd()` classmethod.

| Calendar | Type | Module |
|----------|------|--------|
| Gregorian (proleptic) | `GregorianDate` | `hebrewcal.calendars.gregorian` |
| Julian (proleptic) | `JulianDate` | `hebrewcal.calendars.julian` |
| Hebrew | `HebrewDate` | `hebrewcal.calendars.hebrew` |

All three are re-exported from the package root.

## Gregorian

The proleptic Gregorian calendar is valid for every year, including years ≤ 0.

```python
>>> from hebrewcal import GregorianDate
>>> GregorianDate(2026, 6, 26).to_rd()
739793
>>> GregorianDate.from_rd(739793)
GregorianDate(year=2026, month=6, day=26)
>>> from hebrewcal.calendars.gregorian import is_leap_year
>>> is_leap_year(2000), is_leap_year(1900), is_leap_year(2024)
(True, False, True)
```

Dates are validated on construction:

```python
>>> GregorianDate(2026, 2, 30)
Traceback (most recent call last):
    ...
ValueError: day out of range: 30
```

## Julian

The proleptic Julian calendar uses the simple "every fourth year" leap rule. There is no
year 0; year −1 precedes year 1.

```python
>>> from hebrewcal import JulianDate
>>> from hebrewcal.calendars.julian import is_leap_year
>>> is_leap_year(1900)   # leap in the Julian calendar
True
>>> JulianDate(2026, 6, 13).to_rd()
739793
```

### The Julian/Gregorian reform

The 1582 reform skipped from Julian **Thursday 4 October 1582** straight to Gregorian
**Friday 15 October 1582**. `hebrewcal` never performs this jump silently — it computes
everything through RD and exposes the cutover explicitly:

```python
>>> from hebrewcal import JulianDate, GregorianDate
>>> JulianDate(1582, 10, 4).to_rd()
577735
>>> GregorianDate(1582, 10, 15).to_rd()
577736
>>> # The two are consecutive days: no gap in the RD timeline.
>>> from hebrewcal.calendars.julian import last_gregorian_before_reform
>>> last_gregorian_before_reform()
GregorianDate(year=1582, month=10, day=4)
```

```{admonition} Regional adoption
:class: warning

The 1582 cutover is the *papal* one. Many countries adopted the Gregorian calendar much
later (Britain in 1752, Russia in 1918, …). `hebrewcal` gives you exact RD values for
both calendars; choosing which calendar a historical date was *written in* is your
decision, not a silent default.
```

## Hebrew

The Hebrew date type wires the arithmetic engine (see {doc}`hebrew-internals`) into the
calendar contract.

```python
>>> from hebrewcal import HebrewDate, to_gregorian
>>> HebrewDate(5785, 7, 1)               # 1 Tishri 5785
HebrewDate(year=5785, month=7, day=1)
>>> to_gregorian(HebrewDate(5785, 7, 1))
GregorianDate(year=2024, month=10, day=3)
```

Leap years contain a 13th month (Adar II); month 12 becomes Adar I:

```python
>>> HebrewDate(5784, 13, 1).to_rd() > HebrewDate(5784, 12, 1).to_rd()
True
```

## Converting between calendars

The high-level helpers all route through RD:

```python
>>> from hebrewcal import GregorianDate, to_hebrew, to_julian
>>> to_hebrew(GregorianDate(1867, 10, 31))
HebrewDate(year=5628, month=8, day=2)
>>> to_julian(GregorianDate(1867, 10, 31))
JulianDate(year=1867, month=10, day=19)
```

A worked answer to the classic question — *"What Hebrew date and weekday corresponds to
31 October 1867?"*:

```python
>>> from hebrewcal import GregorianDate, to_hebrew, weekday
>>> g = GregorianDate(1867, 10, 31)
>>> h = to_hebrew(g)
>>> f"{h.day} Marheshvan {h.year}, {weekday(g).name.title()}"
'2 Marheshvan 5628, Thursday'
```
