# User guide

The guide explains each part of the library in depth. It is organised from the
foundational concept (the Rata Die day count) outward to the individual calendars and the
supporting tools.

```{toctree}
:maxdepth: 1

rata-die
calendars
parsing
formatting
numerals
names
hebrew-internals
anno-mundi
astronomy
holidays
```

## How the pieces fit together

```{admonition} The one rule
:class: note

A calendar date converts to an integer **Rata Die (RD)** and rebuilds from one
(`to_rd` / `from_rd`). Conversion between any two calendars always routes through RD, so
adding a new calendar never touches existing ones.
```

- {doc}`rata-die` — the day-count pivot, the `Weekday` enum and `convert()`.
- {doc}`calendars` — the Gregorian, Julian and Hebrew date types and the reform helper.
- {doc}`parsing` and {doc}`formatting` — reading and rendering dates.
- {doc}`numerals` — integers ↔ Hebrew numerals.
- {doc}`names` — month and weekday name tables.
- {doc}`hebrew-internals` — the molad, dechiyot, year typing, keviah and Metonic cycle.
- {doc}`anno-mundi` — the era count and the "missing years".
