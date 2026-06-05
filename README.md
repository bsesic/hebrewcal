# hebrewcal

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

## Design

Everything pivots on the Rata Die (RD) day count from Dershowitz & Reingold,
*Calendrical Calculations*. Every calendar implements only `to_rd` and `from_rd`, so
conversion between any two calendars always goes through RD and new calendars plug in
without changes to the core.

## Status

Early development. See the [architecture and roadmap specification](docs/specs/2026-06-03-architecture-roadmap.md)
for the plan, and the [issues](https://github.com/bsesic/hebrewcal/issues) for tracked work.

## Requirements

- Python 3.11+
- No runtime dependencies (standard library only).

## Development

```bash
pip install -e ".[dev]"
pre-commit install

flake8
ruff check .
mypy
pytest
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow and conventions.

## License

[MIT](LICENSE)
