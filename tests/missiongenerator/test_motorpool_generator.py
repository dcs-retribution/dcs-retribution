from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

from dcs.task import OptAlarmState, OptROE

from game.missiongenerator.motorpoolgenerator import MotorpoolGenerator


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
