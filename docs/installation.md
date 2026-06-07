# Installation

## Requirements

- **Python 3.11 or newer** (the library uses `zoneinfo` and modern typing features).
- **No runtime dependencies** — `hebrewcal` is written entirely against the Python
  standard library. Nothing is downloaded or queried at runtime.

## From PyPI

```bash
pip install hebrewcal
```

This installs the latest released version.

## From source

```bash
git clone https://github.com/bsesic/hebrewcal.git
cd hebrewcal
pip install .
```

## For development

Install the package in editable mode together with the development tooling
(pytest, ruff, flake8, mypy, pre-commit):

```bash
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install
```

To build the documentation locally, install the docs extra instead (or in addition):

```bash
pip install -e ".[docs]"
sphinx-build -b html docs docs/_build/html
```

## Verifying the installation

```python
import hebrewcal

print(hebrewcal.__version__)
```

```{admonition} No network, ever
:class: tip

`hebrewcal` performs every calendar, astronomical and religious computation locally.
It does not call any web service, which makes it suitable for offline, reproducible and
academic use.
```
