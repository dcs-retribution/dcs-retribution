from types import SimpleNamespace
from typing import Any, cast

from dcs.mapping import Point
from dcs.terrain import Caucasus

from game.data.groups import GroupTask
from game.missiongenerator.motorpoolpopulator import MotorpoolPopulator
from game.sim.gameupdateevents import GameUpdateEvents
from game.theater.controlpoint import ControlPointType
from game.theater.presetlocation import PresetLocation
from game.theater.theatergroundobject import MotorpoolGroundObject
from game.utils import Heading


def _land_cp(
    name: str, x: float, y: float, cptype: ControlPointType
) -> SimpleNamespace:
    return SimpleNamespace(
        name=name,
        cptype=cptype,
        position=Point(x, y, Caucasus()),
        connected_objectives=[],
        ground_objects=[],
        preset_locations=SimpleNamespace(motorpools=[]),
    )


def _game(cps: list[Any]) -> Any:
    return SimpleNamespace(
        theater=SimpleNamespace(controlpoints=cps),
        settings=SimpleNamespace(motorpool_enabled=False, motorpool_spawn_cap=0),
    )


def _motorpool_owned_by(owner: Any, x: float, y: float) -> MotorpoolGroundObject:
    loc = PresetLocation("G", Point(x, y, Caucasus()), Heading.from_degrees(0.0))
    owner.preset_locations.motorpools.append(loc)
    tgo = MotorpoolGroundObject("Motorpool 0", loc, owner, GroupTask.MOTORPOOL)
    owner.connected_objectives.append(tgo)
    return tgo


def _rehome(cps: list[Any]) -> None:
    MotorpoolPopulator(cast(Any, _game(cps)))._rehome_motorpools()


def test_rehome_moves_motorpool_to_nearest_farp() -> None:
    base = _land_cp("Countryside AB", 5000.0, 0.0, ControlPointType.AIRBASE)
    farp = _land_cp("Frontline FARP", 0.0, 0.0, ControlPointType.FARP)
    tgo = _motorpool_owned_by(base, 0.0, 0.0)

    _rehome([base, farp])

    assert tgo.control_point is farp
    assert base.connected_objectives == []
    assert farp.connected_objectives == [tgo]


def test_rehome_leaves_motorpool_on_nearest_base() -> None:
    base = _land_cp("Base", 0.0, 0.0, ControlPointType.AIRBASE)
    farp = _land_cp("Far FARP", 5000.0, 0.0, ControlPointType.FARP)
    tgo = _motorpool_owned_by(base, 0.0, 0.0)

    _rehome([base, farp])

    assert tgo.control_point is base
    assert base.connected_objectives == [tgo]
    assert farp.connected_objectives == []


def test_rehome_neutral_fob_claims_adjacent_motorpool() -> None:
    base = _land_cp("Enemy AB", -300000.0, 0.0, ControlPointType.AIRBASE)
    neutral_farp = _land_cp("Neutral FARP", 0.0, 0.0, ControlPointType.FARP)
    tgo = _motorpool_owned_by(base, 0.0, 0.0)

    _rehome([base, neutral_farp])

    # The neutral FOB wins; the motorpool follows its capture state (neutral).
    assert tgo.control_point is neutral_farp


def test_rehome_excludes_naval_control_points() -> None:
    base = _land_cp("AB", 5000.0, 0.0, ControlPointType.AIRBASE)
    carrier = _land_cp("CVN", 0.0, 0.0, ControlPointType.AIRCRAFT_CARRIER_GROUP)
    tgo = _motorpool_owned_by(base, 0.0, 0.0)

    _rehome([base, carrier])

    # Carrier is excluded, so the motorpool stays with the airbase.
    assert tgo.control_point is base


def test_rehome_preserves_motorpool_when_no_eligible_control_point_exists() -> None:
    carrier = _land_cp("CVN", 0.0, 0.0, ControlPointType.AIRCRAFT_CARRIER_GROUP)
    off_map = _land_cp("Off-map", 5000.0, 0.0, ControlPointType.OFF_MAP)
    tgo = _motorpool_owned_by(carrier, 0.0, 0.0)

    _rehome([carrier, off_map])

    assert carrier.connected_objectives == [tgo]
    assert off_map.connected_objectives == []
    assert tgo.control_point is carrier


def test_rehome_without_destination_removes_stale_and_duplicate_references() -> None:
    carrier = _land_cp("CVN", 0.0, 0.0, ControlPointType.AIRCRAFT_CARRIER_GROUP)
    off_map = _land_cp("Off-map", 5000.0, 0.0, ControlPointType.OFF_MAP)
    valid = _motorpool_owned_by(carrier, 0.0, 0.0)
    carrier.connected_objectives.append(valid)
    stale_location = PresetLocation(
        "Removed", Point(1000.0, 0.0, Caucasus()), Heading.from_degrees(0.0)
    )
    stale = MotorpoolGroundObject(
        "Stale depot", stale_location, cast(Any, off_map), GroupTask.MOTORPOOL
    )
    off_map.connected_objectives.append(stale)

    _rehome([carrier, off_map])

    assert carrier.connected_objectives == [valid]
    assert off_map.connected_objectives == []
    assert valid.control_point is carrier


def test_populate_does_not_rehome_existing_motorpools() -> None:
    owner = _land_cp("Owner", 5000.0, 0.0, ControlPointType.AIRBASE)
    nearest = _land_cp("Nearest", 0.0, 0.0, ControlPointType.FARP)
    tgo = _motorpool_owned_by(owner, 0.0, 0.0)

    populator = MotorpoolPopulator(cast(Any, _game([owner, nearest])))
    populator.populate()

    assert tgo.control_point is owner
    assert owner.connected_objectives == [tgo]
    assert nearest.connected_objectives == []


def test_rehome_discards_persisted_motorpool_without_current_marker() -> None:
    owner = _land_cp("Owner", 0.0, 0.0, ControlPointType.AIRBASE)
    stale = _land_cp("Stale", 5000.0, 0.0, ControlPointType.AIRBASE)
    loc = PresetLocation(
        "Removed", Point(0.0, 0.0, Caucasus()), Heading.from_degrees(0.0)
    )
    tgo = MotorpoolGroundObject(
        "Persisted depot", loc, cast(Any, stale), GroupTask.MOTORPOOL
    )
    stale.connected_objectives.append(tgo)

    _rehome([owner, stale])

    assert owner.connected_objectives == []
    assert stale.connected_objectives == []


def test_rehome_deduplicates_current_marker_and_preserves_metadata_and_event() -> None:
    owner = _land_cp("Owner", 5000.0, 0.0, ControlPointType.AIRBASE)
    nearest = _land_cp("Nearest", 0.0, 0.0, ControlPointType.FARP)
    loc = PresetLocation(
        "Authored", Point(0.0, 0.0, Caucasus()), Heading.from_degrees(0.0)
    )
    owner.preset_locations.motorpools = [loc]
    first = MotorpoolGroundObject(
        "First codename", loc, cast(Any, owner), GroupTask.MOTORPOOL
    )
    duplicate = MotorpoolGroundObject(
        "Duplicate codename", loc, cast(Any, owner), GroupTask.MOTORPOOL
    )
    owner.connected_objectives = [first, duplicate]
    events = GameUpdateEvents()

    MotorpoolPopulator(cast(Any, _game([owner, nearest])))._rehome_motorpools(events)

    assert owner.connected_objectives == []
    assert nearest.connected_objectives == [first]
    assert first.control_point is nearest
    assert first.name == "First codename"
    assert duplicate not in nearest.connected_objectives
    assert events.updated_tgos == {first}
