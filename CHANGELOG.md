# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/bsesic/hebrewcal/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/bsesic/hebrewcal/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/bsesic/hebrewcal/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/bsesic/hebrewcal/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/bsesic/hebrewcal/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/bsesic/hebrewcal/releases/tag/v0.1.0
