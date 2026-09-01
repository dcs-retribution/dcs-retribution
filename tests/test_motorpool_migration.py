from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from dcs.mapping import Point
from dcs.terrain import Terrain

from game.migrator import Migrator
from game.theater.presetlocation import PresetLocation
from game.theater.theatergroundobject import MotorpoolGroundObject
from game.utils import Heading


def _loc() -> PresetLocation:
    return PresetLocation(
        "G", Point(0.0, 0.0, MagicMock(spec=Terrain)), Heading.from_degrees(0)
    )


def _migrator_with(cp: object, enabled: bool = True) -> Migrator:
    game = SimpleNamespace(
        theater=SimpleNamespace(controlpoints=[cp]),
        settings=SimpleNamespace(motorpool_enabled=enabled),
    )
    m = Migrator.__new__(Migrator)
    m.game = game  # type: ignore[assignment]
    return m


def test_injects_tgo_for_authored_cp_without_one() -> None:
    cp = MagicMock()
    cp.name = "CP"
    cp.preset_locations = SimpleNamespace(motorpools=[_loc()])
    cp.connected_objectives = []
    cp.ground_objects = []
    m = _migrator_with(cp)
    m._ensure_motorpool_tgos()
    assert any(isinstance(o, MotorpoolGroundObject) for o in cp.connected_objectives)


def test_no_injection_without_authored_locations() -> None:
    cp = MagicMock()
    cp.preset_locations = SimpleNamespace(motorpools=[])
    cp.connected_objectives = []
    cp.ground_objects = []
    m = _migrator_with(cp)
    m._ensure_motorpool_tgos()
    assert cp.connected_objectives == []


def test_no_double_injection_when_tgo_exists() -> None:
    cp = MagicMock()
    cp.name = "CP"
    cp.preset_locations = SimpleNamespace(motorpools=[_loc()])
    existing = MotorpoolGroundObject("CP Motorpool 0", _loc(), cp, None)
    cp.connected_objectives = [existing]
    cp.ground_objects = [existing]
    m = _migrator_with(cp)
    m._ensure_motorpool_tgos()
    pools = [o for o in cp.connected_objectives if isinstance(o, MotorpoolGroundObject)]
    assert len(pools) == 1


def test_migrate_game_reconciles_motorpools_after_all_migrations() -> None:
    events: list[str] = []
    game = SimpleNamespace(settings=SimpleNamespace())
    migrator = Migrator.__new__(Migrator)
    migrator.game = game  # type: ignore[assignment]
    method_names = [
        "_update_doctrine",
        "_update_control_points",
        "_update_packagewaypoints",
        "_update_package_attributes",
        "_update_factions",
        "_update_flights",
        "_update_squadrons",
        "_update_transfers",
        "_release_untasked_flights",
        "_update_weather",
        "_update_tgos",
        "_ensure_motorpool_tgos",
        "_reload_terrain",
        "_update_theater",
        "_update_campaign_name",
    ]
    for method_name in method_names:
        setattr(
            migrator,
            method_name,
            MagicMock(side_effect=lambda n=method_name: events.append(n)),
        )

    with patch(
        "game.missiongenerator.motorpoolpopulator.MotorpoolPopulator"
    ) as populator:
        populator.return_value.populate.side_effect = lambda: events.append("populate")
        migrator._migrate_game()

    populator.assert_called_once_with(game)
    populator.return_value.populate.assert_called_once_with()
    assert events[-1] == "populate"
    assert events.index("populate") > events.index("_ensure_motorpool_tgos")
    assert events.index("populate") > events.index("_update_theater")
