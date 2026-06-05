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

```{toctree}
:maxdepth: 2
:caption: Contents

api
```

## Design in one sentence

Everything pivots on the Rata Die (RD) day count from Dershowitz & Reingold,
*Calendrical Calculations*: every calendar implements only `to_rd` and `from_rd`, and
conversion between any two calendars always goes through RD.

## Indices

- {ref}`genindex`
- {ref}`modindex`
