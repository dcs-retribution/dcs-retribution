"""Sunrise, sunset and moon for the Time & Weather dialog."""

from __future__ import annotations

import datetime

from dcs.mapping import LatLng

from game.weather.daylight import daylight_lines, moon_line, moon_phase, sun_times

UTC = datetime.timezone.utc


def _minutes(t: datetime.datetime) -> int:
    return t.hour * 60 + t.minute


def test_sun_times_west_of_greenwich() -> None:
    # Las Vegas on the solstice: 05:23 and 20:02 PDT.
    tz = datetime.timezone(datetime.timedelta(hours=-7))
    rise, sunset = sun_times(LatLng(36.17, -115.14), datetime.date(2026, 6, 21), tz)
    assert rise is not None and sunset is not None
    assert rise.date() == sunset.date() == datetime.date(2026, 6, 21)
    assert abs(_minutes(rise) - (5 * 60 + 23)) <= 5
    assert abs(_minutes(sunset) - (20 * 60 + 2)) <= 5


def test_sun_times_east_of_greenwich_stay_on_the_local_date() -> None:
    # Guam, +10: local sunrise falls on the prior UTC day.
    tz = datetime.timezone(datetime.timedelta(hours=10))
    rise, sunset = sun_times(LatLng(13.48, 144.79), datetime.date(2026, 5, 21), tz)
    assert rise is not None and sunset is not None
    assert rise.date() == sunset.date() == datetime.date(2026, 5, 21)
    assert rise.hour == 5 and sunset.hour == 18


def test_moon_phase_at_known_full_and_new_moons() -> None:
    full = moon_phase(datetime.datetime(2024, 1, 25, 17, 54, tzinfo=UTC))
    assert full.name == "full moon" and full.illumination > 0.97
    new = moon_phase(datetime.datetime(2024, 1, 11, 11, 57, tzinfo=UTC))
    assert new.name == "new moon" and new.illumination < 0.03


def test_moon_line_reads_as_a_percentage() -> None:
    tz = datetime.timezone(datetime.timedelta(hours=3))
    line = moon_line(datetime.datetime(2024, 1, 25, 20, 54), tz)
    assert line.startswith("Moon ") and "% lit, full moon" in line


def test_daylight_lines_place_the_start_against_the_sun() -> None:
    tz = datetime.timezone(datetime.timedelta(hours=3))
    rise = datetime.datetime(1995, 6, 9, 5, 28, tzinfo=tz)
    sunset = datetime.datetime(1995, 6, 9, 19, 42, tzinfo=tz)
    times, light = daylight_lines(datetime.datetime(1995, 6, 9, 18), rise, sunset)
    assert times == "Sunrise 05:28  ·  Sunset 19:42  (local)"
    assert light == "Starts in daylight, 1 h 42 min before sunset"
    _, light = daylight_lines(datetime.datetime(1995, 6, 9, 4, 28), rise, sunset)
    assert light == "Starts in the dark, 1 h before sunrise"
    _, light = daylight_lines(datetime.datetime(1995, 6, 9, 20, 0), rise, sunset)
    assert light == "Starts in the dark, 18 min after sunset"


def test_daylight_lines_in_polar_day() -> None:
    times, light = daylight_lines(datetime.datetime(2026, 6, 21, 12), None, None)
    assert times == "No sunrise or sunset on this date" and light == ""
