"""Core machinery: the Rata Die day count and the abstract Calendar interface.

This package is the hub of the library. ``rata_die`` defines the RD epoch and
arithmetic; ``calendar`` defines the abstract base class that every concrete
calendar implements via ``to_rd`` / ``from_rd``.
"""
