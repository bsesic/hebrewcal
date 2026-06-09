"""Entry point for ``python -m hebrewcal``."""

from __future__ import annotations

import sys

from hebrewcal.cli import main

if __name__ == "__main__":
    sys.exit(main())
