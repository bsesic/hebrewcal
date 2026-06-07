# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/bsesic/hebrewcal/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/bsesic/hebrewcal/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/bsesic/hebrewcal/releases/tag/v0.1.0
