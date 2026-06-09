# hebrewcal

[![CI](https://github.com/bsesic/hebrewcal/actions/workflows/ci.yml/badge.svg)](https://github.com/bsesic/hebrewcal/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/hebrewcal/badge/?version=latest)](https://hebrewcal.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://img.shields.io/pypi/v/hebrewcal.svg)](https://pypi.org/project/hebrewcal/)
[![Python versions](https://img.shields.io/pypi/pyversions/hebrewcal.svg)](https://pypi.org/project/hebrewcal/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20583972.svg)](https://doi.org/10.5281/zenodo.20583972)

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

> **Project status.** Feature-complete against the roadmap: calendar core and conversion,
> astronomy, holidays, religious times, and alternative calendars are all implemented,
> documented and tested.

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

- Proleptic **Gregorian** and **Julian** calendars (explicit, configurable
  Julian/Gregorian reform) and a complete **Hebrew** calendar (molad/halakim, dechiyot,
  year typing, keviah, Metonic cycle), all interconvertible through **Rata Die**.
- **Parsing** (ISO 8601, DIN 5008, slash form), **formatting**, a **gematria** converter,
  month/weekday **name tables** (transliteration, Babylonian, biblical), and the
  **Anno Mundi** era with the documented "missing years" notice.
- **Astronomy** (pure Python): solar position, sunrise/sunset, twilight, the molad as a
  civil instant.
- **Holidays** for Israel and the Diaspora: festivals, fasts (with postponement), modern
  Israeli days, minority feasts, Rosh Chodesh, the Omer and the special Shabbatot.
- **Religious times**: Shabbat candle lighting and Havdalah, zmanim, the molad
  announcement, yahrzeit, Torah readings, and the Shmita cycle.
- **Alternative calendars**: the Qumran 364-day calendar, plus documented computed
  Samaritan and Karaite models.
- An optional **command-line interface** (see below).

## Command line

Installing the package provides a `hebrewcal` command (and `python -m hebrewcal`):

```console
$ hebrewcal convert 1867-10-31
2 Marheshvan 5628 (Yom Chamishi)

$ hebrewcal shabbat 2026-06-26 --lat 40.71 --lon -74.01 --tz America/New_York
Candle lighting: 20:13
Havdalah: 21:21
```

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

## Citation

If you use `hebrewcal` in academic work, please cite it. Citation metadata is provided in
[`CITATION.cff`](CITATION.cff), and each release is archived on Zenodo.

- **Concept DOI** (always resolves to the latest version): [10.5281/zenodo.20583972](https://doi.org/10.5281/zenodo.20583972)
- Each release also has its own version-specific DOI on the Zenodo record.

## License

[MIT](LICENSE) © Benjamin Schnabel
