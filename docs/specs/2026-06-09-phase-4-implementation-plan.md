# Phase 4 — Religious Times — Implementation Plan

> **Note:** Recorded after implementation; the code, tests and verification described here
> are in the repository.

**Goal:** The religious-time layer — Shabbat candle lighting and Havdalah, the zmanim,
the molad / Rosh Chodesh announcement, yahrzeit, the Torah-reading schedule (annual and a
simple triennial helper), and the Shmita / Jubilee cycle — built on the calendar and
astronomy layers, with no runtime dependencies.

**Architecture:** Time-of-day features build on `hebrewcal.astro` (sunrise/sunset/twilight
return timezone-aware datetimes; proportional "seasonal hours" are derived from them).
Date features (yahrzeit, Torah readings, Shmita) build on the calendar core. The Torah
schedule uses a verified year-type table of combined parashiyot plus festival-Shabbat
skipping.

**Issue map:** Task 1 → #51 · Task 2 → #52 · Task 3 → #53 · Task 4 → #54 · Task 5 → #55 ·
Task 6 → #56 · Task 7 → #57.

### Verified reference data

- Candle lighting = sunset − 18 min (default); NYC Fri 2026-06-26: sunset 20:31 → candle
  20:13; Havdalah at 8.5° = 21:21, at +72 min = 21:43.
- Shmita: a year is sabbatical iff `year % 7 == 0` (5782 was Shmita; next 5789).
- **Torah readings**: the annual schedule was verified against an independent reference
  (`pyluach`) on **10,024 Shabbatot (5755–5850, Israel and Diaspora) with zero structural
  mismatches**.

---

## File Structure

| File | Responsibility |
|------|----------------|
| `src/hebrewcal/religious/shabbat.py` | Candle lighting and Havdalah. |
| `src/hebrewcal/religious/zmanim.py` | Halachic times of the day. |
| `src/hebrewcal/religious/announce.py` | Molad / Rosh Chodesh announcement. |
| `src/hebrewcal/religious/yahrzeit.py` | Yahrzeit. |
| `src/hebrewcal/religious/torah.py` | Torah readings (annual + triennial helper). |
| `src/hebrewcal/religious/sabbatical.py` | Shmita and Jubilee. |

---

## Task 1: Shabbat candle lighting and Havdalah  (issue #51)

`religious/shabbat.py`: `candle_lighting(date, location, minutes_before_sunset=18)` returns
sunset minus the offset; `havdalah(date, location, depression=8.5, minutes_after_sunset=None)`
returns nightfall at the given solar depression, or a fixed offset after sunset. Both return
timezone-aware datetimes, or `None` at high latitudes where the event does not occur.

## Task 2: Zmanim (halachic times)  (issue #52)

`religious/zmanim.py`: a `Zmanim(date, location)` class exposing alot hashachar (16.1°),
misheyakir (11°), sunrise, sof zman Shma / Tefilla (GRA from sunrise, MGA from dawn),
chatzot (solar noon), mincha gedola/ketana, plag hamincha, sunset, and tzeit hakochavim
(8.5°). Seasonal ("proportional") hours divide the GRA day (sunrise→sunset) or the MGA day
(dawn 16.1°→dusk 16.1°) into twelve. Each method returns a timezone-aware datetime or
`None`. Tests assert the strict chronological ordering and that the MGA Shma deadline
precedes the GRA one.

## Task 3: Molad / Rosh Chodesh announcement  (issue #53)

`religious/announce.py`: `month_announcement(year, month)` returns a `MonthAnnouncement`
with the molad (from `hebrewcal.astro.molad`), the Rosh Chodesh day(s) (two when the
preceding month has 30 days), and the Shabbat Mevarchim (the Saturday on or before the day
before Rosh Chodesh).

## Task 4: Yahrzeit  (issue #54)

`religious/yahrzeit.py`: `yahrzeit(death, year)` returns the anniversary in a later year.
Edge cases: a 30 Marheshvan / 30 Kislev death moves to the 1st of the next month in a year
where that month has 29 days; Adar II maps to Adar (month 12) in a common year and Adar II
(13) in a leap year; Adar I maps to Adar.

## Task 5: Torah readings (annual + triennial)  (issue #55)

`religious/torah.py`: `parasha(date, israel=False)` returns the weekly portion for a
Shabbat, or `None` (non-Saturday or a festival Shabbat). The annual cycle begins with
Bereshit on the first Shabbat after Simchat Torah and runs through Ha'azinu. Which of the
seven combinable pairs are read together is fixed by the **year type**
`(is_leap, rosh_hashanah_weekday, year_length, israel)`; a 28-entry table (14 per locale)
encodes the combined-pair sets. The schedule is produced by walking the Shabbatot from the
Bereshit Shabbat, skipping festival Shabbatot, and assigning parashiyot in order with the
year's combinations. `triennial_portion` returns which third (1/2/3) under the common
triennial cycle (documented as a guide, not a ruling).

**Verification:** the year-type → combination determinism (14 distinct types per locale,
zero conflicts over 200 years) and the full per-Shabbat schedule were checked against
`pyluach` with zero structural mismatches.

## Task 6: Shmita and Jubilee  (issue #56)

`religious/sabbatical.py`: `is_shmita(year)` (= `year % 7 == 0`), `shmita_cycle_year(year)`
(1–7, 7 = Shmita), and `is_jubilee(year)` (nominal `year % 50`, documented as conventional).

## Task 7: Religious-times reference-validation suite  (issue #57)

`tests/religious/test_reference_times.py`: candle-lighting reference (NYC), Havdalah after
candle lighting, Torah-reading reference dates for 5785 (Diaspora), and the Shmita anchor.

---

## Notes on correctness and references

- Candle lighting / Havdalah / zmanim build directly on the verified astronomy layer.
- The Torah-reading annual schedule was verified against an independent reference on
  thousands of Shabbatot (both locales) with zero structural mismatches; the year-type
  table is embedded so the library stays dependency-free.
- Shmita uses the conventional `year % 7 == 0` (5782 anchor); the Jubilee indicator is
  nominal. The triennial cycle and some yahrzeit edge conventions vary between communities
  and are documented as guides.
