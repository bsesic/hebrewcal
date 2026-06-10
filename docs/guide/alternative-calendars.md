# Alternative calendars

These calendars plug into the same Rata Die interface as the main calendars
(`to_rd` / `from_rd`), so they interconvert with Gregorian, Julian and Hebrew dates.

```{admonition} Status and verification
:class: warning

Unlike the rest of the library, the Samaritan and Karaite calendars have **no widely
available reference implementation** to check against. The **Qumran** calendar is exact
and fully verified structurally. The **Samaritan** and **Karaite** calendars are
**computed models**, clearly labelled as such: their epochs and year numbering are
conventional, they are not verified against an authoritative source, and the Karaite model
is an approximation that does **not** replace observation. Use them for structural and
academic purposes, not to determine religious observance.
```

## Qumran / Jubilees (364-day)

The calendar of the Dead Sea Scrolls and the Book of Jubilees: a fixed 364-day year of
four 91-day quarters (months of 30, 30, 31 days, so months 3, 6, 9 and 12 have 31). Since
364 = 52 weeks exactly, every year begins on the same weekday and there is no
intercalation (it drifts against the seasons).

```python
>>> from hebrewcal.calendars_alt.qumran import QumranDate, days_in_year
>>> days_in_year()
364
>>> QumranDate(2, 1, 1).to_rd() - QumranDate(1, 1, 1).to_rd()
364
>>> from hebrewcal.core.rata_die import weekday_from_rd
>>> {weekday_from_rd(QumranDate(y, 1, 1).to_rd()) for y in range(1, 50)}
{3}
```

Conversion works through RD like any calendar:

```python
>>> from hebrewcal import GregorianDate
>>> from hebrewcal.calendars_alt.qumran import QumranDate
>>> QumranDate.from_rd(GregorianDate(2026, 6, 26).to_rd())
QumranDate(year=2033, month=3, day=6)
```

## Samaritan (computed model)

A mean-conjunction lunar calendar (mean synodic month, 12 or 13 months on the 19-year
Metonic cycle), anchored so that year numbers approximate the traditional count.

```python
>>> from hebrewcal.calendars_alt.samaritan import SamaritanDate
>>> from hebrewcal import GregorianDate
>>> GregorianDate.from_rd(SamaritanDate(5785, 1, 1).to_rd())
GregorianDate(year=2024, month=10, day=3)
```

## Karaite (astronomical estimate)

The authentic Karaite calendar is **observational** (first sighting of the new crescent
over the Land of Israel, with the year set by the ripeness of the spring barley). This
module gives an **astronomical estimate**, built on verified astronomy:

- A month begins on the evening of estimated first crescent visibility over Jerusalem —
  the first sunset, at or after the **true** lunar conjunction
  ({doc}`astronomy`), at which the moon is at least 20 hours old (a simple age criterion,
  not a full altitude/elongation visibility model).
- The year begins with the month whose 15th day (Passover) is the first on or after the
  vernal equinox (an approximation of the aviv rule).

```python
>>> from hebrewcal.calendars_alt.karaite import KaraiteDate
>>> from hebrewcal import GregorianDate
>>> GregorianDate.from_rd(KaraiteDate(5785, 1, 1).to_rd())    # Aviv (month 1) begins in spring
GregorianDate(year=2025, month=3, day=31)
>>> GregorianDate.from_rd(KaraiteDate(5785, 1, 15).to_rd())   # Passover, on/after the equinox
GregorianDate(year=2025, month=4, day=14)
```

```{admonition} Estimate, not observance
:class: warning

The underlying astronomy (true conjunction, sunset, equinox) is verified, but the calendar
is **not** validated against actual Karaite practice — real sightings and barley reports
can differ, especially in the choice of the leap month. Because it uses ``datetime``, it is
limited to the years 1–9999. Do not use it to determine observance.
```
