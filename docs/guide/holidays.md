# Holidays

The holiday engine produces every observance of a Hebrew year — festivals, fasts, modern
Israeli days, minority feasts, Rosh Chodesh and the special Shabbatot — with the
Israel/Diaspora differences resolved. It is built entirely on the calendar core.

## The engine

`holidays(year, diaspora=True)` returns a chronologically sorted list of `Holiday`
objects for a Hebrew year; `holidays_on(date)` filters to a single Hebrew date.

```python
>>> from hebrewcal.religious.holidays import holidays, holidays_on
>>> from hebrewcal.calendars.hebrew import HebrewDate
>>> days = holidays(5785)              # Diaspora by default
>>> days[0].name, days[0].category.value
('Rosh Hashanah', 'major_festival')
>>> [h.name for h in holidays_on(HebrewDate(5785, 7, 10))]
['Yom Kippur']
```

A `Holiday` records a `name`, a `HebrewDate` (`date`) and a `Category`:

```python
>>> from hebrewcal.religious.holidays import Category
>>> list(Category)  # doctest: +ELLIPSIS
[<Category.MAJOR_FESTIVAL: 'major_festival'>, ...]
```

### Looking up by a civil date

Convert the Gregorian date to Hebrew first:

```python
>>> from hebrewcal import GregorianDate, to_hebrew
>>> from hebrewcal.religious.holidays import holidays_on
>>> [h.name for h in holidays_on(to_hebrew(GregorianDate(2024, 12, 26)))]
['Hanukkah']
```

## Israel vs. Diaspora

Pass `diaspora=False` for the Israeli calendar. The differences are handled
automatically: the second festival day (yom tov sheni), Simchat Torah on 22 Tishri in
Israel versus 23 in the Diaspora, a 7-day Pesach versus 8, and one day of Shavuot
versus two.

```python
>>> from hebrewcal.religious.holidays import holidays_on
>>> from hebrewcal.calendars.hebrew import HebrewDate
>>> "Simchat Torah" in {h.name for h in holidays_on(HebrewDate(5785, 7, 22), diaspora=False)}
True
>>> "Simchat Torah" in {h.name for h in holidays_on(HebrewDate(5785, 7, 22), diaspora=True)}
False
```

## Categories

```{admonition} Category values
:class: note

`MAJOR_FESTIVAL`, `CHOL_HAMOED`, `MINOR_FESTIVAL`, `FAST`, `MODERN`, `ROSH_CHODESH`,
`SPECIAL_SHABBAT`, `MINORITY`.
```

- **Major festivals** — Rosh Hashanah, Yom Kippur, Sukkot (+ Shemini Atzeret / Simchat
  Torah), Pesach, Shavuot.
- **Minor festivals** — Hanukkah, Tu BiShvat, Purim and Shushan Purim, Lag BaOmer, Tu
  B'Av, Pesach Sheni, Hoshana Rabbah.
- **Fasts** — with postponement (see below).
- **Modern** — Yom HaShoah, Yom HaZikaron, Yom HaAtzmaut, Yom Yerushalayim.
- **Rosh Chodesh** — one or two days per month (not Tishri).
- **Special Shabbatot** — Shekalim, Zachor, Parah, HaChodesh, HaGadol, Shuvah, Chazon,
  Nachamu.
- **Minority** — Sigd (Ethiopian Jewry), Mimouna (North African communities).

## Fasts and postponement

A fast that would fall on Shabbat is moved: most fasts are postponed to Sunday, while
Ta'anit Esther (and Ta'anit Bechorot) are brought forward to the preceding Thursday.
Asara B'Tevet is never postponed.

```python
>>> from hebrewcal.religious.holidays import holidays_on
>>> from hebrewcal.calendars.hebrew import HebrewDate
>>> # 3 Tishri 5785 is Shabbat, so Tzom Gedaliah is observed on 4 Tishri.
>>> "Tzom Gedaliah" in {h.name for h in holidays_on(HebrewDate(5785, 7, 4))}
True
```

## Leap years

In a leap year Purim falls in Adar II; Purim Katan marks 14 Adar I.

```python
>>> from hebrewcal.religious.holidays import holidays_on
>>> from hebrewcal.calendars.hebrew import HebrewDate
>>> "Purim" in {h.name for h in holidays_on(HebrewDate(5784, 13, 14))}       # Adar II
True
>>> "Purim Katan" in {h.name for h in holidays_on(HebrewDate(5784, 12, 14))}  # Adar I
True
```

## The Omer count

`omer_count` returns the day of the Omer (1–49) or `None` outside the count; `omer_week_day`
gives the (weeks, days) breakdown.

```python
>>> from hebrewcal.religious.omer import omer_count, omer_week_day
>>> from hebrewcal.calendars.hebrew import HebrewDate
>>> omer_count(HebrewDate(5785, 1, 16))     # 16 Nisan = day 1
1
>>> omer_count(HebrewDate(5785, 2, 18))     # Lag BaOmer = day 33
33
>>> omer_week_day(HebrewDate(5785, 2, 18))  # 4 weeks and 5 days
(4, 5)
```

```{admonition} Verification
:class: note

Classical festivals, fasts, Hanukkah, Purim and the Omer are cross-checked against an
independent Hebrew-calendar reference; the modern Israeli days reproduce the published
official dates for recent years.
```
