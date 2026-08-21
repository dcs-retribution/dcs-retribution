"""Kneeboard time rendering, local and Zulu."""

import datetime

from dcs import Point
from dcs.terrain import Caucasus

from game.ato.flightwaypoint import FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.missiongenerator.kneeboard import FlightPlanBuilder, format_kneeboard_time
from game.utils import NauticalUnits, feet

CAUCASUS = datetime.timezone(datetime.timedelta(hours=4))
LOCAL = datetime.datetime(1988, 7, 15, 7, 19, 13)


def test_local_time_renders_bare() -> None:
    assert format_kneeboard_time(LOCAL) == "07:19:13"


def test_utc_time_carries_the_z_suffix() -> None:
    utc = LOCAL.replace(tzinfo=datetime.timezone.utc)
    assert format_kneeboard_time(utc) == "07:19:13Z"


def test_annotation_puts_zulu_on_a_second_line() -> None:
    """Underneath rather than beside, so the table column does not widen."""
    assert format_kneeboard_time(LOCAL, CAUCASUS) == "07:19:13\n03:19:13Z"


def test_annotation_is_skipped_when_the_time_is_already_zulu() -> None:
    """An airframe on the UTC convention must not get the same time twice."""
    utc = LOCAL.replace(tzinfo=datetime.timezone.utc)
    assert format_kneeboard_time(utc, CAUCASUS) == "07:19:13Z"


def test_missing_time_renders_empty() -> None:
    assert format_kneeboard_time(None, CAUCASUS) == ""


#: Row order is #, Action, Alt, Dist, Bearing, GSPD, Time, Departure, Fuel.
TIME_COLUMN = 6
DEPARTURE_COLUMN = 7


def _takeoff_row(zulu_tz: datetime.timezone | None) -> list[str]:
    """One flight-plan row, built the way BriefingPage builds the table."""
    builder = FlightPlanBuilder(NauticalUnits(), zulu_tz)
    waypoint = FlightWaypoint(
        "TAKEOFF",
        FlightWaypointType.TAKEOFF,
        Point(0, 0, Caucasus()),
        feet(191),
        "BARO",
    )
    waypoint.tot = LOCAL
    waypoint.departure_time = LOCAL + datetime.timedelta(minutes=9)
    builder.add_waypoint(0, waypoint)
    return builder.rows[0]


def test_flight_plan_table_is_local_only_without_the_flag() -> None:
    row = _takeoff_row(None)
    assert row[TIME_COLUMN] == "07:19:13"
    assert row[DEPARTURE_COLUMN] == "07:28:13"


def test_flight_plan_table_annotates_when_the_airframe_asks() -> None:
    # The flag reached only the mission start time, which no page reads, so the
    # table printed local on every airframe that declared it.
    row = _takeoff_row(CAUCASUS)
    assert row[TIME_COLUMN] == "07:19:13\n03:19:13Z"
    assert row[DEPARTURE_COLUMN] == "07:28:13\n03:28:13Z"
