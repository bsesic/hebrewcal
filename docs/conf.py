"""Sphinx configuration for the hebrewcal documentation."""

from __future__ import annotations

from importlib import metadata

project = "hebrewcal"
author = "Benjamin Schnabel"
copyright = "2026, Benjamin Schnabel"

try:
    release = metadata.version("hebrewcal")
except metadata.PackageNotFoundError:
    release = "0.0.0.dev0"
version = release

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "myst_parser",
]

templates_path = ["_templates"]
# The specs directory holds internal planning documents (roadmap, implementation
# plans); they live in the repo but are not part of the published documentation.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "specs/**"]

# Public types are intentionally re-exported from the package root (e.g.
# ``hebrewcal.GregorianDate``) as well as their defining module, so type
# annotations have more than one valid cross-reference target. Suppress that
# specific ambiguity warning; genuine broken refs still surface in review.
suppress_warnings = ["ref.python"]

html_theme = "furo"
html_static_path = ["_static"]

autodoc_typehints = "description"
autodoc_member_order = "bysource"

napoleon_google_docstring = True
napoleon_numpy_docstring = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
