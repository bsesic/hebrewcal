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

## Karaite (computed approximation)

The authentic Karaite calendar is observational (new-moon sighting over the Land of Israel
and the ripeness of the barley). This model approximates it with the mean conjunction plus
a one-day sighting lag.

```python
>>> from hebrewcal.calendars_alt.karaite import KaraiteDate
>>> from hebrewcal.calendars_alt.samaritan import SamaritanDate
>>> KaraiteDate(5785, 1, 1).to_rd() - SamaritanDate(5785, 1, 1).to_rd()   # the one-day lag
1
```
