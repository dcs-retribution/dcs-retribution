from __future__ import annotations

from types import SimpleNamespace
from typing import cast
from unittest.mock import MagicMock

from dcs.mapping import Point
from dcs.statics import Fortification
from dcs.task import OptAlarmState, OptROE

from game.missiongenerator.motorpoolgenerator import (
    MotorpoolGenerator,
    _DEPOT_OFFSET_M,
)
from game.utils import Heading


def _generator() -> MotorpoolGenerator:
    gen = MotorpoolGenerator.__new__(MotorpoolGenerator)
    gen.game = SimpleNamespace(settings=SimpleNamespace(perf_red_alert_state=True))  # type: ignore[assignment]
    gen.unit_map = MagicMock()
    return gen


def _group_with_tasks() -> SimpleNamespace:
    point = SimpleNamespace(tasks=[])
    return SimpleNamespace(points=[point], units=[])


def test_alarm_state_is_always_green_even_when_red_alert_setting_on() -> None:
    gen = _generator()
    group = _group_with_tasks()
    gen.set_alarm_state(group)  # type: ignore[arg-type]
    assert group.points[0].tasks == [OptAlarmState(1)]


def test_register_theater_unit_is_a_noop() -> None:
    gen = _generator()
    gen._register_theater_unit(MagicMock(), MagicMock())
    gen.unit_map.add_theater_unit_mapping.assert_not_called()  # type: ignore[attr-defined]


def test_passivate_holds_fire_and_disables_driving() -> None:
    gen = _generator()
    u1, u2 = SimpleNamespace(player_can_drive=True), SimpleNamespace(
        player_can_drive=True
    )
    group = SimpleNamespace(points=[SimpleNamespace(tasks=[])], units=[u1, u2])
    gen._passivate(group)  # type: ignore[arg-type]
    assert group.points[0].tasks == [OptROE(OptROE.Values.WeaponHold)]
    assert u1.player_can_drive is False and u2.player_can_drive is False


def _spawn_depot_kwargs(heading: float) -> dict[str, object]:
    gen = _generator()
    gen.m = MagicMock()
    gen.country = object()  # type: ignore[assignment]
    origin = Point(1000.0, 2000.0, MagicMock())
    gen.ground_object = SimpleNamespace(  # type: ignore[assignment]
        name="Kutaisi Motorpool 0",
        position=origin,
        heading=Heading.from_degrees(heading),
    )
    gen._spawn_depot()
    gen.m.static_group.assert_called_once()
    gen.unit_map.add_motorpool_units.assert_not_called()  # type: ignore[attr-defined]
    return dict(gen.m.static_group.call_args.kwargs)


def test_spawn_depot_emits_unregistered_garage_static() -> None:
    # North-facing (heading 0): depot sits at the world-axis -x/-y corner, clear of
    # the vehicle grid (which starts on tgo.position) so it never collides with a
    # parked reserve unit. Also a regression guard for the un-rotated layout.
    kwargs = _spawn_depot_kwargs(0.0)
    assert kwargs["_type"] is Fortification.Garage_A
    assert cast(Point, kwargs["position"]).x == 1000.0 - _DEPOT_OFFSET_M
    assert cast(Point, kwargs["position"]).y == 2000.0 - _DEPOT_OFFSET_M


def test_spawn_depot_offset_rotates_with_garage_heading() -> None:
    # Starfire concern: the garage heading must rotate the whole layout. At heading
    # 90 the -x/-y depot corner rotates clockwise about the origin to +x/-y, staying
    # opposite the (also-rotated) vehicle grid.
    kwargs = _spawn_depot_kwargs(90.0)
    pos = cast(Point, kwargs["position"])
    assert abs(pos.x - (1000.0 + _DEPOT_OFFSET_M)) < 1e-6
    assert abs(pos.y - (2000.0 - _DEPOT_OFFSET_M)) < 1e-6
    # Building still faces the authored heading.
    assert kwargs["heading"] == 90.0
