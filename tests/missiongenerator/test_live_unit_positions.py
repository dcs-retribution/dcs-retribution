from types import SimpleNamespace
from typing import Any

from game.missiongenerator.missiongenerator import MissionGenerator


def _unit(x: float, y: float) -> Any:
    return SimpleNamespace(position=SimpleNamespace(x=x, y=y))


def _group(units: list[Any], dead: bool = False) -> Any:
    return SimpleNamespace(units=units, dead=dead)


def _mission(vehicle_groups: list[Any], static_groups: list[Any]) -> Any:
    country = SimpleNamespace(vehicle_group=vehicle_groups, static_group=static_groups)
    coalition = SimpleNamespace(countries={"c": country})
    return SimpleNamespace(coalition={"blue": coalition})


def _group_no_dead_attr(units: list[Any]) -> Any:
    # pydcs VehicleGroup has NO 'dead' attribute (only StaticGroup does); the
    # walker must tolerate its absence rather than AttributeError.
    return SimpleNamespace(units=units)


def test_collects_live_units_skips_dead_groups() -> None:
    gen = MissionGenerator.__new__(MissionGenerator)
    gen.mission = _mission(
        vehicle_groups=[
            _group([_unit(1.0, 2.0)]),
            _group([_unit(9.0, 9.0)], dead=True),
        ],
        static_groups=[_group([_unit(3.0, 4.0)])],
    )
    assert sorted(gen._live_unit_positions()) == [(1.0, 2.0), (3.0, 4.0)]


def test_group_without_dead_attr_is_live() -> None:
    # A VehicleGroup lacks a 'dead' attribute entirely -> treated as live.
    gen = MissionGenerator.__new__(MissionGenerator)
    gen.mission = _mission(
        vehicle_groups=[_group_no_dead_attr([_unit(7.0, 8.0)])],
        static_groups=[],
    )
    assert gen._live_unit_positions() == [(7.0, 8.0)]
