# Month and weekday names

`hebrewcal.names` provides name tables for months and weekdays in several systems.

## Month numbering

`hebrewcal` uses the **standard** month numbering throughout:

| # | Name | # | Name |
|---|------|---|------|
| 1 | Nisan | 7 | **Tishri** (civil new year) |
| 2 | Iyyar | 8 | Marheshvan |
| 3 | Sivan | 9 | Kislev |
| 4 | Tammuz | 10 | Tevet |
| 5 | Av | 11 | Shevat |
| 6 | Elul | 12 | Adar (Adar I in a leap year) |
|   |      | 13 | Adar II (leap years only) |

## Month names

`hebrew_month_name(year, month, system=...)` returns the name. Three systems are
available: `"transliteration"` (default), `"babylonian"` and `"biblical"`.

```python
>>> from hebrewcal.names import hebrew_month_name
>>> hebrew_month_name(5785, 7)
'Tishri'
>>> hebrew_month_name(5785, 7, system="babylonian")
'Tashritu'
>>> hebrew_month_name(5785, 1, system="biblical")
'Aviv'
```

Native **Hebrew script** is available too (`system="hebrew"`):

```python
>>> hebrew_month_name(5785, 7, system="hebrew")
'תשרי'
>>> hebrew_month_name(5784, 13, system="hebrew")   # Adar II in a leap year
'אדר ב׳'
```

The `year` matters because leap years rename month 12:

```python
>>> hebrew_month_name(5784, 12)   # 5784 is a leap year
'Adar I'
>>> hebrew_month_name(5784, 13)
'Adar II'
>>> hebrew_month_name(5785, 12)   # 5785 is a common year
'Adar'
```

```{admonition} Naming systems at a glance
:class: note

- **Transliteration** — the everyday Modern-Hebrew transliterations (Tishri, Kislev, …).
- **Babylonian** — the Akkadian month names the post-exilic calendar adopted
  (Tashritu, Kislimu, …), useful for ancient Near-Eastern context.
- **Biblical** — the handful of names attested in the Hebrew Bible (Aviv, Ziv, Ethanim,
  Bul); other months fall back to the transliteration.
```

## Weekday names

`weekday_name(weekday)` takes the **Sunday = 0 … Saturday = 6** index used everywhere in
the library (see {doc}`rata-die`).

```python
>>> from hebrewcal.names import weekday_name
>>> weekday_name(0)
'Yom Rishon'
>>> weekday_name(6)
'Shabbat'
```

Pass `hebrew=True` for native Hebrew script (`weekday_name(6, hebrew=True)` → `שבת`).

Combine it with `weekday()` to label any date:

```python
>>> from hebrewcal import GregorianDate, weekday
>>> from hebrewcal.names import weekday_name
>>> weekday_name(weekday(GregorianDate(1867, 10, 31)))
'Yom Chamishi'
```

An out-of-range value or unknown system raises `ValueError`.
