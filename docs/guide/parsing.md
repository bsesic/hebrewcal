# Parsing dates

`hebrewcal.parsing.dates.parse_gregorian` reads a Gregorian date from text and returns a
normalised `GregorianDate`. It accepts several common formats and raises `ValueError` on
anything it cannot interpret unambiguously.

## Supported formats

| Format | Example | Pattern |
|--------|---------|---------|
| ISO 8601 | `2026-06-26` | `YYYY-MM-DD` |
| DIN 5008 | `26.06.2026` | `DD.MM.YYYY` |
| Slash form | `2026/06/26` | `YYYY/MM/DD` |

```python
>>> from hebrewcal.parsing.dates import parse_gregorian
>>> parse_gregorian("2026-06-26")
GregorianDate(year=2026, month=6, day=26)
>>> parse_gregorian("26.06.2026")
GregorianDate(year=2026, month=6, day=26)
>>> parse_gregorian("2026/06/26")
GregorianDate(year=2026, month=6, day=26)
```

Surrounding whitespace is tolerated:

```python
>>> parse_gregorian("  2026-06-26  ")
GregorianDate(year=2026, month=6, day=26)
```

## Errors

Unrecognised text and impossible dates both raise `ValueError`:

```python
>>> parse_gregorian("not a date")
Traceback (most recent call last):
    ...
ValueError: unrecognised date format: 'not a date'

>>> parse_gregorian("2026-13-01")   # there is no month 13
Traceback (most recent call last):
    ...
ValueError: month out of range: 13
```

## From text straight to a Hebrew date

Combine parsing with conversion:

```python
>>> from hebrewcal.parsing.dates import parse_gregorian
>>> from hebrewcal import to_hebrew
>>> to_hebrew(parse_gregorian("31.10.1867"))
HebrewDate(year=5628, month=8, day=2)
```

```{admonition} Disambiguation
:class: tip

The three formats are distinguished by their separators (`-`, `.`, `/`) and field order,
so `26.06.2026` (day-first DIN) and `2026-06-26` (year-first ISO) never collide. If you
have data in another layout, normalise it to one of these before calling
`parse_gregorian`.
```
