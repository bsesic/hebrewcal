# Examples

A cookbook of longer, real-world snippets. Each is self-contained.

## Answer a historical conversion question

> *What Hebrew date and weekday corresponds to 31 October 1867?*

```python
from hebrewcal import GregorianDate, to_hebrew, weekday
from hebrewcal.names import hebrew_month_name

g = GregorianDate(1867, 10, 31)
h = to_hebrew(g)
label = f"{h.day} {hebrew_month_name(h.year, h.month)} {h.year}"
print(label, "—", weekday(g).name.title())
# 2 Marheshvan 5628 — Thursday
```

## List the Gregorian date of Rosh Hashanah for several years

```python
from hebrewcal import HebrewDate, to_gregorian, weekday

for year in range(5785, 5790):
    rosh_hashanah = HebrewDate(year, 7, 1)   # 1 Tishri
    g = to_gregorian(rosh_hashanah)
    print(f"AM {year}: {g.year}-{g.month:02d}-{g.day:02d} ({weekday(rosh_hashanah).name.title()})")
```

```text
AM 5785: 2024-10-03 (Thursday)
AM 5786: 2025-09-23 (Tuesday)
AM 5787: 2026-09-12 (Saturday)
AM 5788: 2027-10-02 (Saturday)
AM 5789: 2028-09-21 (Thursday)
```

## Compute a yahrzeit (anniversary) date

A yahrzeit recurs on the same Hebrew date. To find next year's Gregorian date of an event
that happened on 1 Tishri 5785:

```python
from hebrewcal import HebrewDate, to_gregorian

event = HebrewDate(5785, 7, 1)
next_year = HebrewDate(event.year + 1, event.month, event.day)
print(to_gregorian(next_year))   # GregorianDate(year=2025, month=9, day=23)
```

```{admonition} A full yahrzeit engine comes later
:class: note

Real yahrzeit rules handle edge cases — a death on 30 Marheshvan or Kislev in a year
where the following year lacks that day, and the special treatment of Adar in leap vs.
common years. Those rules arrive with the religious-times phase; the snippet above is the
straightforward common case.
```

## Label a date with a gematria year

```python
from hebrewcal import HebrewDate
from hebrewcal.names import hebrew_month_name
from hebrewcal.numerals import to_hebrew_numeral

h = HebrewDate(5785, 7, 1)
print(f"{h.day} {hebrew_month_name(h.year, h.month)} {to_hebrew_numeral(h.year)}")
# 1 Tishri ה׳תשפ״ה
```

## Work with a historical (Julian) date

Before the Gregorian reform, many sources are dated in the Julian calendar. Convert a
Julian date to Hebrew through RD:

```python
from hebrewcal import JulianDate, to_hebrew, to_gregorian

j = JulianDate(1492, 3, 31)            # Alhambra Decree, Julian date
print(to_gregorian(j))                 # the proleptic Gregorian equivalent
print(to_hebrew(j))                    # the Hebrew date
```

## Parse user input and report the Hebrew date

```python
from hebrewcal.parsing.dates import parse_gregorian
from hebrewcal import to_hebrew, weekday
from hebrewcal.formatting.dates import format_hebrew

for text in ("2026-06-26", "26.06.2026", "1867/10/31"):
    g = parse_gregorian(text)
    h = to_hebrew(g)
    print(f"{text:>12}  ->  {format_hebrew(h, style='named')}  ({weekday(g).name.title()})")
```

## Survey the keviah of a decade

```python
from hebrewcal.hebrew.keviah import keviah
from hebrewcal.hebrew.yeartype import days_in_year

for year in range(5784, 5790):
    k = keviah(year)
    kind = k.kind.value
    leap = "leap" if k.leap else "common"
    print(f"{year}: {leap:6} {kind:9} {days_in_year(year)} days, RH weekday {k.rosh_hashanah_weekday}")
```

## Round-trip any date through Rata Die

```python
from hebrewcal import GregorianDate, JulianDate, HebrewDate

for rd in (-1373427, 0, 1, 739793):
    assert GregorianDate.from_rd(rd).to_rd() == rd
    assert JulianDate.from_rd(rd).to_rd() == rd
    assert HebrewDate.from_rd(rd).to_rd() == rd
print("all calendars round-trip exactly")
```
