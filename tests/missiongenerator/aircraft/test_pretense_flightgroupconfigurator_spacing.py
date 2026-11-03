from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

import pytest
from dcs import Mission, Point
from dcs.planes import F_16C_50
from dcs.terrain import Caucasus

from game.pretense import pretenseflightgroupconfigurator as configurator_module
from game.pretense.pretenseflightgroupconfigurator import (
    PretenseFlightGroupConfigurator,
)


class GeometryReached(Exception):
    """Stop configure after it has applied airborne geometry."""


def test_configure_spaces_player_group_from_replaced_client_route() -> None:
    mission = Mission(Caucasus())
    group = mission.flight_group(
        mission.country("USA"),
        "Client flight",
        F_16C_50,
        airport=None,
        position=Point(10000, 10000, mission.terrain),
        altitude=5000,
        speed=200,
        group_size=2,
    )
    # The route initially points east; the rebuilt client route will point north.
    group.add_waypoint(Point(11000, 10000, mission.terrain), altitude=5000)
    leader_position = group.units[0].position
    control_point = SimpleNamespace(
        full_name="Northbound control point",
        position=Point(10000, 11000, mission.terrain),
    )
    flight = SimpleNamespace(
        flight_type=object(),
        client_count=1,
        roster=SimpleNamespace(members=[]),
        iter_members=lambda: iter(()),
        divert=None,
        unit_type=SimpleNamespace(fuel_consumption=None),
        arrival=SimpleNamespace(position=control_point.position),
        flight_plan=SimpleNamespace(waypoints=[]),
    )
    game = SimpleNamespace(
        theater=SimpleNamespace(controlpoints=[control_point]),
        settings=SimpleNamespace(),
    )
    configurator = PretenseFlightGroupConfigurator(
        flight,  # type: ignore[arg-type]
        group,
        game,  # type: ignore[arg-type]
        mission,
        datetime(2024, 1, 1),
        None,  # type: ignore[arg-type]
        None,  # type: ignore[arg-type]
        None,  # type: ignore[arg-type]
        None,  # type: ignore[arg-type]
        {},
        True,
    )
    configurator.setup_props = lambda: None  # type: ignore[method-assign]
    configurator.setup_payloads = lambda: None  # type: ignore[method-assign]
    configurator.setup_fuel = lambda: None  # type: ignore[method-assign]
    configurator.configure_flight_member = lambda *args: None  # type: ignore[method-assign]
    configurator.register_escort_leash = lambda: None  # type: ignore[method-assign]

    class NoOpBehavior:
        def __init__(self, *_args: Any) -> None:
            pass

        def apply_to(self, *_args: Any) -> None:
            pass

    class NoOpPainter:
        def __init__(self, *_args: Any) -> None:
            pass

        def apply_livery(self) -> None:
            pass

    class RouteGenerator:
        def __init__(self, *_args: Any) -> None:
            pass

        def create_waypoints(self) -> tuple[int, list[Any]]:
            return 0, []

    class RouteBuilder:
        def __init__(self, waypoint: Any, actual_group: Any, *_args: Any) -> None:
            self.waypoint = waypoint
            self.group = actual_group

        def build(self) -> None:
            self.group.add_waypoint(self.waypoint.position, altitude=5000)

    def stop_after_spacing(*_args: Any) -> None:
        raise GeometryReached

    with (
        patch.object(configurator, "setup_radios", return_value=None),
        patch.object(configurator_module, "AircraftBehavior", NoOpBehavior),
        patch.object(configurator_module, "AircraftPainter", NoOpPainter),
        patch.object(configurator_module, "WaypointGenerator", RouteGenerator),
        patch.object(configurator_module, "PydcsWaypointBuilder", RouteBuilder),
        patch.object(configurator_module, "BingoEstimator", stop_after_spacing),
    ):
        with pytest.raises(GeometryReached):
            configurator.configure()

    assert group.points[1].position == control_point.position
    assert group.units[0].position == leader_position
    serialized_units = list(group.dict()["units"].values())
    assert serialized_units[0]["heading"] == pytest.approx(1.5707963267948966)
    assert serialized_units[1]["heading"] == pytest.approx(1.5707963267948966)
    # For a northbound route, the second aircraft must be 50 m cross-track.
    assert abs(serialized_units[1]["x"] - serialized_units[0]["x"]) == pytest.approx(50)
    assert serialized_units[1]["y"] - serialized_units[0]["y"] == pytest.approx(0)
