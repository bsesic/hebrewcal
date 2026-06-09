# Command-line interface

Installing `hebrewcal` provides a `hebrewcal` command (and the equivalent
`python -m hebrewcal`). It uses only the standard library and covers the everyday
tasks. Run `hebrewcal --help` or `hebrewcal <command> --help` for the full options.

## convert

Convert a Gregorian date (ISO 8601, DIN 5008 or slash form) to Hebrew (default) or Julian.

```console
$ hebrewcal convert 2024-10-03
1 Tishri 5785 (Yom Chamishi)
$ hebrewcal convert 26.06.2026
11 Tammuz 5786 (Yom Shishi)
$ hebrewcal convert 2026-06-26 --to julian
2026-06-13 (Julian)
```

## holidays

List the observances of a Hebrew (Anno Mundi) year; `--israel` selects the Israeli
schedule.

```console
$ hebrewcal holidays 5785
2024-10-03  Rosh Hashanah  [major_festival]
2024-10-04  Rosh Hashanah  [major_festival]
...
```

## parasha

The weekly Torah portion for a Shabbat (`--israel` for the Israeli schedule).

```console
$ hebrewcal parasha 2024-10-26
Bereshit
```

## shabbat and zmanim

These take a date and a location (`--lat`, `--lon` in degrees, `--tz` an IANA zone).

```console
$ hebrewcal shabbat 2026-06-26 --lat 40.71 --lon -74.01 --tz America/New_York
Candle lighting: 20:13
Havdalah: 21:21

$ hebrewcal zmanim 2026-06-26 --lat 31.77 --lon 35.21 --tz Asia/Jerusalem
Sunrise: 05:35
Sof zman Shma (GRA): 09:08
Chatzot: 12:42
Sunset: 19:48
Tzeit: 20:30
```
