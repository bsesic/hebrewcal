# Formatting dates

`hebrewcal.formatting.dates` renders dates as text. Gregorian dates have numeric styles;
Hebrew dates have a numeric style and a named style that uses the
{doc}`name tables <names>`.

## Gregorian

```python
>>> from hebrewcal import GregorianDate
>>> from hebrewcal.formatting.dates import format_gregorian
>>> g = GregorianDate(2026, 6, 26)
>>> format_gregorian(g, style="iso")
'2026-06-26'
>>> format_gregorian(g, style="din")
'26.06.2026'
```

| Style | Output | Notes |
|-------|--------|-------|
| `"iso"` (default) | `2026-06-26` | ISO 8601, zero-padded |
| `"din"` | `26.06.2026` | DIN 5008, day-first |

## Hebrew

```python
>>> from hebrewcal import HebrewDate
>>> from hebrewcal.formatting.dates import format_hebrew
>>> h = HebrewDate(5785, 7, 1)
>>> format_hebrew(h, style="named")
'1 Tishri 5785'
>>> format_hebrew(h, style="numeric")
'5785-07-01'
```

The named style understands leap-year month naming (Adar I / Adar II):

```python
>>> format_hebrew(HebrewDate(5784, 12, 1), style="named")
'1 Adar I 5784'
>>> format_hebrew(HebrewDate(5784, 13, 1), style="named")
'1 Adar II 5784'
```

```{admonition} Round-tripping with parsing
:class: tip

`format_gregorian(g, "iso")` and `format_gregorian(g, "din")` both produce strings that
`parse_gregorian` reads back into the same date — handy for storage and display layers
that disagree on format.
```

An unknown style raises `ValueError`:

```python
>>> format_gregorian(g, style="rfc")
Traceback (most recent call last):
    ...
ValueError: unknown style: 'rfc'
```
