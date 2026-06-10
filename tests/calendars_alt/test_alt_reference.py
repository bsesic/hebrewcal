"""Round-trip and structural validation for the alternative calendars.

These calendars have no widely available reference implementation; correctness
here rests on round-trip consistency and documented structural invariants. The
Qumran calendar is exact; the Samaritan model is computed; the Karaite calendar is
an astronomical estimate built on the verified true new moon (and is therefore
limited to the years the standard library's ``datetime`` supports).
"""

from __future__ import annotations

import pytest

from hebrewcal.calendars_alt.karaite import KaraiteDate
from hebrewcal.calendars_alt.qumran import QumranDate
from hebrewcal.calendars_alt.samaritan import SamaritanDate
from hebrewcal.core.rata_die import weekday_from_rd


@pytest.mark.parametrize("rd", [-200000, -1000, 0, 1, 500000, 739793])
def test_integer_calendars_round_trip(rd: int) -> None:
    # Qumran and Samaritan use pure integer arithmetic and work proleptically.
    assert QumranDate.from_rd(rd).to_rd() == rd
    assert SamaritanDate.from_rd(rd).to_rd() == rd


def test_karaite_round_trip_modern_range() -> None:
    # The Karaite estimate uses datetime/sunset, so it is exercised over a modern range.
    start = KaraiteDate(5770, 1, 1).to_rd()
    end = KaraiteDate(5795, 1, 1).to_rd()
    for rd in range(start, end, 17):
        assert KaraiteDate.from_rd(rd).to_rd() == rd


def test_qumran_year_invariants() -> None:
    # Exactly 364 days and a constant New Year weekday.
    weekdays = set()
    for year in range(1, 60):
        length = QumranDate(year + 1, 1, 1).to_rd() - QumranDate(year, 1, 1).to_rd()
        assert length == 364
        weekdays.add(weekday_from_rd(QumranDate(year, 1, 1).to_rd()))
    assert len(weekdays) == 1


def test_lunar_model_year_lengths() -> None:
    for year in range(5780, 5800):
        s_len = SamaritanDate(year + 1, 1, 1).to_rd() - SamaritanDate(year, 1, 1).to_rd()
        assert s_len in (353, 354, 355, 383, 384, 385)
        k_len = KaraiteDate(year + 1, 1, 1).to_rd() - KaraiteDate(year, 1, 1).to_rd()
        assert k_len in (354, 355, 383, 384)  # common ~354/355, leap ~383/384
