"""Round-trip and structural validation for the alternative calendars.

These calendars have no widely available reference implementation; correctness
here rests on round-trip consistency and documented structural invariants (the
Qumran calendar is exact, the Samaritan and Karaite models are computed).
"""

from __future__ import annotations

import pytest

from hebrewcal.calendars_alt.karaite import KaraiteDate
from hebrewcal.calendars_alt.qumran import QumranDate
from hebrewcal.calendars_alt.samaritan import SamaritanDate
from hebrewcal.core.rata_die import weekday_from_rd


@pytest.mark.parametrize("rd", [-200000, -1000, 0, 1, 500000, 739793])
def test_all_alt_calendars_round_trip(rd: int) -> None:
    assert QumranDate.from_rd(rd).to_rd() == rd
    assert SamaritanDate.from_rd(rd).to_rd() == rd
    assert KaraiteDate.from_rd(rd).to_rd() == rd


def test_qumran_year_invariants() -> None:
    # Exactly 364 days and a constant New Year weekday.
    weekdays = set()
    for year in range(1, 60):
        length = QumranDate(year + 1, 1, 1).to_rd() - QumranDate(year, 1, 1).to_rd()
        assert length == 364
        weekdays.add(weekday_from_rd(QumranDate(year, 1, 1).to_rd()))
    assert len(weekdays) == 1


def test_lunar_models_year_lengths() -> None:
    for cls in (SamaritanDate, KaraiteDate):
        for year in range(5780, 5800):
            length = cls(year + 1, 1, 1).to_rd() - cls(year, 1, 1).to_rd()
            assert length in (353, 354, 355, 383, 384, 385)


def test_karaite_lags_samaritan_by_one_day() -> None:
    for year in range(5780, 5800):
        assert KaraiteDate(year, 1, 1).to_rd() == SamaritanDate(year, 1, 1).to_rd() + 1
