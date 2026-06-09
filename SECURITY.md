# Security Policy

## Scope

`hebrewcal` is a pure-Python library with **no runtime dependencies** and performs **no
network access, file I/O, or subprocess execution**. Its attack surface is limited to the
parsing of caller-supplied date strings, which is handled with the standard library and
returns errors rather than executing input.

## Supported versions

Security fixes are applied to the latest released version on PyPI.

## Reporting a vulnerability

Please report suspected vulnerabilities privately via GitHub Security Advisories
("Report a vulnerability" on the repository's **Security** tab). If that is unavailable,
open a minimal issue asking for a private contact channel — do not include exploit
details in a public issue.

We aim to acknowledge reports within a few days.
