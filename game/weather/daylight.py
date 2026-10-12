"""Sunrise, sunset and the moon for the Time & Weather dialog.

suntime answers in UTC for a UTC day, so a local date is shifted per event: an
east-of-Greenwich sunrise falls on the prior UTC day, a far-west sunset on the next.
"""

from __future__ import annotations

import datetime
import math
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Tuple

from dcs.mapping import LatLng, Point
from suntime import Sun, SunTimeException  # type: ignore

if TYPE_CHECKING:
    from game.theater import ConflictTheater

SYNODIC_MONTH_DAYS = 29.530588853
# A known new moon (2000-01-06 18:14 UTC); the mean-phase method drifts under a day.
_REFERENCE_NEW_MOON = datetime.datetime(
    2000, 1, 6, 18, 14, tzinfo=datetime.timezone.utc
)
_PHASE_NAMES = (
    "new moon",
    "waxing crescent",
    "first quarter",
    "waxing gibbous",
    "full moon",
    "waning gibbous",
    "last quarter",
    "waning crescent",
)


def _utc_day(day: datetime.date, hour: int, tz: datetime.tzinfo) -> datetime.datetime:
    utc = (
        datetime.datetime(day.year, day.month, day.day, hour, tzinfo=tz)
        .astimezone(datetime.timezone.utc)
        .date()
    )
    return datetime.datetime(utc.year, utc.month, utc.day)


def sun_times(
    latlng: LatLng, day: datetime.date, tz: Optional[datetime.tzinfo]
) -> Tuple[Optional[datetime.datetime], Optional[datetime.datetime]]:
    """Sunrise and sunset on a local date, in local time; None in polar day or night."""
    sun = Sun(latlng.lat, latlng.lng)
    try:
        if tz is not None:
            rise = sun.get_sunrise_time(_utc_day(day, 6, tz))
            sunset = sun.get_sunset_time(_utc_day(day, 18, tz))
        else:
            midnight = datetime.datetime(day.year, day.month, day.day)
            rise = sun.get_sunrise_time(midnight)
            sunset = sun.get_sunset_time(midnight)
    except SunTimeException:
        return None, None
    if tz is not None:
        rise, sunset = rise.astimezone(tz), sunset.astimezone(tz)
    # suntime's clock time is right but its date can slip a day (Guam's sunset came
    # back on the prior day), so pin both to the asked-for date.
    return (
        datetime.datetime.combine(day, rise.timetz()),
        datetime.datetime.combine(day, sunset.timetz()),
    )


@dataclass(frozen=True)
class MoonPhase:
    #: Fraction of the disc lit, 0 to 1.
    illumination: float
    name: str


def moon_phase(moment: datetime.datetime) -> MoonPhase:
    """The moon at a tz-aware moment."""
    age_days = (moment - _REFERENCE_NEW_MOON).total_seconds() / 86400
    fraction = (age_days % SYNODIC_MONTH_DAYS) / SYNODIC_MONTH_DAYS
    illumination = (1 - math.cos(2 * math.pi * fraction)) / 2
    return MoonPhase(illumination, _PHASE_NAMES[round(fraction * 8) % 8])


def _clock(time: datetime.datetime) -> str:
    return time.strftime("%H:%M")


def _duration(delta: datetime.timedelta) -> str:
    minutes = round(abs(delta.total_seconds()) / 60)
    hours, minutes = divmod(minutes, 60)
    if hours and minutes:
        return f"{hours} h {minutes} min"
    if hours:
        return f"{hours} h"
    return f"{minutes} min"


def daylight_lines(
    start: datetime.datetime,
    sunrise: Optional[datetime.datetime],
    sunset: Optional[datetime.datetime],
) -> Tuple[str, str]:
    """The sun times and where the mission start falls against them.

    `start` is naive local time, as the mission clock is.
    """
    if sunrise is None or sunset is None:
        return "No sunrise or sunset on this date", ""
    rise = sunrise.replace(tzinfo=None)
    down = sunset.replace(tzinfo=None)
    times = f"Sunrise {_clock(rise)}  ·  Sunset {_clock(down)}  (local)"
    if start < rise:
        where = f"Starts in the dark, {_duration(rise - start)} before sunrise"
    elif start < down:
        where = f"Starts in daylight, {_duration(down - start)} before sunset"
    else:
        where = f"Starts in the dark, {_duration(start - down)} after sunset"
    return times, where


def moon_line(start: datetime.datetime, tz: Optional[datetime.tzinfo]) -> str:
    moment = start.replace(tzinfo=tz or datetime.timezone.utc)
    moon = moon_phase(moment)
    return f"Moon {round(moon.illumination * 100)}% lit, {moon.name}"


def theater_middle(theater: ConflictTheater) -> LatLng:
    """The middle of the campaign's bases, off-map spawns left out."""
    from game.theater.controlpoint import OffMapSpawn

    points = [
        cp.position for cp in theater.controlpoints if not isinstance(cp, OffMapSpawn)
    ] or [cp.position for cp in theater.controlpoints]
    x = sum(p.x for p in points) / len(points)
    y = sum(p.y for p in points) / len(points)
    return Point(x, y, theater.terrain).latlng()
