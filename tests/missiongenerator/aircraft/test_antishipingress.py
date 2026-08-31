import logging
import math
from types import SimpleNamespace
from typing import Any, Callable, cast
from unittest.mock import MagicMock

import pytest
from dcs import Point
from dcs.planes import A_10C
from dcs.point import MovingPoint
from dcs.task import (
    AttackGroup,
    Bombing,
    CarpetBombing,
    ControlledTask,
    EngageTargetsInZone,
    WeaponType,
)
from dcs.terrain import Terrain
from dcs.vehicles import Armor

from game.ato.flighttype import FlightType
from game.data.groups import GroupTask
from game.dcs.groundunittype import GroundUnitType
from game.missiongenerator.aircraft.waypoints.antishipingress import (
    AntiShipIngressBuilder,
)
from game.missiongenerator.aircraft.waypoints.armedreconingress import (
    ArmedReconIngressBuilder,
)
from game.missiongenerator.aircraft.waypoints.baiingress import BaiIngressBuilder
from game.missiongenerator.aircraft.waypoints.strikeingress import StrikeIngressBuilder
from game.missiongenerator.motorpoolpopulator import MotorpoolPopulator
from game.theater import NavalControlPoint, TheaterGroundObject
from game.theater.controlpoint import ControlPoint
from game.theater.presetlocation import PresetLocation
from game.theater.theatergroundobject import MotorpoolGroundObject
from game.utils import Heading


def _model_group(name: str) -> MagicMock:
    group = MagicMock()
    group.group_name = name
    return group


def _build_builder(target: Any, find_group: Callable[[str], Any]) -> tuple[Any, Any]:
    # Bypass __init__ (it needs a full mission/flight); only add_tasks() and the
    # few collaborators it consults are exercised. Typed as Any so the mocks can
    # stand in for the real, strongly-typed attributes.
    builder: Any = object.__new__(AntiShipIngressBuilder)
    builder.register_special_ingress_points = MagicMock()
    builder.package = MagicMock()
    builder.package.target = target
    builder.flight = MagicMock()
    builder.mission = MagicMock()
    builder.mission.find_group.side_effect = find_group
    waypoint = MagicMock()
    waypoint.tasks = []
    return builder, waypoint


def test_naval_control_point_targets_main_tgo_not_first_ground_object() -> None:
    """Regression test: the carrier group must come from find_main_tgo().

    A NavalControlPoint can own several ground objects; ground_objects[0] is
    not necessarily the carrier (it may be a sunk group that never spawns).
    The attack task must target the group the flight plan routes to.
    """
    carrier_group = _model_group("carrier-group")
    main_tgo = MagicMock()
    main_tgo.groups = [carrier_group]

    wrong_group = _model_group("wrong-group")
    wrong_tgo = MagicMock()
    wrong_tgo.groups = [wrong_group]

    target = MagicMock(spec=NavalControlPoint)
    target.find_main_tgo.return_value = main_tgo
    target.ground_objects = [wrong_tgo]  # ground_objects[0] is the wrong group

    miz_group = MagicMock()
    miz_group.id = 42

    def find_group(name: str) -> Any:
        return miz_group if name == "carrier-group" else None

    builder, waypoint = _build_builder(target, find_group)
    builder.add_tasks(waypoint)

    queried = [call.args[0] for call in builder.mission.find_group.call_args_list]
    assert "carrier-group" in queried
    assert "wrong-group" not in queried

    attacks = [task for task in waypoint.tasks if isinstance(task, AttackGroup)]
    assert attacks, "expected at least one AttackGroup task"
    assert all(task.params["groupId"] == 42 for task in attacks)


def test_warns_when_no_attackable_group(caplog: pytest.LogCaptureFixture) -> None:
    """A target whose groups are not in the mission yields a clear warning."""
    group = _model_group("missing-group")
    target = MagicMock(spec=TheaterGroundObject)
    target.groups = [group]

    builder, waypoint = _build_builder(target, lambda name: None)

    with caplog.at_level(logging.WARNING):
        builder.add_tasks(waypoint)

    assert not [t for t in waypoint.tasks if isinstance(t, AttackGroup)]
    assert any("no attackable target group" in rec.message for rec in caplog.records)


def _motorpool_target(unit_positions: list[Point]) -> MotorpoolGroundObject:
    control_point = MagicMock(spec=ControlPoint)
    location = PresetLocation(
        "Garage", Point(0.0, 0.0, MagicMock(spec=Terrain)), Heading.from_degrees(0.0)
    )
    target = MotorpoolGroundObject(
        "Motorpool", location, control_point, GroupTask.MOTORPOOL
    )
    target.groups = cast(
        Any,
        [
            SimpleNamespace(
                units=[SimpleNamespace(position=p, alive=True) for p in unit_positions]
            )
        ],
    )
    return target


def _motorpool_group(name: str, positions: list[Point]) -> Any:
    """A fake TheaterGroup as the populator renders them: one group per unit
    type, named "{tgo.name} ({unit_type})"."""
    return SimpleNamespace(
        id=len(name),
        group_name=name,
        units=[SimpleNamespace(position=p, alive=True) for p in positions],
    )


def _motorpool_ingress_builder(
    builder_type: type[Any], target: MotorpoolGroundObject
) -> tuple[Any, MovingPoint]:
    builder: Any = object.__new__(builder_type)
    builder.package = SimpleNamespace(target=target)
    builder.flight = SimpleNamespace(
        is_helo=False,
        client_count=0,
        coalition=SimpleNamespace(
            game=SimpleNamespace(
                settings=SimpleNamespace(armed_recon_engagement_range_distance=5)
            )
        ),
        package=SimpleNamespace(target=target),
        flight_plan=SimpleNamespace(
            # Deliberately distinct from the garage position so tests can tell
            # whether a zone is centered on the TGO or on the ToT waypoint.
            tot_waypoint=SimpleNamespace(
                position=Point(500.0, 500.0, MagicMock(spec=Terrain))
            )
        ),
    )
    builder.register_special_ingress_points = MagicMock()
    builder.mission = MagicMock()
    waypoint = MovingPoint(target.position)
    return builder, waypoint


def _populated_motorpool(armor: dict[GroundUnitType, int]) -> MotorpoolGroundObject:
    """Run a real MotorpoolPopulator pass over a fresh motorpool TGO."""
    target = _motorpool_target([])
    control_point = target.control_point
    control_point.base = cast(Any, SimpleNamespace(armor=armor))
    control_point.connected_points = []
    cast(Any, control_point).ground_objects = [target]

    unit_ids = iter(range(1, 1000))
    group_ids = iter(range(1, 1000))
    game = SimpleNamespace(
        theater=SimpleNamespace(controlpoints=[control_point]),
        settings=SimpleNamespace(motorpool_enabled=True, motorpool_spawn_cap=10),
        next_unit_id=lambda: next(unit_ids),
        next_group_id=lambda: next(group_ids),
    )
    MotorpoolPopulator(cast(Any, game)).populate()
    return target


def _strike_ingress_builder(
    target: MotorpoolGroundObject,
) -> tuple[Any, MovingPoint]:
    builder: Any = object.__new__(StrikeIngressBuilder)
    builder.group = SimpleNamespace(
        units=[SimpleNamespace(unit_type=A_10C)], task="Ground Attack"
    )
    builder.waypoint = SimpleNamespace(targets=[])
    builder.package = SimpleNamespace(target=target)
    builder.flight = SimpleNamespace(
        flight_type=FlightType.STRIKE,
        client_count=0,
        unit_type=SimpleNamespace(dcs_unit_type=A_10C),
    )
    builder.register_special_ingress_points = MagicMock()
    waypoint = MovingPoint(target.position)
    return builder, waypoint


def test_strike_motorpool_bombing_tasks_are_one_per_unit() -> None:
    """Spec: motorpool STRIKE gets one AI bombing task per parked unit at the
    ingress waypoint, each aimed at that unit's position — not a single
    centroid/carpet task over the whole park."""
    unit_type = next(GroundUnitType.for_dcs_type(Armor.M_1_Abrams))
    target = _populated_motorpool({unit_type: 3})
    unit_positions = {
        (unit.position.x, unit.position.y)
        for group in target.groups
        for unit in group.units
    }
    assert len(unit_positions) == 3

    builder, waypoint = _strike_ingress_builder(target)

    cast(Any, builder).add_tasks(waypoint)

    bombing = [
        task
        for task in waypoint.tasks
        if isinstance(task, Bombing)
        and task.params["weaponType"] == WeaponType.Bombs.value
    ]
    assert len(bombing) == len(unit_positions)
    assert {(task.params["x"], task.params["y"]) for task in bombing} == (
        unit_positions
    )


def test_strike_motorpool_empty_reserve_adds_no_bombing_tasks() -> None:
    """Spec: an empty motorpool reserve adds nothing — no bombing tasks at the
    ingress waypoint."""
    target = _populated_motorpool({})
    assert not [unit for group in target.groups for unit in group.units]

    builder, waypoint = _strike_ingress_builder(target)

    cast(Any, builder).add_tasks(waypoint)

    assert not [
        task for task in waypoint.tasks if isinstance(task, (Bombing, CarpetBombing))
    ]


def test_bai_motorpool_engages_each_unit_type_group() -> None:
    """Spec: motorpool BAI gets one AttackGroup task per unit-type group at the
    ingress waypoint — the populator builds one group per unit type, named
    "{tgo.name} ({unit_type})" — matching the shape of non-motorpool BAI group
    engagement. The old single EngageTargetsInZone task is gone."""
    target = _motorpool_target([])
    target.groups = [
        _motorpool_group(
            "Motorpool (M-1 Abrams)", [Point(3.0, 4.0, MagicMock(spec=Terrain))]
        ),
        _motorpool_group(
            "Motorpool (T-90)", [Point(0.0, 10.0, MagicMock(spec=Terrain))]
        ),
    ]
    builder, waypoint = _motorpool_ingress_builder(BaiIngressBuilder, target)
    miz_groups = {
        "Motorpool (M-1 Abrams)": SimpleNamespace(id=11),
        "Motorpool (T-90)": SimpleNamespace(id=22),
    }
    builder.mission.find_group.side_effect = lambda name: miz_groups[name]

    cast(Any, builder).add_tasks(waypoint)

    attacks = [task for task in waypoint.tasks if isinstance(task, AttackGroup)]
    assert sorted(task.params["groupId"] for task in attacks) == [11, 22]
    assert not [
        task for task in waypoint.tasks if isinstance(task, EngageTargetsInZone)
    ]


# Spec: the armed-recon motorpool zone reaches the furthest slot of a FULL 5x5
# parked grid — 4 rows behind the garage (45.72 m + 3 more rows at 12 m
# spacing) and 4 columns (12 m spacing) beside it — plus a 20 m (60 ft) buffer.
# The radius is stable regardless of how many units are rendered and is never
# taken from the configured engagement range.
_FULL_GRID_RADIUS_M = math.ceil(math.hypot(45.72 + 4 * 12.0, 4 * 12.0) + 20)


def _motorpool_zone_task(waypoint: MovingPoint) -> Any:
    return next(
        task
        for task in waypoint.tasks
        if isinstance(task, ControlledTask)
        and task.params["task"]["id"] == "EngageTargetsInZone"
    )


def test_armed_recon_motorpool_zone_is_garage_centered_full_grid() -> None:
    """Spec: the zone is centered on the garage (the TGO position, not the ToT
    waypoint) and sized to a FULL 5x5 grid plus 20 m. The fixture's configured
    engagement range is 5 NM (~9260 m) and must never size this zone."""
    target = _motorpool_target(
        [
            Point(6.0, 8.0, MagicMock(spec=Terrain)),
            Point(0.0, 10.0, MagicMock(spec=Terrain)),
        ]
    )
    builder, waypoint = _motorpool_ingress_builder(ArmedReconIngressBuilder, target)

    cast(Any, builder).add_tasks(waypoint)

    params = _motorpool_zone_task(waypoint).params["task"]["params"]
    assert params["zoneRadius"] == _FULL_GRID_RADIUS_M
    assert (params["x"], params["y"]) == (target.position.x, target.position.y)


def test_armed_recon_motorpool_radius_is_stable_when_empty() -> None:
    """Spec: 'full 5x5 grid' means the radius does not depend on how many
    vehicles are currently rendered — an empty motorpool gets the same
    garage-centered zone as a full one (the old behavior was a zero radius)."""
    target = _motorpool_target([])
    builder, waypoint = _motorpool_ingress_builder(ArmedReconIngressBuilder, target)

    cast(Any, builder).add_tasks(waypoint)

    params = _motorpool_zone_task(waypoint).params["task"]["params"]
    assert params["zoneRadius"] == _FULL_GRID_RADIUS_M
    assert (params["x"], params["y"]) == (target.position.x, target.position.y)
