from __future__ import annotations

from types import SimpleNamespace
from typing import TYPE_CHECKING, cast
from unittest.mock import MagicMock

from dcs.mapping import Point
from dcs.terrain import Terrain
from dcs.vehicles import Armor

from game.ato.flighttype import FlightType
from game.commander.objectivefinder import ObjectiveFinder
from game.commander.tasks.compound.attackmotorpools import AttackMotorpools
from game.commander.tasks.primitive.motorpool import PlanMotorpoolAttack
from game.data.groups import GroupTask
from game.dcs.groundunittype import GroundUnitType
from game.theater.controlpoint import ControlPoint
from game.theater.player import Player
from game.theater.presetlocation import PresetLocation
from game.theater.theatergroundobject import MotorpoolGroundObject
from game.utils import Heading

if TYPE_CHECKING:
    from game.game import Game


def _gut() -> GroundUnitType:
    return next(GroundUnitType.for_dcs_type(Armor.M_1_Abrams))


def _motorpool_cp(
    reserve: dict[GroundUnitType, int], friendly: bool, name: str = "CP"
) -> tuple[MotorpoolGroundObject, ControlPoint]:
    cp = MagicMock(spec=ControlPoint)
    cp.is_friendly = MagicMock(return_value=friendly)
    cp.captured = Player.BLUE if friendly else Player.RED
    cp.base = SimpleNamespace(armor=dict(reserve), total_armor=sum(reserve.values()))
    cp.connected_points = []  # rear CP: reserve == full pool
    cp.name = name
    loc = PresetLocation(
        "G", Point(0.0, 0.0, MagicMock(spec=Terrain)), Heading.from_degrees(0.0)
    )
    tgo = MotorpoolGroundObject(f"{name} Motorpool 0", loc, cp, GroupTask.MOTORPOOL)
    tgo.distance_to = MagicMock(return_value=100.0)  # type: ignore[method-assign]
    cp.ground_objects = [tgo]
    return tgo, cp


def _game(
    controlpoints: list[ControlPoint], cap: int = 10, enabled: bool = True
) -> object:
    return SimpleNamespace(
        theater=SimpleNamespace(controlpoints=controlpoints),
        settings=SimpleNamespace(motorpool_enabled=enabled, motorpool_spawn_cap=cap),
    )


def _friendly_cp() -> ControlPoint:
    cp = MagicMock(spec=ControlPoint)
    cp.is_friendly = MagicMock(return_value=True)
    cp.captured = Player.BLUE
    return cp


# --- ObjectiveFinder.motorpool_targets ---------------------------------------


def test_motorpool_targets_yields_enemy_motorpool_with_reserve() -> None:
    gut = _gut()
    enemy_tgo, enemy_cp = _motorpool_cp({gut: 4}, friendly=False)
    game = _game([enemy_cp, _friendly_cp()])
    targets = list(ObjectiveFinder(cast("Game", game), Player.BLUE).motorpool_targets())
    assert targets == [enemy_tgo]


def test_motorpool_targets_excludes_friendly_motorpools() -> None:
    gut = _gut()
    _friendly_tgo, friendly_cp = _motorpool_cp({gut: 4}, friendly=True)
    game = _game([friendly_cp, _friendly_cp()])
    assert (
        list(ObjectiveFinder(cast("Game", game), Player.BLUE).motorpool_targets()) == []
    )


def test_motorpool_targets_excludes_motorpool_with_no_reserve() -> None:
    gut = _gut()
    _empty_tgo, enemy_cp = _motorpool_cp({gut: 0}, friendly=False)
    game = _game([enemy_cp, _friendly_cp()])
    assert (
        list(ObjectiveFinder(cast("Game", game), Player.BLUE).motorpool_targets()) == []
    )


def test_motorpool_targets_excludes_motorpool_when_disabled() -> None:
    gut = _gut()
    _disabled_tgo, enemy_cp = _motorpool_cp({gut: 4}, friendly=False)
    game = _game([enemy_cp, _friendly_cp()], enabled=False)
    assert (
        list(ObjectiveFinder(cast("Game", game), Player.BLUE).motorpool_targets()) == []
    )


def test_motorpool_targets_sorted_nearest_first() -> None:
    gut = _gut()
    near_tgo, near_cp = _motorpool_cp({gut: 1}, friendly=False, name="Near")
    far_tgo, far_cp = _motorpool_cp({gut: 1}, friendly=False, name="Far")
    near_tgo.distance_to = MagicMock(return_value=10.0)  # type: ignore[method-assign]
    far_tgo.distance_to = MagicMock(return_value=500.0)  # type: ignore[method-assign]
    game = _game([far_cp, near_cp, _friendly_cp()])
    targets = list(ObjectiveFinder(cast("Game", game), Player.BLUE).motorpool_targets())
    assert targets == [near_tgo, far_tgo]


# --- PlanMotorpoolAttack ------------------------------------------------------


def _motorpool_target(reserve_count: int) -> MotorpoolGroundObject:
    gut = _gut()
    tgo, cp = _motorpool_cp({gut: reserve_count}, friendly=False)
    settings = cp.coalition.game.settings
    settings.motorpool_spawn_cap = 10
    settings.motorpool_enabled = True
    settings.autoplan_tankers_for_strike = False
    return tgo


def test_motorpool_bai_proposes_bai_plus_escorts() -> None:
    tgo = _motorpool_target(8)
    task = PlanMotorpoolAttack(tgo, FlightType.BAI)
    task.propose_flights()
    flight_tasks = [f.task for f in task.flights]
    assert FlightType.BAI in flight_tasks
    assert FlightType.STRIKE not in flight_tasks
    assert FlightType.SEAD_ESCORT in flight_tasks
    assert FlightType.ESCORT in flight_tasks
    assert FlightType.SEAD_SWEEP in flight_tasks


def test_motorpool_strike_proposes_strike_plus_escorts() -> None:
    tgo = _motorpool_target(8)
    task = PlanMotorpoolAttack(tgo, FlightType.STRIKE)
    task.propose_flights()
    flight_tasks = [f.task for f in task.flights]
    assert FlightType.STRIKE in flight_tasks
    assert FlightType.BAI not in flight_tasks
    assert FlightType.SEAD_ESCORT in flight_tasks


def test_motorpool_attack_effect_removes_target() -> None:
    tgo = _motorpool_target(4)
    other = _motorpool_target(4)
    state = SimpleNamespace(motorpool_targets=[tgo, other])
    task = PlanMotorpoolAttack(tgo, FlightType.BAI)
    task.package = None  # super().apply_effects is a no-op with no package
    task.apply_effects(state)  # type: ignore[arg-type]
    assert state.motorpool_targets == [other]


def test_motorpool_attack_precondition_fails_when_not_listed() -> None:
    tgo = _motorpool_target(4)
    state = SimpleNamespace(motorpool_targets=[])
    task = PlanMotorpoolAttack(tgo, FlightType.BAI)
    # Target absent: short-circuits before the heavy fulfillment path.
    assert task.preconditions_met(state) is False  # type: ignore[arg-type]


# --- AttackMotorpools ---------------------------------------------------------


def test_attack_motorpools_yields_bai_then_strike_per_motorpool() -> None:
    tgo = _motorpool_target(4)
    state = SimpleNamespace(motorpool_targets=[tgo])
    methods = list(AttackMotorpools().each_valid_method(state))  # type: ignore[arg-type]
    assert len(methods) == 2
    bai = methods[0][0]
    strike = methods[1][0]
    assert isinstance(bai, PlanMotorpoolAttack)
    assert isinstance(strike, PlanMotorpoolAttack)
    assert bai.task is FlightType.BAI
    assert strike.task is FlightType.STRIKE
    assert bai.target is tgo
    assert strike.target is tgo
