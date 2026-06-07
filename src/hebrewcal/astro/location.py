"""The geographic location type used by all astronomical computations."""

from __future__ import annotations

from dataclasses import dataclass
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


@dataclass(frozen=True)
class Location:
    """A geographic location.

    Attributes:
        latitude: Degrees north of the equator, in [-90, 90].
        longitude: Degrees east of the prime meridian, in [-180, 180].
        elevation: Metres above sea level (default 0).
        timezone: An IANA time-zone name (default "UTC").
    """

    latitude: float
    longitude: float
    elevation: float = 0.0
    timezone: str = "UTC"

    def __post_init__(self) -> None:
        if not -90.0 <= self.latitude <= 90.0:
            raise ValueError(f"latitude out of range: {self.latitude}")
        if not -180.0 <= self.longitude <= 180.0:
            raise ValueError(f"longitude out of range: {self.longitude}")
        try:
            ZoneInfo(self.timezone)
        except (ZoneInfoNotFoundError, ValueError) as exc:
            raise ValueError(f"unknown time zone: {self.timezone!r}") from exc

    @property
    def tzinfo(self) -> ZoneInfo:
        """Return the :class:`zoneinfo.ZoneInfo` for this location's time zone."""
        return ZoneInfo(self.timezone)
