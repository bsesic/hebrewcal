"""Tests for the Shmita and Jubilee cycle."""

from __future__ import annotations

from hebrewcal.religious.sabbatical import is_jubilee, is_shmita, shmita_cycle_year


def test_known_shmita_years() -> None:
    # 5782 (2021-22) was a Shmita year; 5789 is the next.
    assert is_shmita(5782) is True
    assert is_shmita(5789) is True
    assert is_shmita(5785) is False


def test_cycle_year() -> None:
    assert shmita_cycle_year(5782) == 7
    assert shmita_cycle_year(5783) == 1


def test_jubilee_is_a_bool() -> None:
    assert isinstance(is_jubilee(5785), bool)
