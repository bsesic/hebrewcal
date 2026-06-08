"""Cross-checked reference dates for holidays (verified against pyluach)."""

from __future__ import annotations

from hebrewcal.conversion import to_gregorian
from hebrewcal.religious.holidays import holidays


def _greg(year: int, name: str, diaspora: bool = True) -> set[tuple[int, int, int]]:
    out: set[tuple[int, int, int]] = set()
    for h in holidays(year, diaspora):
        if h.name == name:
            g = to_gregorian(h.date)
            out.add((g.year, g.month, g.day))
    return out


def test_rosh_hashanah_5785() -> None:
    assert (2024, 10, 3) in _greg(5785, "Rosh Hashanah")


def test_yom_kippur_5785() -> None:
    assert _greg(5785, "Yom Kippur") == {(2024, 10, 12)}


def test_hanukkah_first_day_5785() -> None:
    assert (2024, 12, 26) in _greg(5785, "Hanukkah")


def test_purim_5785() -> None:
    assert _greg(5785, "Purim") == {(2025, 3, 14)}


def test_pesach_first_day_5785() -> None:
    assert (2025, 4, 13) in _greg(5785, "Pesach")


def test_yom_haatzmaut_2025() -> None:
    # 5785: moved to Thursday 1 May 2025.
    assert _greg(5785, "Yom HaAtzmaut") == {(2025, 5, 1)}


def test_diaspora_vs_israel_pesach_length() -> None:
    israel = [h for h in holidays(5785, diaspora=False) if h.name == "Pesach"]
    diaspora = [h for h in holidays(5785, diaspora=True) if h.name == "Pesach"]
    assert len(diaspora) == len(israel) + 1  # the eighth day
