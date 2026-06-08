# Astronomy and locations

The astronomy layer computes the sun's position and the day's solar events for any
location — in pure Python, with no dependencies and no network calls. It is the
foundation for the religious times (Shabbat, zmanim) that arrive in a later phase.

```{admonition} Accuracy and range
:class: note

Sunrise and sunset agree with NOAA / reference implementations to within about 15-20
seconds at mid latitudes (the target is one minute). Because the layer bridges to
`datetime`, it is limited to the years `datetime` supports (1–9999).
```

## Locations

A `Location` carries coordinates, an optional elevation and an IANA time-zone name.
Latitude and longitude are decimal degrees; longitude is **positive east**.

```python
>>> from hebrewcal.astro.location import Location
>>> nyc = Location(40.7128, -74.0060, timezone="America/New_York")
>>> jerusalem = Location(31.7683, 35.2137, elevation=754.0, timezone="Asia/Jerusalem")
>>> nyc.timezone
'America/New_York'
```

Out-of-range coordinates or an unknown time zone raise `ValueError`.

## Sunrise, sunset and solar noon

The event functions take a `GregorianDate` and a `Location` and return a timezone-aware
`datetime` in the location's zone (or `None` at high latitudes where the event does not
occur that day).

```python
>>> from hebrewcal.astro.solar import sunrise, sunset, solar_noon
>>> from hebrewcal.calendars.gregorian import GregorianDate
>>> date = GregorianDate(2026, 6, 26)
>>> sunrise(date, nyc).strftime("%H:%M")
'05:26'
>>> sunset(date, nyc).strftime("%H:%M")
'20:31'
>>> solar_noon(date, nyc).strftime("%H:%M")
'12:58'
```

```{admonition} Events are absolute instants
:class: warning

The returned `datetime` is a true instant converted to the location's zone, so its civil
date may differ from the input date — for example a sunset just after midnight during
polar summer. Compare instants, not wall-clock fields, when this matters.
```

### Polar days and nights

When the sun does not rise or set on a given date, the function returns `None`:

```python
>>> north = Location(89.9, 0.0, timezone="UTC")
>>> sunrise(GregorianDate(2026, 6, 21), north) is None   # midnight sun
True
```

## Twilight

`dawn` and `dusk` take a solar depression angle below the horizon. The standard angles are
provided as constants; the default is civil twilight.

```python
>>> from hebrewcal.astro.solar import (
...     dawn, dusk, CIVIL_DEPRESSION, NAUTICAL_DEPRESSION, ASTRONOMICAL_DEPRESSION,
... )
>>> dawn(date, nyc).strftime("%H:%M")        # civil dawn (default)
'04:53'
>>> dusk(date, nyc, ASTRONOMICAL_DEPRESSION).strftime("%H:%M")
'22:37'
```

| Constant | Depression | Meaning |
|----------|-----------|---------|
| `CIVIL_DEPRESSION` | 6° | civil twilight |
| `NAUTICAL_DEPRESSION` | 12° | nautical twilight |
| `ASTRONOMICAL_DEPRESSION` | 18° | astronomical twilight |

The general form accepts any angle, which later phases reuse for several zmanim.

## Lower-level solar terms

If you need the raw quantities, `solar_declination` and `equation_of_time` are available:

```python
>>> from hebrewcal.astro.solar import solar_declination, equation_of_time
>>> round(solar_declination(2026, 6, 21), 2)   # near the June solstice
23.44
>>> round(equation_of_time(2026, 11, 3), 1)    # minutes, early November maximum
16.5
```

## The molad as a civil instant

The molad is the calendar's **mean** lunar conjunction. `molad_moment` returns it as a
naive datetime in **Jerusalem mean time** (the molad "day" begins at 18:00 the previous
evening); `molad_breakdown` gives the traditional day/hours/parts presentation.

```python
>>> from hebrewcal.astro.molad import molad_moment, molad_breakdown
>>> molad_moment(5785, 7).strftime("%Y-%m-%d %H:%M")    # molad of Tishri 5785
'2024-10-03 09:21'
>>> day_index, hours, parts = molad_breakdown(5785, 7)
>>> hours, parts                                         # after 18:00
(15, 391)
```

```{admonition} Mean vs. true conjunction
:class: note

The molad is a *mean* conjunction and can differ from the true astronomical new moon by
up to ~14 hours. This module exposes the molad for comparison; it does not compute true
syzygy. The interval between consecutive molads is exactly 29 days, 12 hours and 793
parts.
```
