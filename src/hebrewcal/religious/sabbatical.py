"""The Shmita (sabbatical) and Yovel (jubilee) cycle.

A year is a Shmita year when ``year % 7 == 0`` in the conventional reckoning used
today (5782 was the most recent Shmita year). The cycle year runs 1-7, with 7 being
Shmita. The Jubilee (50th year) has not been observed since Temple times and its
reckoning is disputed; this module exposes a conventional ``year % 50 == 0`` test
and documents that it is nominal.
"""

from __future__ import annotations


def is_shmita(year: int) -> bool:
    """Return whether the Hebrew ``year`` is a Shmita (sabbatical) year."""
    return year % 7 == 0


def shmita_cycle_year(year: int) -> int:
    """Return the year's position in the seven-year cycle (1-7; 7 is Shmita)."""
    return 7 if year % 7 == 0 else year % 7


def is_jubilee(year: int) -> bool:
    """Return whether ``year`` is a Jubilee year by the nominal ``year % 50`` reckoning.

    The Jubilee has not been observed since Temple times and the count is disputed;
    this is a conventional indicator only.
    """
    return year % 50 == 0
