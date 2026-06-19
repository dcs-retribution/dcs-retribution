from types import SimpleNamespace

from dcs import Point
from dcs.terrain import Caucasus

from game.ato.flightwaypoint import FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.missiongenerator.aircraft.waypoints.pydcswaypointbuilder import (
    PydcsWaypointBuilder,
)
from game.missiongenerator.aircraft.waypoints.target import TargetBuilder


def _waypoint(custom_name: str | None) -> FlightWaypoint:
    wp = FlightWaypoint(
        "[OBJ] : Scud #0", FlightWaypointType.TARGET_POINT, Point(0, 0, Caucasus())
    )
    wp.custom_name = custom_name
    return wp


def _base_builder(custom_name: str | None) -> PydcsWaypointBuilder:
    builder = PydcsWaypointBuilder.__new__(PydcsWaypointBuilder)
    builder.waypoint = _waypoint(custom_name)
    return builder


def _target_builder(custom_name: str | None, f15e: bool) -> TargetBuilder:
    builder = TargetBuilder.__new__(TargetBuilder)
    builder.waypoint = _waypoint(custom_name)
    builder.flight = SimpleNamespace(  # type: ignore[assignment]
        unit_type=SimpleNamespace(use_f15e_waypoint_names=f15e)
    )
    return builder


def test_dcs_name_uses_custom_name_when_set() -> None:
    assert _base_builder("SCUD1").dcs_name_for_waypoint() == "SCUD1"


def test_dcs_name_falls_back_to_name_when_unset() -> None:
    assert _base_builder(None).dcs_name_for_waypoint() == "[OBJ] : Scud #0"


def test_dcs_name_ignores_override_for_structural_join_waypoint() -> None:
    # JOIN's generated name is matched downstream (formation/EW jamming); a rename must not
    # reach the .miz or that logic breaks, so the canonical name wins.
    builder = _base_builder("MyJoin")
    builder.waypoint.name = "JOIN"
    assert builder.dcs_name_for_waypoint() == "JOIN"


def test_dcs_name_ignores_override_for_dropoffzone_waypoint() -> None:
    # DROPOFFZONE drives the CTLD air-assault split trigger (landingzone.py).
    builder = _base_builder("LZ Alpha")
    builder.waypoint.name = "DROPOFFZONE"
    assert builder.dcs_name_for_waypoint() == "DROPOFFZONE"


def test_target_builder_non_f15e_uses_custom_name() -> None:
    assert _target_builder("SCUD1", f15e=False).dcs_name_for_waypoint() == "SCUD1"


def test_target_builder_f15e_wraps_custom_name() -> None:
    assert _target_builder("SCUD1", f15e=True).dcs_name_for_waypoint() == "#T SCUD1"


def test_target_builder_f15e_falls_back_to_name() -> None:
    assert (
        _target_builder(None, f15e=True).dcs_name_for_waypoint() == "#T [OBJ] : Scud #0"
    )
