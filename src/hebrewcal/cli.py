"""A small command-line interface for hebrewcal.

Exposed as the ``hebrewcal`` console script and via ``python -m hebrewcal``.
Uses only the standard library (argparse).
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from hebrewcal import GregorianDate, to_hebrew, to_julian, weekday
from hebrewcal.astro.location import Location
from hebrewcal.conversion import to_gregorian
from hebrewcal.names import hebrew_month_name, weekday_name
from hebrewcal.parsing.dates import parse_gregorian
from hebrewcal.religious.holidays import holidays
from hebrewcal.religious.shabbat import candle_lighting, havdalah
from hebrewcal.religious.torah import parasha
from hebrewcal.religious.zmanim import Zmanim


def _hebrew_label(g: GregorianDate) -> str:
    h = to_hebrew(g)
    name = hebrew_month_name(h.year, h.month)
    return f"{h.day} {name} {h.year} ({weekday_name(weekday(g))})"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hebrewcal", description="Hebrew calendar tools.")
    sub = parser.add_subparsers(dest="command", required=True)

    convert = sub.add_parser("convert", help="Convert a Gregorian date.")
    convert.add_argument("date", help="Gregorian date (ISO 8601, DIN 5008 or slash form).")
    convert.add_argument("--to", choices=("hebrew", "julian"), default="hebrew")

    hol = sub.add_parser("holidays", help="List the holidays of a Hebrew year.")
    hol.add_argument("year", type=int, help="Hebrew (Anno Mundi) year.")
    hol.add_argument("--israel", action="store_true", help="Use the Israeli schedule.")

    par = sub.add_parser("parasha", help="Weekly Torah portion for a Shabbat.")
    par.add_argument("date", help="Gregorian date of the Shabbat.")
    par.add_argument("--israel", action="store_true")

    location_commands = (
        ("shabbat", "Candle lighting and Havdalah."),
        ("zmanim", "Halachic times."),
    )
    for name, helptext in location_commands:
        loc = sub.add_parser(name, help=helptext)
        loc.add_argument("date", help="Gregorian date.")
        loc.add_argument("--lat", type=float, required=True, help="Latitude (degrees north).")
        loc.add_argument("--lon", type=float, required=True, help="Longitude (degrees east).")
        loc.add_argument("--tz", default="UTC", help="IANA time-zone name.")

    return parser


def _fmt(value: object) -> str:
    return value.strftime("%H:%M") if hasattr(value, "strftime") else "n/a (no event)"


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line interface. Returns a process exit code."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "convert":
            g = parse_gregorian(args.date)
            if args.to == "hebrew":
                print(_hebrew_label(g))
            else:
                j = to_julian(g)
                print(f"{j.year}-{j.month:02d}-{j.day:02d} (Julian)")
        elif args.command == "holidays":
            for h in holidays(args.year, diaspora=not args.israel):
                g = to_gregorian(h.date)
                print(f"{g.year}-{g.month:02d}-{g.day:02d}  {h.name}  [{h.category.value}]")
        elif args.command == "parasha":
            g = parse_gregorian(args.date)
            name = parasha(to_hebrew(g), israel=args.israel)
            print(name if name is not None else "(no weekly parasha on this date)")
        elif args.command == "shabbat":
            g = parse_gregorian(args.date)
            loc = Location(args.lat, args.lon, timezone=args.tz)
            print(f"Candle lighting: {_fmt(candle_lighting(g, loc))}")
            print(f"Havdalah: {_fmt(havdalah(g, loc))}")
        elif args.command == "zmanim":
            g = parse_gregorian(args.date)
            z = Zmanim(g, Location(args.lat, args.lon, timezone=args.tz))
            print(f"Sunrise: {_fmt(z.sunrise())}")
            print(f"Sof zman Shma (GRA): {_fmt(z.sof_zman_shma_gra())}")
            print(f"Chatzot: {_fmt(z.chatzot())}")
            print(f"Sunset: {_fmt(z.sunset())}")
            print(f"Tzeit: {_fmt(z.tzeit_hakochavim())}")
    except ValueError as exc:
        print(f"error: {exc}")
        return 2
    return 0
