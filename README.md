# hebrewcal

[![CI](https://github.com/bsesic/hebrewcal/actions/workflows/ci.yml/badge.svg)](https://github.com/bsesic/hebrewcal/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/hebrewcal/badge/?version=latest)](https://hebrewcal.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://img.shields.io/pypi/v/hebrewcal.svg)](https://pypi.org/project/hebrewcal/)
[![Python versions](https://img.shields.io/pypi/pyversions/hebrewcal.svg)](https://pypi.org/project/hebrewcal/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A pure-Python library for the Hebrew calendar.

`hebrewcal` makes the Hebrew calendar usable programmatically and converts it
bidirectionally against the Gregorian and Julian calendars. Every computation is
performed locally — the library never issues network calls to any external service.

It is built for two audiences:

- **Religious use** — holidays (Israel and the Diaspora, including minority feasts and
  Shushan Purim), Shabbat candle lighting and Havdalah, zmanim, Torah readings, the Omer
  count, yahrzeit, and the sabbatical and jubilee cycle.
- **Academic use** — historical, medieval and ancient dates, Babylonian and biblical
  month names, proleptic calendars, the Julian/Gregorian reform, and the documented
  "missing years" of the Anno Mundi count.

> **Project status.** Early development. The calendar core, conversion and date handling
> (Phase 1) are implemented. Astronomy, holidays and religious times follow on the
> [roadmap](docs/specs/2026-06-03-architecture-roadmap.md).

## Installation

```bash
pip install hebrewcal
```

`hebrewcal` requires Python 3.11+ and has **no runtime dependencies** (standard library
only).

## Quick start

```python
from hebrewcal import GregorianDate, HebrewDate, to_hebrew, to_gregorian, weekday

# What Hebrew date and weekday corresponds to 31 October 1867?
g = GregorianDate(1867, 10, 31)
h = to_hebrew(g)
print(h)            # HebrewDate(year=5628, month=8, day=2)  -> 2 Marheshvan 5628
print(weekday(g).name)   # THURSDAY

# Convert a Hebrew date back to Gregorian.
print(to_gregorian(HebrewDate(5785, 7, 1)))   # GregorianDate(year=2024, month=10, day=3)
```

Every calendar reduces a date to an integer **Rata Die (RD)** day count and rebuilds a
date from it, so any two calendars are interconvertible through RD:

```python
from hebrewcal import GregorianDate, to_julian

GregorianDate(2026, 6, 26).to_rd()     # 739793
to_julian(GregorianDate(2026, 6, 26))  # JulianDate(year=2026, month=6, day=13)
```

## Features

- Proleptic **Gregorian** and **Julian** calendars, with an explicit, configurable
  Julian/Gregorian reform helper.
- A complete **Hebrew** calendar: molad and halakim, the dechiyot ("four gates"), year
  typing (deficient / regular / complete), the keviah signature, and the Metonic cycle.
- Bidirectional **conversion** between any supported calendars through Rata Die.
- **Parsing** of Gregorian input (ISO 8601, DIN 5008 and slash form) and **formatting**
  in numeric and named styles.
- A **gematria** converter between integers and Hebrew numerals.
- Month and weekday **name tables** (transliteration, Babylonian, biblical).
- The **Anno Mundi** era with a documented "missing years" notice.

## Documentation

Full documentation, including a user guide with many examples, lives at
**[hebrewcal.readthedocs.io](https://hebrewcal.readthedocs.io)**.

## Development

```bash
git clone https://github.com/bsesic/hebrewcal.git
cd hebrewcal
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

Run the lint gate and the test suite:

```bash
flake8
ruff check .
mypy
pytest
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the branching strategy and conventions.

## License

[MIT](LICENSE) © Benjamin Schnabel
