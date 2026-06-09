"""Tests for the command-line interface."""

from __future__ import annotations

import pytest

from hebrewcal.cli import main


def test_convert_to_hebrew(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["convert", "2024-10-03"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Tishri" in out
    assert "5785" in out


def test_convert_hebrew_script(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["convert", "2024-10-03", "--hebrew"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "תשרי" in out  # Tishri in Hebrew script


def test_convert_to_julian(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["convert", "2026-06-26", "--to", "julian"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "2026-06-13" in out


def test_holidays(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["holidays", "5785"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Yom Kippur" in out
    assert "Hanukkah" in out


def test_parasha(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["parasha", "2024-10-26"])  # 24 Tishri 5785, a Saturday
    out = capsys.readouterr().out
    assert rc == 0
    assert "Bereshit" in out


def test_shabbat(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(
        ["shabbat", "2026-06-26", "--lat", "40.71", "--lon", "-74.01", "--tz", "America/New_York"]
    )
    out = capsys.readouterr().out
    assert rc == 0
    assert "Candle lighting" in out
    assert "Havdalah" in out


def test_invalid_date_returns_error(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["convert", "not-a-date"])
    assert rc != 0
