"""Convert between integers and Hebrew numerals (gematria).

Hebrew numerals are additive letter values. Conventions implemented here:
- 15 and 16 are written ט״ו and ט״ז (9+6, 9+7) to avoid spelling fragments of
  the divine name.
- A geresh (׳) marks a single-letter number; a gershayim (״) is inserted before
  the last letter of a multi-letter number.
- Thousands are written as the hundreds-or-less value followed by a geresh, then
  the remainder (e.g. 5785 -> ה׳תשפ״ה).
"""

from __future__ import annotations

GERESH = "׳"
GERSHAYIM = "״"

# Letter values in descending order. 15 and 16 are handled specially below.
_VALUES: tuple[tuple[int, str], ...] = (
    (400, "ת"),
    (300, "ש"),
    (200, "ר"),
    (100, "ק"),
    (90, "צ"),
    (80, "פ"),
    (70, "ע"),
    (60, "ס"),
    (50, "נ"),
    (40, "מ"),
    (30, "ל"),
    (20, "כ"),
    (10, "י"),
    (9, "ט"),
    (8, "ח"),
    (7, "ז"),
    (6, "ו"),
    (5, "ה"),
    (4, "ד"),
    (3, "ג"),
    (2, "ב"),
    (1, "א"),
)
_LETTER_TO_VALUE = {letter: value for value, letter in _VALUES}


def _letters_for(value: int) -> str:
    """Return the bare letters (no punctuation) for 1..999."""
    out: list[str] = []
    remaining = value
    for amount, letter in _VALUES:
        # Special-case the tens-and-units 15 and 16.
        if remaining in (15, 16):
            out.append("ט")  # 9
            out.append("ו" if remaining == 15 else "ז")  # 6 / 7
            remaining = 0
            break
        while remaining >= amount:
            out.append(letter)
            remaining -= amount
    return "".join(out)


def _punctuate(letters: str) -> str:
    """Add geresh/gershayim to a bare letter string."""
    if len(letters) == 1:
        return letters + GERESH
    return letters[:-1] + GERSHAYIM + letters[-1]


def _sum_letters(letters: str, text: str) -> int:
    """Sum the values of bare numeral letters, raising on any non-letter."""
    total = 0
    for char in letters:
        value = _LETTER_TO_VALUE.get(char)
        if value is None:
            raise ValueError(f"not a Hebrew numeral: {text!r}")
        total += value
    return total


def to_hebrew_numeral(number: int) -> str:
    """Convert a positive integer to its Hebrew numeral string.

    Note: an exact multiple of 1000 with no remainder (e.g. 1000) is ambiguous in
    this additive notation and round-trips to its sub-1000 value; year-style
    numbers (a thousands group followed by a remainder, e.g. 5785) are
    unambiguous.
    """
    if number <= 0:
        raise ValueError("Hebrew numerals represent positive integers only")
    thousands, rest = divmod(number, 1000)
    parts: list[str] = []
    if thousands:
        parts.append(_letters_for(thousands) + GERESH)
    if rest:
        parts.append(_punctuate(_letters_for(rest)))
    return "".join(parts)


def from_hebrew_numeral(text: str) -> int:
    """Convert a Hebrew numeral string back to an integer."""
    cleaned = text.strip().replace(GERSHAYIM, "")
    thousands = 0
    geresh_index = cleaned.find(GERESH)
    if geresh_index != -1 and geresh_index != len(cleaned) - 1:
        # A geresh with letters after it separates the thousands group.
        thousands = _sum_letters(cleaned[:geresh_index], text)
        cleaned = cleaned[geresh_index + 1:]
    # Any remaining geresh is the single-number marker; drop it.
    cleaned = cleaned.replace(GERESH, "")
    total = thousands * 1000 + _sum_letters(cleaned, text)
    if total <= 0:
        raise ValueError(f"not a Hebrew numeral: {text!r}")
    return total
