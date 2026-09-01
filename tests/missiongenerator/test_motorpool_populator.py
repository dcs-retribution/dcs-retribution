from __future__ import annotations

from dataclasses import replace
from itertools import permutations
import pickle
from types import SimpleNamespace
from typing import Any, TYPE_CHECKING, cast
from unittest.mock import MagicMock

from dcs.mapping import Point
from dcs.terrain import Terrain
from dcs.terrain.caucasus import Caucasus
from dcs.vehicles import Armor

from game.dcs.groundunittype import GroundUnitType
from game.missiongenerator.motorpoolpopulator import MotorpoolPopulator, _select_capped
from game.theater.controlpoint import ControlPoint
from game.theater.presetlocation import PresetLocation
from game.theater.theatergroundobject import MotorpoolGroundObject
from game.utils import Heading

if TYPE_CHECKING:
    from game.game import Game


def _gut() -> GroundUnitType:
    return next(GroundUnitType.for_dcs_type(Armor.M_1_Abrams))


def _motorpool(
    reserve: dict[GroundUnitType, int],
    heading: float = 0.0,
) -> tuple[MotorpoolGroundObject, ControlPoint]:
    cp = MagicMock(spec=ControlPoint)
    cp.captured = object()
    cp.base = SimpleNamespace(armor=dict(reserve), total_armor=sum(reserve.values()))
    cp.connected_points = []  # rear CP -> reserve == full pool
    cp.name = "CP"
    loc = PresetLocation(
        "G", Point(0.0, 0.0, MagicMock(spec=Terrain)), Heading.from_degrees(heading)
    )
    from game.data.groups import GroupTask

    tgo = MotorpoolGroundObject("CP Motorpool 0", loc, cp, GroupTask.MOTORPOOL)
    cp.ground_objects = [tgo]
    return tgo, cp


def _game(cps: list[ControlPoint], cap: int, enabled: bool = True) -> Any:
    counter = {"u": 0, "g": 0}

    def next_unit_id() -> int:
        counter["u"] += 1
        return counter["u"]

    def next_group_id() -> int:
        counter["g"] += 1
        return counter["g"]

    return SimpleNamespace(
        theater=SimpleNamespace(controlpoints=cps),
        settings=SimpleNamespace(motorpool_enabled=enabled, motorpool_spawn_cap=cap),
        next_unit_id=next_unit_id,
        next_group_id=next_group_id,
        motorpool_id_counts=counter,
    )


def test_populate_renders_all_when_under_cap() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 4})
    MotorpoolPopulator(cast("Game", _game([cp], cap=10))).populate()
    rendered = sum(len(g.units) for g in tgo.groups)
    assert rendered == 4
    assert tgo.motorpool_unit_types[tgo.groups[0].id] is gut


def test_populate_caps_total() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 25})
    MotorpoolPopulator(cast("Game", _game([cp], cap=10))).populate()
    assert sum(len(g.units) for g in tgo.groups) == 10


def test_select_capped_uses_stable_allocation_behavior() -> None:
    alpha = MagicMock(spec=GroundUnitType)
    alpha.variant_id = "Alpha"
    bravo = MagicMock(spec=GroundUnitType)
    bravo.variant_id = "Bravo"
    charlie = MagicMock(spec=GroundUnitType)
    charlie.variant_id = "Charlie"
    expected = {alpha: 1, bravo: 1}

    for order in permutations(((charlie, 1), (alpha, 1), (bravo, 1))):
        assert _select_capped(dict(order), 2) == expected


def test_motorpool_unit_ids_share_campaign_allocator_with_other_tgos() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 2})
    game = _game([cp], cap=10)
    first_id = game.next_unit_id()

    MotorpoolPopulator(cast("Game", game)).populate()

    ids = [unit.id for group in tgo.groups for unit in group.units]
    assert first_id not in ids
    assert ids == [first_id + 1, first_id + 2]


def test_populate_empty_when_no_reserve() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 0})
    MotorpoolPopulator(cast("Game", _game([cp], cap=10))).populate()
    assert tgo.groups == []


def test_populate_disabled_renders_nothing() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 5})
    MotorpoolPopulator(cast("Game", _game([cp], cap=10, enabled=False))).populate()
    assert tgo.groups == []


def test_populate_is_idempotent_across_runs() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 3})
    pop = MotorpoolPopulator(cast("Game", _game([cp], cap=10)))
    pop.populate()
    pop.populate()
    assert sum(len(g.units) for g in tgo.groups) == 3  # reset each run, not 6


def _unit_positions(tgo: MotorpoolGroundObject) -> list[Point]:
    return [u.position for g in tgo.groups for u in g.units]


def test_grid_spawns_behind_north_facing_garage() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 3}, heading=0.0)
    MotorpoolPopulator(cast("Game", _game([cp], cap=10))).populate()
    positions = _unit_positions(tgo)
    assert len(positions) == 3
    # DCS x is north/south in this project: a north-facing garage's parking
    # grid must be south of the authored Garage_A marker.
    assert abs(positions[0].x + 45.72) < 1e-6 and abs(positions[0].y) < 1e-6
    assert abs(positions[1].x + 45.72) < 1e-6 and abs(positions[1].y - 12.0) < 1e-6
    assert abs(positions[2].x + 45.72) < 1e-6 and abs(positions[2].y - 24.0) < 1e-6


def test_grid_offset_and_spacing_rotate_with_garage_heading() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 3}, heading=90.0)
    MotorpoolPopulator(cast("Game", _game([cp], cap=10))).populate()
    positions = _unit_positions(tgo)
    assert len(positions) == 3
    # An east-facing garage has its parking row west of the marker, with the
    # vehicles laid out from north to south along the garage's right-hand side.
    assert abs(positions[0].x) < 1e-6 and abs(positions[0].y + 45.72) < 1e-6
    assert abs(positions[1].x + 12.0) < 1e-6 and abs(positions[1].y + 45.72) < 1e-6
    assert abs(positions[2].x + 24.0) < 1e-6 and abs(positions[2].y + 45.72) < 1e-6


def _two_motorpools(
    reserve: dict[GroundUnitType, int],
) -> tuple[MotorpoolGroundObject, MotorpoolGroundObject, ControlPoint]:
    from game.data.groups import GroupTask

    cp = MagicMock(spec=ControlPoint)
    cp.captured = object()
    cp.base = SimpleNamespace(armor=dict(reserve), total_armor=sum(reserve.values()))
    cp.connected_points = []
    cp.name = "CP"

    def location(x: float) -> PresetLocation:
        return PresetLocation(
            "G",
            Point(x, 0.0, MagicMock(spec=Terrain)),
            Heading.from_degrees(0),
        )

    first = MotorpoolGroundObject(
        "CP Motorpool 0", location(0.0), cp, GroupTask.MOTORPOOL
    )
    second = MotorpoolGroundObject(
        "CP Motorpool 1", location(100.0), cp, GroupTask.MOTORPOOL
    )
    cp.ground_objects = [first, second]
    return first, second, cp


def _units(tgo: MotorpoolGroundObject) -> list[Any]:
    return [unit for group in tgo.groups for unit in group.units]


def test_multiple_motorpools_share_one_capped_projection() -> None:
    gut = _gut()
    first, second, cp = _two_motorpools({gut: 20})

    MotorpoolPopulator(cast("Game", _game([cp], cap=5))).populate()

    assert len(_units(first)) == 3
    assert len(_units(second)) == 2
    keys = [
        key for tgo in (first, second) for key in tgo.motorpool_projection_keys.values()
    ]
    assert keys == [
        (first.id, gut.variant_id, 0),
        (first.id, gut.variant_id, 1),
        (first.id, gut.variant_id, 2),
        (second.id, gut.variant_id, 0),
        (second.id, gut.variant_id, 1),
    ]


def test_reconcile_unchanged_preserves_ids_and_allocator_counts() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 3})
    game = _game([cp], cap=10)
    populator = MotorpoolPopulator(cast("Game", game))
    populator.populate()
    original_group = tgo.groups[0]
    original_units = list(original_group.units)
    original_positions = [unit.position for unit in original_units]
    allocator_counts = dict(game.motorpool_id_counts)

    populator.populate()

    assert tgo.groups[0] is original_group
    assert tgo.groups[0].units == original_units
    assert all(
        current is original
        for current, original in zip(tgo.groups[0].units, original_units)
    )
    assert [unit.position for unit in tgo.groups[0].units] == original_positions
    assert game.motorpool_id_counts == allocator_counts


def test_mixed_type_growth_uses_unoccupied_grid_slot() -> None:
    abrams = _gut()
    bradley = next(GroundUnitType.for_dcs_type(Armor.M_2_Bradley))
    earlier, later = sorted(
        (abrams, bradley), key=lambda unit_type: unit_type.variant_id
    )
    tgo, cp = _motorpool({earlier: 1, later: 1})
    game = _game([cp], cap=10)
    populator = MotorpoolPopulator(cast("Game", game))
    populator.populate()
    original_by_key = {
        tgo.motorpool_projection_keys[unit.id]: unit for unit in _units(tgo)
    }
    original_ids = {key: unit.id for key, unit in original_by_key.items()}
    original_positions = {key: unit.position for key, unit in original_by_key.items()}
    allocator_counts = dict(game.motorpool_id_counts)

    cp.base.armor[earlier] = 2
    populator.populate()

    current_by_key = {
        tgo.motorpool_projection_keys[unit.id]: unit for unit in _units(tgo)
    }
    for key, original in original_by_key.items():
        assert current_by_key[key] is original
        assert current_by_key[key].id == original_ids[key]
        assert current_by_key[key].position is original_positions[key]
    positions = [(unit.position.x, unit.position.y) for unit in current_by_key.values()]
    assert len(set(positions)) == len(positions)
    added = current_by_key[(tgo.id, earlier.variant_id, 1)]
    expected_position = MotorpoolPopulator._grid_position(tgo, 2)
    assert (added.position.x, added.position.y) == (
        expected_position.x,
        expected_position.y,
    )
    assert added.id not in original_ids.values()
    assert game.motorpool_id_counts == {
        "u": allocator_counts["u"] + 1,
        "g": allocator_counts["g"],
    }


def test_reconcile_after_pickle_preserves_matching_ids() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 3})
    game = _game([cp], cap=10)
    MotorpoolPopulator(cast("Game", game)).populate()
    original_group_id = tgo.groups[0].id
    original_unit_ids = [unit.id for unit in tgo.groups[0].units]

    terrain = Caucasus()
    tgo.position._terrain = terrain
    for group in tgo.groups:
        group.position._terrain = terrain
        for unit in group.units:
            unit.position._terrain = terrain
    tgo.control_point = None  # type: ignore[assignment]
    restored = pickle.loads(pickle.dumps(tgo))
    restored.control_point = cp
    for group in restored.groups:
        group.ground_object = restored
        for unit in group.units:
            unit.ground_object = restored
    cp.__dict__["ground_objects"] = [restored]

    MotorpoolPopulator(cast("Game", game)).populate()

    assert restored.groups[0].id == original_group_id
    assert [unit.id for unit in restored.groups[0].units] == original_unit_ids


def test_changed_projection_rewrites_only_affected_motorpool_slice() -> None:
    gut = _gut()
    first, second, cp = _two_motorpools({gut: 4})
    game = _game([cp], cap=10)
    populator = MotorpoolPopulator(cast("Game", game))
    populator.populate()
    first_group = first.groups[0]
    first_units = list(first_group.units)
    second_group = second.groups[0]
    second_units = list(second_group.units)
    counts_after_initial = dict(game.motorpool_id_counts)

    cp.base.armor[gut] = 3
    populator.populate()

    assert first.groups[0] is first_group
    assert first.groups[0].units == first_units
    assert second.groups[0] is second_group
    assert second.groups[0].units == second_units[:1]
    assert game.motorpool_id_counts == counts_after_initial

    cp.base.armor[gut] = 5
    populator.populate()

    assert first.groups[0] is first_group
    assert first.groups[0].units[:2] == first_units
    assert second.groups[0] is second_group
    assert second.groups[0].units[:1] == second_units[:1]
    assert game.motorpool_id_counts == {
        "u": counts_after_initial["u"] + 2,
        "g": counts_after_initial["g"],
    }


def test_legacy_groups_are_backfilled_and_matching_ids_survive() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 3})
    game = _game([cp], cap=10)
    populator = MotorpoolPopulator(cast("Game", game))
    populator.populate()
    original_group = tgo.groups[0]
    original_units = list(original_group.units)
    del tgo.motorpool_projection_keys
    allocator_counts = dict(game.motorpool_id_counts)

    populator.populate()

    assert tgo.groups[0] is original_group
    assert tgo.groups[0].units == original_units
    assert tgo.motorpool_projection_keys == {
        unit.id: (tgo.id, gut.variant_id, ordinal)
        for ordinal, unit in enumerate(original_units)
    }
    assert game.motorpool_id_counts == allocator_counts


def test_type_replacement_uses_variant_order_and_allocates_only_new_ids() -> None:
    abrams = _gut()
    bradley = next(GroundUnitType.for_dcs_type(Armor.M_2_Bradley))
    first, second, cp = _two_motorpools({bradley: 2, abrams: 2})
    game = _game([cp], cap=10)
    populator = MotorpoolPopulator(cast("Game", game))

    populator.populate()

    ordered_types = sorted(
        (abrams, bradley), key=lambda unit_type: unit_type.variant_id
    )
    assert [
        first.motorpool_unit_types[group.id] for group in first.groups
    ] == ordered_types
    original_ids = {unit.id for tgo in (first, second) for unit in _units(tgo)}
    allocator_counts = dict(game.motorpool_id_counts)

    cp.base.armor = {bradley: 2}
    populator.populate()

    remaining_ids = {unit.id for tgo in (first, second) for unit in _units(tgo)}
    assert remaining_ids < original_ids
    assert game.motorpool_id_counts == allocator_counts

    cp.base.armor = {abrams: 2}
    populator.populate()

    replacement_ids = {unit.id for tgo in (first, second) for unit in _units(tgo)}
    assert replacement_ids.isdisjoint(remaining_ids)
    assert game.motorpool_id_counts == {
        "u": allocator_counts["u"] + 2,
        "g": allocator_counts["g"] + 2,
    }


def test_partial_legacy_metadata_backfills_after_existing_ordinals() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 3})
    populator = MotorpoolPopulator(cast("Game", _game([cp], cap=10)))
    populator.populate()
    units = list(tgo.groups[0].units)
    tgo.motorpool_projection_keys = {
        units[0].id: (tgo.id, gut.variant_id, 0),
    }

    populator.populate()

    assert tgo.motorpool_projection_keys == {
        unit.id: (tgo.id, gut.variant_id, ordinal) for ordinal, unit in enumerate(units)
    }


def test_partial_legacy_metadata_on_later_unit_preserves_all_units() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 3})
    game = _game([cp], cap=10)
    populator = MotorpoolPopulator(cast("Game", game))
    populator.populate()
    group = tgo.groups[0]
    units = list(group.units)
    unit_ids = {unit.id for unit in units}
    allocator_counts = dict(game.motorpool_id_counts)
    tgo.motorpool_projection_keys = {
        units[-1].id: (tgo.id, gut.variant_id, 0),
    }

    populator.populate()

    assert len(set(tgo.motorpool_projection_keys.values())) == len(units)
    assert tgo.motorpool_projection_keys == {
        units[-1].id: (tgo.id, gut.variant_id, 0),
        units[0].id: (tgo.id, gut.variant_id, 1),
        units[1].id: (tgo.id, gut.variant_id, 2),
    }
    assert tgo.groups[0] is group
    assert [unit.id for unit in tgo.groups[0].units] == [unit.id for unit in units]
    assert {unit.id for unit in tgo.groups[0].units} == unit_ids
    assert all(
        current is original for current, original in zip(tgo.groups[0].units, units)
    )
    assert game.motorpool_id_counts == allocator_counts


def test_duplicate_persisted_keys_retain_first_authored_unit() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 3})
    game = _game([cp], cap=10)
    populator = MotorpoolPopulator(cast("Game", game))
    populator.populate()
    group = tgo.groups[0]
    units = list(group.units)
    allocator_counts = dict(game.motorpool_id_counts)
    duplicate_key = (tgo.id, gut.variant_id, 0)
    tgo.motorpool_projection_keys = {
        units[0].id: duplicate_key,
        units[1].id: duplicate_key,
    }

    populator.populate()

    assert tgo.motorpool_projection_keys == {
        unit.id: (tgo.id, gut.variant_id, ordinal) for ordinal, unit in enumerate(units)
    }
    assert tgo.groups[0] is group
    assert all(current is original for current, original in zip(group.units, units))
    assert game.motorpool_id_counts == allocator_counts


def test_dead_persisted_unit_is_replaced_for_matching_projection_key() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 1})
    game = _game([cp], cap=10)
    populator = MotorpoolPopulator(cast("Game", game))
    populator.populate()
    dead_unit = tgo.groups[0].units[0]
    dead_unit.alive = False
    allocator_counts = dict(game.motorpool_id_counts)

    populator.populate()

    live_units = _units(tgo)
    assert len(live_units) == 1
    assert live_units[0].alive
    assert live_units[0].id != dead_unit.id
    assert game.motorpool_id_counts["u"] == allocator_counts["u"] + 1


def test_unchanged_live_projection_removes_extra_dead_cached_unit() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 1})
    game = _game([cp], cap=10)
    populator = MotorpoolPopulator(cast("Game", game))
    populator.populate()
    group = tgo.groups[0]
    live_unit = group.units[0]
    dead_unit = replace(live_unit, id=game.next_unit_id(), alive=False)
    group.units = [live_unit, dead_unit]
    tgo.motorpool_projection_keys[dead_unit.id] = (tgo.id, gut.variant_id, 1)

    populator.populate()

    assert tgo.groups[0] is group
    assert tgo.groups[0].units == [live_unit]
    assert tgo.groups[0].units[0] is live_unit
    assert tgo.motorpool_projection_keys == {
        live_unit.id: (tgo.id, gut.variant_id, 0),
    }


def test_all_dead_cached_units_are_removed_when_desired_projection_is_empty() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 1})
    game = _game([cp], cap=10)
    populator = MotorpoolPopulator(cast("Game", game))
    populator.populate()
    tgo.groups[0].units[0].alive = False
    cp.base.armor[gut] = 0

    populator.populate()

    assert tgo.groups == []
    assert tgo.motorpool_unit_types == {}
    assert tgo.motorpool_projection_keys == {}


def test_disabled_or_zero_cap_reconciliation_empties_every_motorpool() -> None:
    gut = _gut()
    first, second, cp = _two_motorpools({gut: 4})
    game = _game([cp], cap=10)
    populator = MotorpoolPopulator(cast("Game", game))
    populator.populate()

    game.settings.motorpool_enabled = False
    populator.populate()

    for tgo in (first, second):
        assert tgo.groups == []
        assert tgo.motorpool_unit_types == {}
        assert tgo.motorpool_projection_keys == {}

    game.settings.motorpool_enabled = True
    game.settings.motorpool_spawn_cap = 0
    populator.populate()
    assert first.groups == []
    assert second.groups == []


def test_cached_motorpool_plan_survives_unchanged_reconciliation() -> None:
    from game.ato.flightplans.formationattack import FormationAttackLayout
    from game.ato.flightplans.strike import StrikeFlightPlan
    from game.ato.flightwaypoint import FlightWaypoint
    from game.ato.flightwaypointtype import FlightWaypointType

    gut = _gut()
    tgo, cp = _motorpool({gut: 2})
    populator = MotorpoolPopulator(cast("Game", _game([cp], cap=10)))
    populator.populate()

    # Cache a real flight plan whose ingress waypoint retains the materialized
    # motorpool targets used by mission generation.
    waypoint = FlightWaypoint("WP", FlightWaypointType.NAV, tgo.position)
    ingress = FlightWaypoint(
        "INGRESS",
        FlightWaypointType.INGRESS_STRIKE,
        tgo.position,
        targets=list(tgo.strike_targets),
    )
    layout = FormationAttackLayout(
        departure=waypoint,
        custom_waypoints=[],
        arrival=waypoint,
        divert=None,
        bullseye=waypoint,
        nav_to=[],
        nav_from=[],
        hold=None,
        join=waypoint,
        split=waypoint,
        refuel=None,
        ingress=ingress,
        targets=[waypoint],
    )
    cached_plan = StrikeFlightPlan(cast(Any, SimpleNamespace()), layout)
    cached_targets = list(cached_plan.layout.ingress.targets)

    populator.populate()

    assert cached_plan.layout.ingress.targets == tgo.strike_targets
    assert all(
        cached is current for cached, current in zip(cached_targets, tgo.strike_targets)
    )
