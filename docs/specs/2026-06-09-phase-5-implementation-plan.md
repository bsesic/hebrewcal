# Phase 5 — Alternative Calendars — Implementation Plan

> **Note:** Recorded after implementation; the code, tests and verification described here
> are in the repository.

**Goal:** Add the alternative Jewish calendars — Qumran / Jubilees, Samaritan and Karaite
— through the same Rata Die interface as the main calendars, with no runtime dependencies.

**Scope decision (agreed up front):** unlike the earlier phases, the Samaritan and Karaite
calendars have **no widely available reference implementation** to validate against. All
three were nevertheless implemented, **clearly labelled**:

- **Qumran** is an exact, fully verifiable calendar.
- **Samaritan** is a *computed mean-lunar model* — not an authoritative reproduction of
  the calendar set by the Samaritan priesthood.
- **Karaite** is a *computed approximation* of an observational calendar (first-sighting
  of the moon + the aviv barley) and must not be used to determine observance.

Each module carries a prominent warning in its docstring, and the documentation repeats
the caveat.

**Issue map:** Task 1 → #63 (Qumran) · Task 2 → #61 (Samaritan) · Task 3 → #62 (Karaite) ·
Task 4 → #64 (validation).

---

## File Structure

| File | Responsibility |
|------|----------------|
| `src/hebrewcal/calendars_alt/qumran.py` | Qumran / Jubilees 364-day calendar (exact). |
| `src/hebrewcal/calendars_alt/_meanlunar.py` | Shared mean-conjunction lunar engine. |
| `src/hebrewcal/calendars_alt/samaritan.py` | Samaritan computed model. |
| `src/hebrewcal/calendars_alt/karaite.py` | Karaite computed approximation. |

---

## Task 1: Qumran / Jubilees 364-day calendar  (issue #63)

`calendars_alt/qumran.py`: a `QumranDate` with `to_rd` / `from_rd`. The year is a fixed
**364 days**: four quarters of 91 days, each three months of 30, 30, 31 (so months 3, 6, 9
and 12 have 31 days). Because 364 = 52 weeks exactly, **every year begins on the same
weekday** and there is no intercalation (the calendar drifts against the seasons). The
epoch is conventional: year 1, month 1, day 1 is anchored to the Wednesday on or after the
proleptic Gregorian March equinox of year 1 (the Jubilees New Year is a Wednesday).

**Verification:** exact — round-trips over wide/proleptic ranges; the year is always 364
days; New Year is always the same weekday.

## Task 2: Samaritan calendar — computed model  (issue #61)

A shared engine, `calendars_alt/_meanlunar.py`, implements a mean-conjunction lunar
calendar: the mean synodic month (29 d 12 h 793 p), 12 or 13 months on the 19-year Metonic
cycle, an integer month index from the epoch, and an optional whole-day `lag`.
`calendars_alt/samaritan.py` instantiates it (`lag = 0`) anchored to the Anno Mundi epoch
so year numbers approximate the traditional count.

```{warning}
This is a computed mean-lunar model, not an authoritative reproduction of the Samaritan
calendar. The living Samaritan calendar is fixed by the Samaritan High Priesthood; the
absolute correspondence and year numbering here are conventional, and the model is not
verified against an authoritative source.
```

## Task 3: Karaite calendar — computed approximation  (issue #62)

`calendars_alt/karaite.py` instantiates the same engine with a **one-day lag**, standing
in for the delay between conjunction and first sighting.

```{warning}
The authentic Karaite calendar is observational (new-moon sighting over the Land of Israel
and the ripeness of the barley) and cannot be reduced to a formula. This module provides a
computed approximation only; it is not verified against actual practice and should not be
used to determine observance.
```

## Task 4: Alternative-calendars validation suite  (issue #64)

`tests/calendars_alt/test_alt_reference.py`: round-trip (`from_rd(to_rd(d)) == d`) over
wide, including proleptic, ranges for all three; the Qumran year is exactly 364 days with a
constant New-Year weekday; the lunar models produce 353–385-day years; the Karaite model
lags the Samaritan model by exactly one day.

---

## Notes on correctness and references

- The Qumran calendar is exact and fully verified structurally.
- The Samaritan and Karaite calendars are computed models; their epochs and year numbering
  are conventional and they are **not** verified against an authoritative source. They
  demonstrate the extensible calendar interface and the mean-lunar structure, and are
  documented as such in both the code and the user guide.
