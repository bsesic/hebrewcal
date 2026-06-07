# hebrewcal

A pure-Python library for the Hebrew calendar.

`hebrewcal` makes the Hebrew calendar usable programmatically and converts it
bidirectionally against the Gregorian and Julian calendars. Every computation is
performed locally — the library never issues network calls to any external service.

It serves both **religious** use (holidays, Shabbat, Havdalah, zmanim, Torah readings,
the Omer, yahrzeit, the sabbatical and jubilee cycle, for Israel and the Diaspora) and
**academic** use (historical, medieval and ancient dates, Babylonian and biblical month
names, proleptic calendars, the Julian/Gregorian reform, and the documented "missing
years" of the Anno Mundi count).

```{admonition} Project status
:class: note

Early development. The calendar core, conversion and date handling (Phase 1) are
implemented and documented here. Astronomy, holidays and religious times follow on the
roadmap.
```

## The idea in one sentence

Everything pivots on the **Rata Die (RD)** day count from Dershowitz & Reingold,
*Calendrical Calculations*: every calendar implements only `to_rd` and `from_rd`, and
conversion between any two calendars always goes through RD.

```python
from hebrewcal import GregorianDate, to_hebrew, weekday

g = GregorianDate(1867, 10, 31)
print(to_hebrew(g))      # HebrewDate(year=5628, month=8, day=2)
print(weekday(g).name)   # THURSDAY
```

```{toctree}
:maxdepth: 2
:caption: Getting started

installation
quickstart
```

```{toctree}
:maxdepth: 2
:caption: User guide

guide/index
```

```{toctree}
:maxdepth: 2
:caption: Reference

examples
testing
api
contributing
changelog
```

## Indices

- {ref}`genindex`
- {ref}`modindex`
