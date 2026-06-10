# Religious times

Building on the {doc}`astronomy <astronomy>` and calendar layers, this part of the
library computes the times and observances of religious life: Shabbat candle lighting and
Havdalah, the zmanim, the molad / Rosh Chodesh announcement, yahrzeit, the Torah-reading
schedule, and the Shmita / Jubilee cycle.

## Shabbat candle lighting and Havdalah

Candle lighting is a fixed number of minutes before sunset (18 by default); Havdalah is
nightfall (a solar depression of 8.5° by default, or a fixed offset after sunset).

```python
>>> from hebrewcal.astro.location import Location
>>> from hebrewcal.calendars.gregorian import GregorianDate
>>> from hebrewcal.religious.shabbat import candle_lighting, havdalah
>>> nyc = Location(40.7128, -74.0060, timezone="America/New_York")
>>> candle_lighting(GregorianDate(2026, 6, 26), nyc).strftime("%H:%M")
'20:13'
>>> havdalah(GregorianDate(2026, 6, 27), nyc).strftime("%H:%M")
'21:21'
>>> candle_lighting(GregorianDate(2026, 6, 26), nyc, minutes_before_sunset=40).strftime("%H:%M")
'19:51'
```

## Zmanim

`Zmanim(date, location)` exposes the halachic times as methods returning timezone-aware
datetimes. Seasonal ("proportional") hours divide the day into twelve; the GRA day runs
sunrise→sunset, the MGA day dawn→nightfall.

```python
>>> from hebrewcal.religious.zmanim import Zmanim
>>> z = Zmanim(GregorianDate(2026, 6, 26), nyc)
>>> z.sunrise().strftime("%H:%M"), z.chatzot().strftime("%H:%M"), z.sunset().strftime("%H:%M")
('05:26', '12:58', '20:31')
>>> z.sof_zman_shma_gra().strftime("%H:%M")   # latest Shema (Vilna Gaon)
'09:12'
```

Available times: `alot_hashachar`, `misheyakir`, `sunrise`, `sof_zman_shma_gra` /
`sof_zman_shma_mga`, `sof_zman_tefilla_gra` / `sof_zman_tefilla_mga`, `chatzot`,
`mincha_gedola`, `mincha_ketana`, `plag_hamincha`, `sunset`, `tzeit_hakochavim`. Each
returns `None` at high latitudes where the underlying event does not occur.

### Opinions and variants

`alot_hashachar`, `misheyakir` and `tzeit_hakochavim` take a configurable solar
depression, and fixed-clock-minute variants are provided for the common opinions:

```python
>>> z = Zmanim(GregorianDate(2026, 6, 26), nyc)
>>> z.alot_hashachar(19.8) < z.alot_hashachar()        # a deeper (earlier) dawn opinion
True
>>> z.alot_hashachar_fixed(72) is not None              # 72 clock minutes before sunrise
True
>>> z.tzeit_rabbeinu_tam(72).strftime("%H:%M")          # Rabbeinu Tam nightfall
'21:43'
```

Sunrise/sunset can also be elevation-corrected via the astronomy layer
(`sunrise(date, location, elevation=True)`); see {doc}`astronomy`.

## Molad / Rosh Chodesh announcement

`month_announcement(year, month)` returns the molad, the Rosh Chodesh day(s) and the
Shabbat Mevarchim on which the month is blessed.

```python
>>> from hebrewcal.religious.announce import month_announcement
>>> a = month_announcement(5785, 9)   # Kislev 5785
>>> a.molad.strftime("%Y-%m-%d %H:%M")
'2024-12-01 10:49'
>>> [(d.month, d.day) for d in a.rosh_chodesh]
[(8, 30), (9, 1)]
>>> (a.shabbat_mevarchim.month, a.shabbat_mevarchim.day)
(8, 29)
```

## Yahrzeit

`yahrzeit(death, year)` returns the anniversary date in a later Hebrew year, handling the
30th-of-month and Adar edge cases.

```python
>>> from hebrewcal.calendars.hebrew import HebrewDate
>>> from hebrewcal.religious.yahrzeit import yahrzeit
>>> yahrzeit(HebrewDate(5780, 10, 10), 5785)   # 10 Tevet
HebrewDate(year=5785, month=10, day=10)
```

```{admonition} Edge cases
:class: note

- A death on 30 Marheshvan or 30 Kislev moves to the 1st of the next month in a year
  where that month has only 29 days.
- A death in Adar II of a leap year is observed in Adar (month 12) in a common year and
  in Adar II (month 13) in a leap year.
```

## Torah readings

`parasha(date, israel=False)` returns the weekly portion for a Shabbat, or `None` if the
date is not a Saturday or carries a festival reading. Combined portions are joined with a
hyphen (e.g. `Matot-Masei`).

```python
>>> from hebrewcal.religious.torah import parasha
>>> parasha(HebrewDate(5785, 7, 24))           # Diaspora
'Bereshit'
>>> parasha(HebrewDate(5785, 7, 17)) is None   # Shabbat Chol HaMoed Sukkot
True
>>> parasha(HebrewDate(5785, 8, 1), israel=True)   # the israel schedule is also available
'Noach'
```

Pass `israel=True` for the Israeli schedule. The Israel and Diaspora schedules differ for
a stretch in spring when the Diaspora's eighth day of Pesach falls on Shabbat, then
realign through the combination rules.

```{admonition} Verification
:class: note

The annual schedule was cross-checked against an independent reference on **10,024
Shabbatot (5755–5850, Israel and Diaspora) with zero structural mismatches**. The
combination of portions is fixed by the year type; the table is embedded so the library
stays dependency-free. A simple `triennial_portion` helper returns which third (1/2/3) is
read under the common triennial cycle.
```

## Shmita and Jubilee

```python
>>> from hebrewcal.religious.sabbatical import is_shmita, shmita_cycle_year, is_jubilee
>>> is_shmita(5782), is_shmita(5785)
(True, False)
>>> shmita_cycle_year(5785)   # position in the 7-year cycle
3
```

The Jubilee (`is_jubilee`) uses the nominal `year % 50` reckoning and is documented as a
conventional indicator only — it has not been observed since Temple times and the count
is disputed.
