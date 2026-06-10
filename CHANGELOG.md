# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2026-06-10

### Added

- Additional **zmanim opinions**: `alot_hashachar`, `misheyakir` and
  `tzeit_hakochavim` take a configurable solar depression, plus fixed-minute
  variants `alot_hashachar_fixed`, `tzeit_fixed` and `tzeit_rabbeinu_tam`.
- Optional **elevation** correction for `sunrise`/`sunset` (`elevation=True`),
  using the geometric horizon dip `acos(R/(R+h))` (`elevation_depression`).

## [1.2.0] - 2026-06-09

### Added

- The **true astronomical new moon** (`hebrewcal.astro.lunar`): `nth_new_moon`,
  `new_moon_at_or_after` and `new_moon_before`, computed with the Meeus periodic
  terms and distinct from the calendar's mean molad (the two differ by up to
  ~14 hours). Verified against an independent ephemeris to ~1 minute.

## [1.1.0] - 2026-06-09

### Added

- Native **Hebrew-script** output: `hebrew_month_name(..., system="hebrew")` and
  `weekday_name(..., hebrew=True)`, a `format_hebrew(date, style="hebrew")` that
  renders the day and year as gematria numerals (e.g. `א׳ תשרי ה׳תשפ״ה`), and a
  `hebrewcal convert --hebrew` CLI flag.

## [1.0.0] - 2026-06-09

First stable release. Completes the roadmap: calendar core and conversion, astronomy,
holidays, religious times, alternative calendars, and a command-line interface — all in
pure Python with no runtime dependencies. The public API is now considered stable.

### Added

- An optional command-line interface: the `hebrewcal` console script (and
  `python -m hebrewcal`) with `convert`, `holidays`, `parasha`, `shabbat` and
  `zmanim` subcommands.
- Curated public API surface: `hebrewcal.astro`, `hebrewcal.religious` and
  `hebrewcal.calendars_alt` re-export their key names with explicit `__all__`.
- `SECURITY.md`.

### Changed

- Memoised the heavily-used year-keyed helpers (`calendar_elapsed_days`,
  `year_length_correction`, `new_year_rd`) for faster holiday/Torah computation.
- Documentation polished for 1.0 (CLI guide, refreshed README and feature list).
- Marked the development status as Production/Stable.

## [0.5.0] - 2026-06-09

Phase 5 of the roadmap: alternative calendars.

### Added

- Alternative calendars (via the same Rata Die interface):
  - The **Qumran / Jubilees** 364-day solar calendar (exact: four 91-day
    quarters, every year starts on the same weekday, no intercalation).
  - A **Samaritan** computed mean-lunar model and a **Karaite** computed
    approximation (mean conjunction with a one-day sighting lag). Both are
    clearly documented as computed models that are not verified against an
    authoritative source and, for the Karaite calendar, do not replace
    observation.

## [0.4.0] - 2026-06-09

Phase 4 of the roadmap: the religious-time layer.

### Added

- Religious-time layer, built on the astronomy and calendar layers:
  - Shabbat (and yom tov) candle lighting and Havdalah, with configurable offsets.
  - Zmanim (halachic times): alot, misheyakir, sunrise, sof zman Shma/Tefilla
    (GRA and MGA), chatzot, mincha gedola/ketana, plag hamincha, sunset, tzeit.
  - The molad / Rosh Chodesh announcement (Shabbat Mevarchim).
  - Yahrzeit, with the 30th-of-month and Adar edge cases.
  - The Torah-reading schedule (annual cycle, Israel and Diaspora, plus a simple
    triennial helper), verified against an independent reference on thousands of
    Shabbatot.
  - The Shmita (sabbatical) and Jubilee cycle.

## [0.3.0] - 2026-06-07

Phase 3 of the roadmap: the holiday engine. This release completes the MVP
(calendar core, astronomy and holidays).

### Added

- Holiday engine for the Hebrew year: a `Holiday` value type, a `Category` enum,
  and `holidays(year, diaspora=...)` / `holidays_on(date)`.
- Major festivals with Israel/Diaspora differences (second festival day, Simchat
  Torah placement, 7- vs 8-day Pesach, 1 vs 2 days Shavuot), plus Chol HaMoed.
- Minor festivals (Hanukkah, Tu BiShvat, Purim and Shushan Purim with leap-year
  Adar II placement, Lag BaOmer, Tu B'Av, Pesach Sheni) and Rosh Chodesh.
- Public fasts with their postponement rules (Tzom Gedaliah, Asara B'Tevet,
  Ta'anit Esther, Shiva Asar B'Tammuz, Tisha B'Av, Ta'anit Bechorot).
- Modern Israeli days with the statutory weekday adjustments (Yom HaShoah,
  Yom HaZikaron, Yom HaAtzmaut, Yom Yerushalayim).
- Minority/communal feasts (Sigd, Mimouna).
- The Omer count (`omer_count`, `omer_week_day`).
- The special Shabbatot (Shekalim, Zachor, Parah, HaChodesh, HaGadol, Shuvah,
  Chazon, Nachamu).

## [0.2.0] - 2026-06-07

Phase 2 of the roadmap: the astronomy layer.

### Added

- Astronomy layer (pure Python, no dependencies): a `Location` value type
  (coordinates, elevation, IANA time zone).
- A Julian Day time base derived from the Rata Die count, and a bridge between
  RD/UTC-minutes and timezone-aware datetimes.
- A NOAA/Meeus solar position model (declination, equation of time), with
  `sunrise`, `sunset` and `solar_noon` agreeing with reference implementations
  to within ~20 seconds at mid latitudes.
- Civil, nautical and astronomical twilight (`dawn`, `dusk`) with a configurable
  solar depression angle.
- The molad expressed as a civil instant in Jerusalem mean time.

## [0.1.1] - 2026-06-07

### Added

- `CITATION.cff` and `.zenodo.json` metadata for citation and Zenodo archival
  (DOI). No functional code changes.

## [0.1.0] - 2026-06-07

First release. Phase 0 (infrastructure) and Phase 1 (calendar core, conversion and date
handling) of the roadmap.

### Added

- Project scaffolding and infrastructure: `src/` layout, PEP 621 `pyproject.toml`,
  package skeleton for all roadmap subpackages.
- Tooling: pytest, ruff, flake8, mypy, and pre-commit configuration.
- GitHub Actions CI with a test matrix across Python 3.11–3.13.
- Sphinx documentation and ReadTheDocs build configuration.
- PyPI release workflow using Trusted Publishing (OIDC).
- `CONTRIBUTING.md` describing the workflow and conventions.
- Calendar core: the Rata Die day count, the `CalendarDate` interface and a
  `convert()` helper routing every conversion through RD.
- Proleptic Gregorian and Julian calendars, the latter with an explicit
  Julian/Gregorian reform helper.
- Hebrew calendar arithmetic: the Metonic cycle, molad and halakim, the dechiyot
  year-length correction, year typing (deficient/regular/complete with month
  lengths) and the keviah signature.
- Hebrew date type with bidirectional RD conversion.
- High-level conversion API (`to_gregorian`, `to_julian`, `to_hebrew`, `weekday`).
- Gregorian date parsing (ISO 8601, DIN 5008 and slash form).
- Date formatting (numeric and named styles).
- Hebrew numeral (gematria) converter.
- Month and weekday name tables (transliteration, Babylonian, biblical).
- Anno Mundi era with a documented "missing years" notice.

[Unreleased]: https://github.com/bsesic/hebrewcal/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/bsesic/hebrewcal/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/bsesic/hebrewcal/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/bsesic/hebrewcal/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/bsesic/hebrewcal/compare/v0.5.0...v1.0.0
[0.5.0]: https://github.com/bsesic/hebrewcal/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/bsesic/hebrewcal/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/bsesic/hebrewcal/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/bsesic/hebrewcal/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/bsesic/hebrewcal/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/bsesic/hebrewcal/releases/tag/v0.1.0
