# Contributing to hebrewcal

Thank you for contributing. This document describes the workflow and conventions
for the project.

## Language

All code comments, docstrings, commit messages, issues, and pull/merge requests
are written in **English**.

## Issue-driven work

All work is tracked with **GitHub Issues** — todos, features, bug fixes, and
chores. Open an issue before starting work and close it when the work is merged.
Each roadmap phase has a corresponding milestone.

## Branching strategy

- `main` — releases and deployment. Protected; only merged via pull request.
- `development` — the integration branch for ongoing work.
- `feature/<short-name>` — a new feature; branched off `development`.
- `bugfix/<short-name>` — a bug fix; branched off `development`.
- Anything else gets its own descriptively named branch.

Branch off `development`, open a pull request back into `development`, and
reference the issues it closes (for example, `Closes #12`).

## Before every commit

Run the lint gate and the test suite locally:

```bash
flake8
ruff check .
mypy
pytest
```

Installing the pre-commit hooks runs these automatically:

```bash
pip install -e ".[dev]"
pre-commit install
```

## Commit messages

- Written in English, in the imperative mood.
- A short summary line, optionally followed by a body explaining the *why*.
- Conventional prefixes are encouraged (`feat:`, `fix:`, `docs:`, `test:`,
  `refactor:`, `chore:`).

## Project principles

- **Pure Python, no runtime dependencies** — everything is computed locally.
- **No network calls** to any external service.
- The Rata Die day count is the conversion pivot; new calendars implement only
  `to_rd` / `from_rd`.
