"""Smoke tests for package metadata and importability."""

from __future__ import annotations

import hebrewcal


def test_version_is_exposed() -> None:
    assert isinstance(hebrewcal.__version__, str)
    assert hebrewcal.__version__


def test_subpackages_import() -> None:
    # Each roadmap subpackage must import cleanly so the skeleton stays valid.
    import importlib

    for name in (
        "core",
        "calendars",
        "hebrew",
        "eras",
        "parsing",
        "formatting",
        "astro",
        "religious",
        "calendars_alt",
    ):
        importlib.import_module(f"hebrewcal.{name}")
