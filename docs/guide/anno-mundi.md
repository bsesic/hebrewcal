# The Anno Mundi era and the "missing years"

## Anno Mundi

The Hebrew year number *is* the **Anno Mundi (AM)** year — years counted "from the
creation of the world". `hebrewcal.eras.anno_mundi` exposes this directly:

```python
>>> from hebrewcal import HebrewDate
>>> from hebrewcal.eras.anno_mundi import anno_mundi_year
>>> anno_mundi_year(HebrewDate(5785, 7, 1))
5785
```

AM conversion is computationally exact and unambiguous — it is simply the Hebrew calendar
arithmetic documented in {doc}`hebrew-internals`.

## The "missing years"

There is a well-known discrepancy between the **traditional** Hebrew chronology and the
**academic-historical** one for the Persian period: the traditional reckoning compresses
that era and ends up roughly **165 years** shorter. (See the
[Wikipedia overview](https://en.wikipedia.org/wiki/Missing_years_(Jewish_calendar)).)

`hebrewcal` takes a deliberate stance:

> AM years are computed exactly and the discrepancy is **documented, not silently
> corrected.** This keeps the library correct for religious use (which follows the
> traditional count) while being honest for academic use.

```python
>>> from hebrewcal.eras.anno_mundi import traditional_vs_academic_gap, MISSING_YEARS_NOTICE
>>> traditional_vs_academic_gap()
165
>>> print(MISSING_YEARS_NOTICE)
The traditional Anno Mundi reckoning differs from academic-historical chronology by about 165 years for the Persian period (the 'missing years'). hebrewcal computes AM years exactly and does not silently correct this discrepancy; consumers needing historical alignment should apply the gap explicitly. See the project specification for details.
```

```{admonition} How to use the gap
:class: tip

If you are aligning Hebrew AM years with secular historical dates in the first millennium
BCE, apply `traditional_vs_academic_gap()` explicitly in your own code, and document that
you have done so. `hebrewcal` will never apply it for you, because for the modern and
medieval periods — and for all religious use — the traditional count is exactly what you
want.
```
