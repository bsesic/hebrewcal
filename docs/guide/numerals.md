# Hebrew numerals (gematria)

`hebrewcal.numerals` converts between integers and Hebrew numerals in both directions.
Hebrew numerals are additive: letters carry values (א = 1, י = 10, ק = 100, …) that are
summed.

## Integer → numeral

```python
>>> from hebrewcal.numerals import to_hebrew_numeral
>>> to_hebrew_numeral(1)
'א׳'
>>> to_hebrew_numeral(123)
'קכ״ג'
>>> to_hebrew_numeral(5785)
'ה׳תשפ״ה'
```

### Conventions implemented

- **15 and 16** are written טו (9 + 6) and טז (9 + 7) rather than יה / יו, to avoid
  writing fragments of the divine name:

  ```python
  >>> to_hebrew_numeral(15)
  'ט״ו'
  >>> to_hebrew_numeral(16)
  'ט״ז'
  ```

- **Punctuation.** A single-letter number takes a *geresh* (׳); a multi-letter number
  takes a *gershayim* (״) before its last letter.

- **Thousands.** A year like 5785 is written as the thousands group (ה = 5) followed by a
  geresh, then the remainder (תשפ״ה = 785): `ה׳תשפ״ה`.

## Numeral → integer

```python
>>> from hebrewcal.numerals import from_hebrew_numeral
>>> from_hebrew_numeral("קכ״ג")
123
>>> from_hebrew_numeral("ה׳תשפ״ה")
5785
```

Round-tripping holds for the values you are likely to use (years, day-of-month, counts):

```python
>>> from hebrewcal.numerals import to_hebrew_numeral, from_hebrew_numeral
>>> all(from_hebrew_numeral(to_hebrew_numeral(n)) == n
...     for n in (1, 7, 15, 16, 123, 248, 411, 785, 5785))
True
```

## Validation and limits

Only positive integers are representable:

```python
>>> to_hebrew_numeral(0)
Traceback (most recent call last):
    ...
ValueError: Hebrew numerals represent positive integers only
```

```{admonition} Exact thousands are ambiguous
:class: note

In this additive notation a bare multiple of 1000 (e.g. 1000 itself) cannot be
distinguished from its sub-thousand value and will round-trip to the smaller number.
Year-style numbers — a thousands group **followed by a remainder**, like 5785 — are
unambiguous, which covers the calendrical use cases.
```
