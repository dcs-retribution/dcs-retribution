from __future__ import annotations

import pickle
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import MagicMock, patch

from dcs.mapping import Point
from dcs.terrain import Caucasus, Terrain
from dcs.vehicles import Armor

from game import persistency
from game.dcs.groundunittype import GroundUnitType
from game.migrator import Migrator
from game.theater.controlpoint import ControlPointType
from game.theater.presetlocation import PresetLocation
from game.theater.theatergroundobject import MotorpoolGroundObject
from game.utils import Heading


class _IdAllocator:
    def __init__(self) -> None:
        self.calls = 0

    def __call__(self) -> int:
        self.calls += 1
        return self.calls


class _MigrationControlPoint:
    def __init__(self, name: str, position: Point, armor: dict[object, int]) -> None:
        self.name = name
        self.cptype = ControlPointType.AIRBASE
        self.position = position
        self.connected_objectives: list[object] = []
        self.preset_locations = SimpleNamespace(motorpools=[])
        self.captured = object()
        self.connected_points: list[object] = []
        self.base = SimpleNamespace(armor=armor, total_armor=sum(armor.values()))

    @property
    def ground_objects(self) -> list[object]:
        return list(self.connected_objectives)


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


def test_duplicate_reference_to_same_tgo_is_canonicalized_globally() -> None:
    cp = _MigrationControlPoint("CP", Point(0.0, 0.0, Caucasus()), {})
    other_cp = _MigrationControlPoint("Other", Point(1000.0, 0.0, Caucasus()), {})
    location = _loc()
    cp.preset_locations.motorpools = [location]
    existing = MotorpoolGroundObject("Persisted depot", location, cast(Any, cp), None)
    cp.connected_objectives = [existing]
    other_cp.connected_objectives = [existing]
    migrator = _migrator_with(cp)
    migrator.game.theater.controlpoints.append(cast(Any, other_cp))

    migrator._ensure_motorpool_tgos()

    assert cp.connected_objectives == [existing]
    assert other_cp.connected_objectives == []


def test_removed_authored_marker_discards_persisted_tgo() -> None:
    cp = _MigrationControlPoint("CP", Point(0.0, 0.0, Caucasus()), {})
    stale = MotorpoolGroundObject("Persisted depot", _loc(), cast(Any, cp), None)
    cp.connected_objectives = [stale]

    _migrator_with(cp)._ensure_motorpool_tgos()

    assert cp.connected_objectives == []


def test_moved_authored_marker_replaces_persisted_identity() -> None:
    cp = _MigrationControlPoint("CP", Point(0.0, 0.0, Caucasus()), {})
    current = PresetLocation(
        "Garage A", Point(1000.0, 0.0, Caucasus()), Heading.from_degrees(90)
    )
    cp.preset_locations.motorpools = [current]
    old = PresetLocation(
        "Garage A", Point(0.0, 0.0, Caucasus()), Heading.from_degrees(0)
    )
    stale = MotorpoolGroundObject("Old codename", old, cast(Any, cp), None)
    cp.connected_objectives = [stale]

    _migrator_with(cp)._ensure_motorpool_tgos()

    pools = [o for o in cp.connected_objectives if isinstance(o, MotorpoolGroundObject)]
    assert len(pools) == 1
    assert pools[0] is not stale
    assert pools[0].original_name == "Garage A"
    assert pools[0].position.x == 1000.0
    assert pools[0].position.y == 0.0
    assert pools[0].heading.degrees == 90


def test_global_marker_reconciliation_finds_tgo_under_another_cp() -> None:
    marker_cp = _MigrationControlPoint("Marker", Point(0.0, 0.0, Caucasus()), {})
    stale_cp = _MigrationControlPoint("Stale", Point(10000.0, 0.0, Caucasus()), {})
    marker = PresetLocation(
        "Garage A", Point(0.0, 0.0, Caucasus()), Heading.from_degrees(0)
    )
    marker_cp.preset_locations.motorpools = [marker]
    stale_tgo = MotorpoolGroundObject("JAGUAR", marker, cast(Any, stale_cp), None)
    stale_cp.connected_objectives.append(cast(Any, stale_tgo))
    migrator = _migrator_with(marker_cp)
    migrator.game.theater.controlpoints.append(cast(Any, stale_cp))

    migrator._ensure_motorpool_tgos()
    from game.missiongenerator.motorpoolpopulator import MotorpoolPopulator

    MotorpoolPopulator(migrator.game)._rehome_motorpools()

    motorpools = [
        tgo
        for cp in (marker_cp, stale_cp)
        for tgo in cp.connected_objectives
        if isinstance(tgo, MotorpoolGroundObject)
    ]
    assert motorpools == [stale_tgo]
    assert stale_tgo.control_point is marker_cp
    assert marker_cp.preset_locations.motorpools == [marker]


def test_migrate_game_rehomes_motorpools_after_all_migrations() -> None:
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
        populator.return_value._rehome_motorpools.side_effect = lambda: events.append(
            "rehome"
        )
        migrator._migrate_game()

    populator.assert_called_once_with(game)
    populator.return_value._rehome_motorpools.assert_called_once_with()
    populator.return_value.populate.assert_not_called()
    assert events[-1] == "rehome"
    assert events.index("rehome") > events.index("_ensure_motorpool_tgos")
    assert events.index("rehome") > events.index("_update_theater")


def test_loaded_migration_rehomes_without_persisting_ephemeral_groups(
    tmp_path: Path,
) -> None:
    unit_type = next(GroundUnitType.for_dcs_type(Armor.M_1_Abrams))
    owner = _MigrationControlPoint(
        "Rear Base", Point(5000.0, 0.0, Caucasus()), {unit_type: 3}
    )
    farp = _MigrationControlPoint(
        "Frontline FARP", Point(0.0, 0.0, Caucasus()), {unit_type: 3}
    )
    farp.cptype = ControlPointType.FARP
    owner.preset_locations.motorpools = [
        PresetLocation(
            "Garage A", Point(0.0, 0.0, Caucasus()), Heading.from_degrees(0)
        ),
        PresetLocation(
            "Garage B", Point(1000.0, 0.0, Caucasus()), Heading.from_degrees(0)
        ),
    ]
    tgo = MotorpoolGroundObject(
        "Motorpool A", owner.preset_locations.motorpools[0], cast("Any", owner), None
    )
    owner.connected_objectives.append(tgo)
    tgo.groups = [cast(Any, object())]
    tgo.motorpool_unit_types = {1: unit_type}
    next_group_id = _IdAllocator()
    next_unit_id = _IdAllocator()
    game = SimpleNamespace(
        theater=SimpleNamespace(controlpoints=[owner, farp]),
        settings=SimpleNamespace(motorpool_enabled=True, motorpool_spawn_cap=10),
        current_group_id=20,
        current_unit_id=10,
        next_group_id=next_group_id,
        next_unit_id=next_unit_id,
    )
    save_path = tmp_path / "campaign.retribution"
    with save_path.open("wb") as save_file:
        pickle.dump(game, save_file)

    persistency.setup(str(tmp_path), False, 0)
    loaded = persistency.load_game(str(save_path))
    assert loaded is not None

    migrator = Migrator.__new__(Migrator)
    migrator.game = loaded
    for method_name in (
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
        "_reload_terrain",
        "_update_theater",
        "_update_campaign_name",
    ):
        setattr(migrator, method_name, MagicMock())
    migrator._migrate_game()

    loaded_motorpools = [
        tgo
        for control_point in loaded.theater.controlpoints
        for tgo in control_point.connected_objectives
        if isinstance(tgo, MotorpoolGroundObject)
    ]
    assert len(loaded_motorpools) == 2
    assert {tgo.original_name for tgo in loaded_motorpools} == {"Garage A", "Garage B"}
    assert all(
        tgo.control_point is loaded.theater.controlpoints[1]
        for tgo in loaded_motorpools
    )
    assert loaded.theater.controlpoints[0].connected_objectives == []
    assert loaded.theater.controlpoints[0].preset_locations.motorpools == [
        PresetLocation(
            "Garage A", Point(0.0, 0.0, Caucasus()), Heading.from_degrees(0)
        ),
        PresetLocation(
            "Garage B", Point(1000.0, 0.0, Caucasus()), Heading.from_degrees(0)
        ),
    ]
    assert all(tgo.groups == [] for tgo in loaded_motorpools)
    assert all(tgo.motorpool_unit_types == {} for tgo in loaded_motorpools)
    assert loaded.current_group_id == 20
    assert loaded.current_unit_id == 10
    loaded_next_group_id = cast(_IdAllocator, loaded.next_group_id)
    loaded_next_unit_id = cast(_IdAllocator, loaded.next_unit_id)
    assert loaded_next_group_id.calls == 0
    assert loaded_next_unit_id.calls == 0

    migrator._migrate_game()

    loaded_motorpools = [
        tgo
        for control_point in loaded.theater.controlpoints
        for tgo in control_point.connected_objectives
        if isinstance(tgo, MotorpoolGroundObject)
    ]
    assert len(loaded_motorpools) == 2
    assert {tgo.original_name for tgo in loaded_motorpools} == {"Garage A", "Garage B"}
    assert all(
        tgo.control_point is loaded.theater.controlpoints[1]
        for tgo in loaded_motorpools
    )
    assert loaded.theater.controlpoints[0].connected_objectives == []

    migrated_save = tmp_path / "migrated.retribution"
    with migrated_save.open("wb") as save_file:
        pickle.dump(loaded, save_file)
    reloaded = persistency.load_game(str(migrated_save))
    assert reloaded is not None
    reloaded_motorpools = [
        tgo
        for tgo in reloaded.theater.controlpoints[1].connected_objectives
        if isinstance(tgo, MotorpoolGroundObject)
    ]
    assert len(reloaded_motorpools) == 2
    assert all(tgo.groups == [] for tgo in reloaded_motorpools)
