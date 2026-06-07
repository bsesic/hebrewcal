# Hebrew calendar internals

This page documents the arithmetic engine behind `HebrewDate`. You rarely need these
functions directly — they are exposed for academic use, for building higher-level
features, and for understanding *why* a given year has the shape it does. All algorithms
follow Dershowitz & Reingold, *Calendrical Calculations*.

The engine lives in the `hebrewcal.hebrew` subpackage:

| Module | Responsibility |
|--------|----------------|
| `metonic` | The 19-year leap cycle |
| `molad` | Molad, halakim, calendar-elapsed-days |
| `dechiyot` | The four postponement rules as a year-length correction |
| `yeartype` | New-year RD, year length, month lengths |
| `keviah` | The year signature |

## The Metonic cycle

Hebrew leap years follow a 19-year cycle with **seven** leap years. A year is leap iff
`(7 · year + 1) mod 19 < 7`.

```python
>>> from hebrewcal.hebrew.metonic import is_leap_year, months_in_year
>>> is_leap_year(5784), is_leap_year(5785)
(True, False)
>>> months_in_year(5784)   # leap year: 13 months
13
>>> months_in_year(5785)   # common year: 12 months
12
```

## Molad and halakim

Time in the Hebrew calendar is measured in **halakim** ("parts"): there are 1080 parts in
an hour, so 25920 in a day. A single part is a **helek**. The **molad** is the mean lunar
conjunction.

```python
>>> from hebrewcal.hebrew.molad import HALAKIM_PER_HOUR, HALAKIM_PER_DAY
>>> HALAKIM_PER_HOUR, HALAKIM_PER_DAY
(1080, 25920)
```

`molad_parts(year, month)` returns the molad as an absolute count of parts since the
epoch. Split it into a day and a position within the day:

```python
>>> from hebrewcal.hebrew.molad import molad_parts, HALAKIM_PER_DAY, HALAKIM_PER_HOUR
>>> parts = molad_parts(5785, 7)        # molad of Tishri 5785
>>> day, within = divmod(parts, HALAKIM_PER_DAY)
>>> hours, halakim = divmod(within, HALAKIM_PER_HOUR)
>>> day, hours, halakim
(2112589, 15, 391)
>>> day % 7                              # weekday of the molad (0 = Sunday)
3
```

`calendar_elapsed_days(year)` gives the days from the epoch to that year's Tishri, with
the molad-zaken adjustment already applied:

```python
>>> from hebrewcal.hebrew.molad import calendar_elapsed_days
>>> calendar_elapsed_days(5785)
2112589
```

## The dechiyot (the "four gates")

Rosh Hashanah may not fall on certain weekdays (the rule **lo ADU rosh**: not Sunday,
Wednesday or Friday), and two further cases adjust the *length* of a year so that no year
is illegally short or long. Together these are the four postponement rules, the
**dechiyot**. The molad-zaken / lo-ADU part is folded into `calendar_elapsed_days`; the
year-length part is `year_length_correction`, which adds 0, 1 or 2 days:

```python
>>> from hebrewcal.hebrew.dechiyot import year_length_correction
>>> year_length_correction(5785)
0
>>> all(year_length_correction(y) in (0, 1, 2) for y in range(5700, 5800))
True
```

## Year length and month lengths

`new_year_rd(year)` is the RD of 1 Tishri (Rosh Hashanah); `days_in_year` is the gap to
the next one.

```python
>>> from hebrewcal.hebrew.yeartype import new_year_rd, days_in_year
>>> new_year_rd(5785)
739162
>>> days_in_year(5785)
355
```

A Hebrew year has **353, 354 or 355** days (common) or **383, 384 or 385** (leap). The
length decides whether Marheshvan is long (30) and whether Kislev is short (29):

```python
>>> from hebrewcal.hebrew.yeartype import last_day_of_month
>>> last_day_of_month(5785, 8)   # Marheshvan
30
>>> last_day_of_month(5785, 9)   # Kislev
30
```

## The keviah (year signature)

The **keviah** captures a whole year in three facts: leap or not, the weekday of Rosh
Hashanah, and whether the year is **deficient** (chaser), **regular** (kesidran) or
**complete** (shalem).

```python
>>> from hebrewcal.hebrew.keviah import keviah, YearKind
>>> k = keviah(5785)
>>> k.leap, k.rosh_hashanah_weekday, k.kind
(False, 4, <YearKind.COMPLETE: 'complete'>)
```

Three consecutive years show the variety:

| Year | Leap | Rosh Hashanah weekday | Kind | Days |
|------|------|-----------------------|------|------|
| 5784 | yes | 6 (Saturday) | deficient | 383 |
| 5785 | no | 4 (Thursday) | complete | 355 |
| 5786 | no | 2 (Tuesday) | regular | 354 |

```{admonition} Deficient / regular / complete
:class: note

- **Deficient** (353 / 383): both Marheshvan (29) and Kislev (29) are short.
- **Regular** (354 / 384): Marheshvan 29, Kislev 30.
- **Complete** (355 / 385): both Marheshvan and Kislev have 30 days.
```
