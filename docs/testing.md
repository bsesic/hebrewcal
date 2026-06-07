# Testing and development

## Setting up a development environment

```bash
git clone https://github.com/bsesic/hebrewcal.git
cd hebrewcal
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install
```

## Running the test suite

The project uses **pytest**:

```bash
pytest
```

With coverage:

```bash
pytest --cov --cov-report=term-missing
```

Run a single module or test:

```bash
pytest tests/calendars/test_hebrew.py
pytest tests/test_conversion.py::test_acceptance_1867_10_31
```

## The lint gate

Every commit must pass the lint gate and the tests. Run them before committing:

```bash
flake8          # the lint gate
ruff check .    # fast linter and import sorting
mypy            # static type checking (strict)
pytest          # the test suite
```

`pre-commit install` wires these to run automatically on `git commit`.

## How the tests are organised

The test tree mirrors the package:

| Tests | Cover |
|-------|-------|
| `tests/core/` | Rata Die and the calendar interface |
| `tests/calendars/` | Gregorian, Julian and Hebrew date types |
| `tests/hebrew/` | the arithmetic engine (metonic, molad, dechiyot, yeartype, keviah) |
| `tests/parsing/`, `tests/formatting/` | text input and output |
| `tests/eras/` | the Anno Mundi era |
| `tests/test_numerals.py`, `tests/test_names.py` | gematria and name tables |
| `tests/test_conversion.py` | the high-level conversion API |
| `tests/test_reference_dates.py` | cross-checked reference dates and round-trips |

## Correctness strategy

- **Round-trip properties.** For each calendar, `from_rd(to_rd(d)) == d` is tested across
  wide and proleptic ranges, including negative RD values.
- **Independent cross-checks.** Gregorian RD values are checked against Python's own
  proleptic ordinal (`datetime.date.toordinal`). Hebrew/Gregorian correspondences use
  well-known fixed points.
- **No silent magic.** The Julian/Gregorian reform and the Anno Mundi "missing years" are
  surfaced explicitly and covered by tests, never applied behind your back.

```{admonition} Continuous integration
:class: note

GitHub Actions runs the full gate (ruff, flake8, mypy, pytest) on Python 3.11, 3.12 and
3.13 for every push and pull request.
```
