"""Tests for the campaign-persistent CSAR mechanic.

Covers the pilot/downed-pilot state machine, squadron slot reservation, the CSAR
service (creation, survival window, rescue/MIA, turn ageing), the hybrid rescue
resolution in the results processor, the aircraft CSAR-capability derivation, and
state.json parsing of the new ejection/rescue keys.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import MagicMock, patch

import pytest
from dcs.mapping import Point
from dcs.terrain import Terrain

from game import persistency
from game.ato.flighttype import FlightType
from game.debriefing import StateData
from game.dcs.aircrafttype import AircraftType
from game.missiongenerator.aircraft.waypoints.pydcswaypointbuilder import (
    PydcsWaypointBuilder as _PydcsWaypointBuilder,
)
from game.sim.missionresultsprocessor import MissionResultsProcessor
from game.squadrons.csarservice import CsarService
from game.squadrons.downedpilot import DownedPilot
from game.squadrons.pilot import Pilot, PilotStatus


@pytest.fixture(autouse=True)
def _persistency(tmp_path: Path) -> None:
    persistency.setup(str(tmp_path), prefer_liberation_payloads=False, port=16885)


#: dcs.mapping.Point requires a real Terrain; a spec'd mock is the convention
#: used elsewhere in the suite (see tests/commander/test_motorpool_targeting.py)
#: for Points that are never actually projected to lat/lng.
_TERRAIN = MagicMock(spec=Terrain)


# ---------------------------------------------------------------------------
# Pilot state machine
# ---------------------------------------------------------------------------


def test_pilot_down_recover_active_cycle() -> None:
    pilot = Pilot("Joe")
    assert pilot.status is PilotStatus.Active

    pilot.go_down()
    assert pilot.downed
    assert pilot.alive  # a downed pilot is still alive

    pilot.begin_recovery(2)
    assert pilot.recovering
    assert pilot.turns_until_available == 2

    pilot.advance_recovery()
    assert pilot.recovering
    pilot.advance_recovery()
    assert pilot.status is PilotStatus.Active
    assert pilot.turns_until_available == 0


def test_pilot_down_to_mia() -> None:
    pilot = Pilot("Jane")
    pilot.go_down()
    pilot.go_mia()
    assert pilot.missing_in_action
    assert not pilot.alive


def test_begin_recovery_zero_turns_returns_active_immediately() -> None:
    pilot = Pilot("Zero")
    pilot.go_down()
    pilot.begin_recovery(0)
    assert pilot.status is PilotStatus.Active


def test_pilot_setstate_defaults_turns_until_available() -> None:
    pilot = Pilot("Old")
    # Simulate an old save with no turns_until_available field.
    state = dict(pilot.__dict__)
    del state["turns_until_available"]
    restored = Pilot.__new__(Pilot)
    restored.__setstate__(state)
    assert restored.turns_until_available == 0


# ---------------------------------------------------------------------------
# Squadron slot reservation
# ---------------------------------------------------------------------------


def _make_squadron(pilots: list[Pilot], pilot_limits: bool = True) -> Any:
    from game.squadrons.squadron import Squadron

    sqn = Squadron.__new__(Squadron)
    sqn.current_roster = pilots
    sqn.owned_aircraft = 12
    settings = SimpleNamespace(
        squadron_pilot_limit=10,
        enable_squadron_pilot_limits=pilot_limits,
        squadron_replenishment_rate=4,
    )
    sqn.settings = settings  # type: ignore[assignment]
    return sqn


def test_downed_and_recovering_pilots_hold_their_slot() -> None:
    active = [Pilot(f"A{i}") for i in range(6)]
    downed = Pilot("Down")
    downed.go_down()
    recovering = Pilot("Rec")
    recovering.begin_recovery(2)
    sqn = _make_squadron(active + [downed, recovering])

    # 10 slots, 6 active, but downed+recovering (2) also reserve a slot each.
    assert sqn._number_of_unfilled_pilot_slots == 10 - 6 - 2
    assert downed in sqn.downed_pilots
    assert recovering in sqn.recovering_pilots


def test_downed_pilots_are_untaskable_without_pilot_limits() -> None:
    """With per-squadron pilot limits off there is no slot to reserve, and
    replenishment is skipped entirely -- but a downed or recovering pilot must
    still be untaskable. Availability is rebuilt from the active pilots, and
    neither state is Active, so this holds without depending on the setting."""
    active = Pilot("A")
    downed = Pilot("Down")
    downed.go_down()
    recovering = Pilot("Rec")
    recovering.begin_recovery(2)
    sqn = _make_squadron([active, downed, recovering], pilot_limits=False)

    sqn.return_all_pilots_and_aircraft()
    assert sqn.available_pilots == [active]
    # No limit, so the squadron can always field whatever is asked of it; the
    # reservation above is simply not consulted.
    assert sqn.can_provide_pilots(99)
    sqn.replenish_lost_pilots()
    assert sqn.current_roster == [active, downed, recovering]


def test_rescued_pilot_returns_to_duty_without_pilot_limits() -> None:
    """The recovery countdown is not gated on the limits setting, so a rescued
    pilot still comes back rather than being stuck Recovering forever."""
    rescued = Pilot("Rescued")
    rescued.go_down()
    rescued.begin_recovery(1)
    sqn = _make_squadron([rescued], pilot_limits=False)

    sqn._process_pilot_recovery()
    assert rescued.status is PilotStatus.Active
    sqn.return_all_pilots_and_aircraft()
    assert sqn.available_pilots == [rescued]


def test_process_pilot_recovery_advances_countdown() -> None:
    recovering = Pilot("Rec")
    recovering.begin_recovery(1)
    sqn = _make_squadron([recovering])
    sqn._process_pilot_recovery()
    assert recovering.status is PilotStatus.Active


def test_living_pilots_excludes_mia() -> None:
    active = Pilot("A")
    mia = Pilot("M")
    mia.go_down()
    mia.go_mia()
    sqn = _make_squadron([active, mia])
    assert active in sqn.living_pilots
    assert mia not in sqn.living_pilots


# ---------------------------------------------------------------------------
# CsarService
# ---------------------------------------------------------------------------


def _blue_red_player() -> Any:
    from game.theater.player import Player

    return Player


def _make_game(**settings: Any) -> Any:
    from game.theater.player import Player

    defaults = dict(
        csar_enabled=True,
        csar_enabled_red=True,
        csar_ejection_chance=40,
        csar_survival_turns=3,
        csar_survival_turns_hostile=2,
        csar_ai_recovery_turns=2,
        csar_player_recovery_turns=1,
    )
    defaults.update(settings)
    game = MagicMock()
    game.settings = SimpleNamespace(**defaults)
    game.turn = 5
    game.db.downed_pilots = MagicMock()
    return game


def _make_downed(game: Any, player: Any, was_player: bool) -> DownedPilot:
    pilot = Pilot("Downed")
    squadron = MagicMock()
    squadron.player = player
    squadron.aircraft.display_name = "F/A-18C Hornet"
    squadron.coalition.downed_pilots = []
    flight = MagicMock()
    flight.squadron = squadron
    csar = CsarService(game)
    with patch(
        "game.squadrons.csarservice.find_downed_pilot_position",
        return_value=Point(100.0, 200.0, _TERRAIN),
    ):
        # Simplify survival-turn logic to a friendly rear position.
        game.theater.closest_control_point.return_value.is_friendly.return_value = True
        game.theater.conflicts.return_value = []
        downed = csar.down_pilot(flight, pilot, was_player, Point(0.0, 0.0, _TERRAIN))
    assert downed is not None
    return downed


def test_down_pilot_creates_downed_and_registers() -> None:
    from game.theater.player import Player

    game = _make_game()
    downed = _make_downed(game, Player.BLUE, was_player=True)
    assert downed.pilot.downed
    assert downed.turns_remaining == 3  # friendly rear
    assert downed in downed.squadron.coalition.downed_pilots
    game.db.downed_pilots.add.assert_called_once()


def test_survival_turns_hostile_when_near_front() -> None:
    from game.theater.player import Player

    game = _make_game()
    csar = CsarService(game)
    # Friendly-owned nearest CP, but a front line right on top of the pilot.
    game.theater.closest_control_point.return_value.is_friendly.return_value = True
    front = SimpleNamespace(position=Point(0.0, 0.0, _TERRAIN))
    game.theater.conflicts.return_value = [front]
    turns = csar._survival_turns(Point(0.0, 0.0, _TERRAIN), Player.BLUE)
    assert turns == 2


def test_survival_turns_hostile_when_enemy_territory() -> None:
    from game.theater.player import Player

    game = _make_game()
    csar = CsarService(game)
    game.theater.closest_control_point.return_value.is_friendly.return_value = False
    game.theater.conflicts.return_value = []
    turns = csar._survival_turns(Point(0.0, 0.0, _TERRAIN), Player.BLUE)
    assert turns == 2


def test_rescue_player_pilot_recovers_one_turn() -> None:
    from game.theater.player import Player

    game = _make_game()
    downed = _make_downed(game, Player.BLUE, was_player=True)
    CsarService(game).rescue(downed)
    assert downed.pilot.recovering
    assert downed.pilot.turns_until_available == 1
    assert downed not in downed.squadron.coalition.downed_pilots


def test_rescue_ai_pilot_recovers_two_turns() -> None:
    from game.theater.player import Player

    game = _make_game()
    downed = _make_downed(game, Player.RED, was_player=False)
    CsarService(game).rescue(downed)
    assert downed.pilot.turns_until_available == 2


def test_advance_turn_expires_to_mia() -> None:
    from game.theater.player import Player

    game = _make_game()
    downed = _make_downed(game, Player.BLUE, was_player=True)
    downed.turns_remaining = 1
    coalition = downed.squadron.coalition
    CsarService(game).advance_turn_for(coalition)
    assert downed.pilot.missing_in_action
    assert downed not in coalition.downed_pilots


def test_advance_turn_decrements_without_expiry() -> None:
    from game.theater.player import Player

    game = _make_game()
    downed = _make_downed(game, Player.BLUE, was_player=True)
    downed.turns_remaining = 3
    CsarService(game).advance_turn_for(downed.squadron.coalition)
    assert downed.turns_remaining == 2
    assert downed.pilot.downed


# ---------------------------------------------------------------------------
# Aircraft CSAR capability derivation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "display_name, expected",
    [
        ("UH-60A", True),
        ("CH-47F Block I", True),
        ("Mi-8MTV2 Hip", True),
        # Fixed-wing transports can't set down at an unprepared pickup site; the
        # DCS AI Land task is helicopter-only so they would just orbit the pilot.
        ("C-130J-30 Super Hercules", False),
        ("C-130J-30", False),
        ("OH-58D Kiowa Warrior", False),  # cabin_size 0
        ("F/A-18C Hornet (Lot 20)", False),  # not a transport
    ],
)
def test_csar_capability_derivation(display_name: str, expected: bool) -> None:
    match = None
    for ac in AircraftType.iter_all():
        if ac.display_name == display_name:
            match = ac
            break
    assert match is not None, f"aircraft {display_name} not found"
    assert match.capable_of(FlightType.CSAR) is expected


# ---------------------------------------------------------------------------
# StateData parsing
# ---------------------------------------------------------------------------


def test_statedata_parses_ejections_and_rescues() -> None:
    unit_map = MagicMock()
    unit_map.flight.return_value = None
    data = {
        "ejection_events": [
            {"unit": "Hornet 1-1", "x": 12.0, "z": 34.0},
            {"unit": "Viper 2-1", "x": 5.0, "z": 6.0, "landed": True},
        ],
        "csar_rescued": ["11111111-1111-1111-1111-111111111111"],
    }
    state = StateData.from_json(data, unit_map)
    assert state.ejections["Hornet 1-1"] == (12.0, 34.0)
    assert state.ejections["Viper 2-1"] == (5.0, 6.0)
    assert state.rescued_pilot_ids == ["11111111-1111-1111-1111-111111111111"]


def test_statedata_defaults_when_keys_absent() -> None:
    unit_map = MagicMock()
    unit_map.flight.return_value = None
    state = StateData.from_json({}, unit_map)
    assert state.ejections == {}
    assert state.rescued_pilot_ids == []


def test_statedata_skips_malformed_ejection() -> None:
    unit_map = MagicMock()
    unit_map.flight.return_value = None
    data = {"ejection_events": [{"x": 1.0, "z": 2.0}]}  # no unit
    state = StateData.from_json(data, unit_map)
    assert state.ejections == {}


# ---------------------------------------------------------------------------
# Loss processing: down vs. kill
# ---------------------------------------------------------------------------


def _loss(pilot: Pilot, player: Any) -> Any:
    squadron = MagicMock()
    squadron.player = player
    squadron.aircraft.display_name = "F/A-18C Hornet"
    squadron.coalition.downed_pilots = []
    flight = MagicMock()
    flight.squadron = squadron
    return SimpleNamespace(pilot=pilot, flight=flight)


def test_invulnerable_player_pilot_survives() -> None:
    from game.theater.player import Player

    game = _make_game()
    game.settings.invulnerable_player_pilots = True
    processor = MissionResultsProcessor(game)
    pilot = Pilot("P", player=True)
    loss = _loss(pilot, Player.BLUE)
    debriefing = MagicMock()
    debriefing.ejected_pilot_positions = {}
    processor._process_lost_pilot(loss, debriefing, CsarService(game))
    assert pilot.status is PilotStatus.Active


def test_ejection_downs_pilot() -> None:
    from game.theater.player import Player

    game = _make_game()
    game.settings.invulnerable_player_pilots = False
    game.theater.closest_control_point.return_value.is_friendly.return_value = True
    game.theater.conflicts.return_value = []
    processor = MissionResultsProcessor(game)
    pilot = Pilot("P", player=True)
    loss = _loss(pilot, Player.BLUE)
    debriefing = MagicMock()
    debriefing.ejected_pilot_positions = {id(pilot): Point(50.0, 60.0, _TERRAIN)}
    with patch(
        "game.squadrons.csarservice.find_downed_pilot_position",
        return_value=Point(50.0, 60.0, _TERRAIN),
    ):
        processor._process_lost_pilot(loss, debriefing, CsarService(game))
    assert pilot.downed


def test_no_ejection_failed_roll_kills() -> None:
    from game.theater.player import Player

    game = _make_game(csar_ejection_chance=0)  # never survive without ejection
    game.settings.invulnerable_player_pilots = False
    processor = MissionResultsProcessor(game)
    pilot = Pilot("P", player=False)
    loss = _loss(pilot, Player.BLUE)
    debriefing = MagicMock()
    debriefing.ejected_pilot_positions = {}
    processor._process_lost_pilot(loss, debriefing, CsarService(game))
    assert pilot.status is PilotStatus.Dead


def test_csar_disabled_kills() -> None:
    from game.theater.player import Player

    game = _make_game(csar_enabled=False)
    game.settings.invulnerable_player_pilots = False
    processor = MissionResultsProcessor(game)
    pilot = Pilot("P", player=True)
    loss = _loss(pilot, Player.BLUE)
    debriefing = MagicMock()
    debriefing.ejected_pilot_positions = {id(pilot): Point(1.0, 2.0, _TERRAIN)}
    processor._process_lost_pilot(loss, debriefing, CsarService(game))
    assert pilot.status is PilotStatus.Dead


# ---------------------------------------------------------------------------
# Hybrid rescue resolution
# ---------------------------------------------------------------------------


def _csar_flight_targeting(downed: DownedPilot, client_count: int) -> Any:
    flight = MagicMock()
    flight.flight_type = FlightType.CSAR
    flight.client_count = client_count
    flight.package.target = downed
    return flight


def _game_with_csar_package(downed: DownedPilot, flight: Any) -> Any:
    game = _make_game()
    package = SimpleNamespace(flights=[flight])
    blue = SimpleNamespace(ato=SimpleNamespace(packages=[package]))
    red = SimpleNamespace(ato=SimpleNamespace(packages=[]))
    game.coalitions = [blue, red]
    return game


def _standalone_downed() -> DownedPilot:
    pilot = Pilot("Rescuee")
    squadron = MagicMock()
    squadron.coalition.downed_pilots = []
    downed = DownedPilot(
        pilot=pilot,
        squadron=squadron,
        _position=Point(0.0, 0.0, _TERRAIN),
        player=_blue_red_player().BLUE,
        turn_downed=1,
        turns_remaining=3,
        was_player=False,
        aircraft_name="F/A-18C Hornet",
    )
    squadron.coalition.downed_pilots.append(downed)
    return downed


def test_lua_rescue_is_authoritative() -> None:
    downed = _standalone_downed()
    flight = _csar_flight_targeting(downed, client_count=1)
    game = _game_with_csar_package(downed, flight)
    game.db.downed_pilots.get.return_value = downed
    debriefing = MagicMock()
    debriefing.state_data.rescued_pilot_ids = [str(downed.id)]
    processor = MissionResultsProcessor(game)
    processor.commit_csar_results(debriefing)
    assert downed.pilot.recovering


def test_ai_flight_survives_rescues() -> None:
    downed = _standalone_downed()
    flight = _csar_flight_targeting(downed, client_count=0)
    game = _game_with_csar_package(downed, flight)
    debriefing = MagicMock()
    debriefing.state_data.rescued_pilot_ids = []
    debriefing.air_losses.surviving_flight_members.return_value = 2
    processor = MissionResultsProcessor(game)
    processor.commit_csar_results(debriefing)
    assert downed.pilot.recovering


def test_player_flight_without_lua_confirmation_fails() -> None:
    downed = _standalone_downed()
    flight = _csar_flight_targeting(downed, client_count=1)
    game = _game_with_csar_package(downed, flight)
    debriefing = MagicMock()
    debriefing.state_data.rescued_pilot_ids = []
    debriefing.air_losses.surviving_flight_members.return_value = 2
    processor = MissionResultsProcessor(game)
    processor.commit_csar_results(debriefing)
    assert not downed.pilot.recovering


def test_wiped_out_ai_flight_fails() -> None:
    downed = _standalone_downed()
    flight = _csar_flight_targeting(downed, client_count=0)
    game = _game_with_csar_package(downed, flight)
    debriefing = MagicMock()
    debriefing.state_data.rescued_pilot_ids = []
    debriefing.air_losses.surviving_flight_members.return_value = 0
    processor = MissionResultsProcessor(game)
    processor.commit_csar_results(debriefing)
    assert not downed.pilot.recovering


# ---------------------------------------------------------------------------
# Planning prerequisites
#
# These pin the two bugs that stopped CSAR missions from ever being planned:
# squadrons were never opted in to the CSAR task, and the flight plan depended on
# package waypoints that are deliberately not generated for friendly targets.
# ---------------------------------------------------------------------------


def test_csar_flight_plan_does_not_require_package_waypoints() -> None:
    """A DownedPilot is friendly, and IBuilder skips package-waypoint generation
    for friendly targets, so the CSAR layout must not depend on them."""
    import inspect

    from game.ato.flightplans import csar as csar_module

    source = inspect.getsource(csar_module)
    assert "package.waypoints" not in source, (
        "CSAR flight plan must not use package waypoints: they are never "
        "generated for friendly targets (see IBuilder."
        "_generate_package_waypoints_if_needed)"
    )


def test_csar_flight_plan_builds_from_standard_layout() -> None:
    from game.ato.flightplans.csar import CsarFlightPlan, CsarLayout
    from game.ato.flightplans.standard import StandardFlightPlan, StandardLayout

    assert issubclass(CsarFlightPlan, StandardFlightPlan)
    assert issubclass(CsarLayout, StandardLayout)


def test_enable_csar_if_capable_opts_in_capable_squadron() -> None:
    from game.squadrons.squadron import Squadron

    squadron = Squadron.__new__(Squadron)
    squadron.aircraft = _aircraft_named("UH-60A")
    squadron.auto_assignable_mission_types = {FlightType.TRANSPORT}
    squadron.enable_csar_if_capable()
    assert FlightType.CSAR in squadron.auto_assignable_mission_types


def test_enable_csar_if_capable_skips_incapable_squadron() -> None:
    from game.squadrons.squadron import Squadron

    squadron = Squadron.__new__(Squadron)
    squadron.aircraft = _aircraft_named("F/A-18C Hornet (Lot 20)")
    squadron.auto_assignable_mission_types = {FlightType.CAS}
    squadron.enable_csar_if_capable()
    assert FlightType.CSAR not in squadron.auto_assignable_mission_types


def test_set_auto_assignable_does_not_force_csar_on() -> None:
    """The Air Wing dialog applies the player's explicit choices through this
    method, so it must stay a pure filter or CSAR could never be turned off."""
    from game.squadrons.squadron import Squadron

    squadron = Squadron.__new__(Squadron)
    squadron.aircraft = _aircraft_named("UH-60A")
    squadron.set_auto_assignable_mission_types({FlightType.TRANSPORT})
    assert FlightType.CSAR not in squadron.auto_assignable_mission_types


def _opscsar_lua() -> str:
    return Path("resources/plugins/opscsar/OpsCSAR.lua").read_text(encoding="utf-8")


def test_ops_csar_considers_every_friendly_helicopter() -> None:
    """Ops.CSAR defaults to useprefix=true with csarPrefix={"helicargo","MEDEVAC"},
    and that set is the only source of csarUnits -- which drives both the F10 menu
    and MOOSE's boarding. Retribution names flights after the mission, so leaving
    the default means no player helicopter is ever a rescue helicopter."""
    assert "my.useprefix = false" in _opscsar_lua()


def test_player_rescues_are_credited_on_delivery_not_pickup() -> None:
    """Ops.CSAR destroys the survivor at pickup and credits the rescue only when
    they are delivered to a MASH or airfield. Our own vanish/carried detection
    fires the moment the survivor leaves the map, so it must ignore player
    helicopters or a crewed rescue is reported while the pilot is still aboard."""
    lua = _opscsar_lua()
    # rescue_helo_near drives both the vanish attribution and carried_out_of_zone.
    assert "helo_near(side_const, px, pz, PICKUP_RADIUS, PICKUP_MAX_AGL, true)" in lua
    # Delivery, via Ops.CSAR's own Rescued event, stays the reporting point.
    assert "function my:OnAfterRescued" in lua


def test_require_open_doors_is_wired_to_ops_csar() -> None:
    """The setting only means anything if it reaches MOOSE's pilotmustopendoors."""
    assert 'my.pilotmustopendoors = cfg.requireOpenDoors == "true"' in _opscsar_lua()


def test_ai_only_checks_are_asked_of_the_whole_group() -> None:
    """A Retribution flight is one DCS group holding the client slots and their AI
    wingmen. Testing units individually leaves the wingmen looking like an AI
    rescue flight -- and they are parked right next to the survivor, so every
    proximity check passes and the rescue is credited at pickup after all."""
    lua = _opscsar_lua()
    # One place asks the question, and it asks it of the group.
    assert lua.count("getPlayerName") == 1
    assert "local function group_has_player(group)" in lua
    # Both consumers go through it: the proximity scan and the LZ event handler.
    assert "not (ai_only and group_has_player(group))" in lua
    assert "return not group_has_player(group)" in lua


def test_boarded_hook_resolves_the_pilot_from_our_own_list() -> None:
    """Looking the id up in MOOSE's downedPilots is a race: the survivor's group
    is destroyed at pickup and Boarded is raised 5s later, while
    _CheckDownedPilotTable drops entries whose group has gone. Usually the entry
    survives that window; when it doesn't, the player's rescue goes unrecorded."""
    lua = _opscsar_lua()
    boarded = lua.split("function my:OnAfterBoarded")[1].split("function my:")[0]
    assert "tracked_by_group(Woundedgroupname)" in boarded
    assert "pairs(self.downedPilots" not in boarded


def test_aicsar_warning_does_not_fire_on_the_class_alone() -> None:
    """Moose.lua always defines the AICSAR class, so a bare nil check warns on
    every mission and sends players chasing a conflict that isn't there."""
    lua = _opscsar_lua()
    assert 'AICSAR ~= nil and AICSAR.lid ~= nil and AICSAR.lid ~= ""' in lua


def _csar_planning_state(targets: list[DownedPilot], max_flights: int) -> Any:
    from game.commander.theaterstate import TheaterState

    state = TheaterState.__new__(TheaterState)
    state.csar_targets = list(targets)
    state.csar_flights_planned = 0
    state.context = cast(
        Any, SimpleNamespace(settings=SimpleNamespace(max_csar_flights=max_flights))
    )
    return state


def test_csar_planning_stops_at_the_flight_cap() -> None:
    """The cap counts packages actually committed, so the planner keeps working
    down the (closest-first) list until it has the configured number."""
    from game.commander.tasks.primitive.csar import PlanCsar

    targets = [_standalone_downed() for _ in range(4)]
    state = _csar_planning_state(targets, max_flights=2)

    planned = []
    for target in list(targets):
        task = PlanCsar(target)
        # Isolate the cap from the rest of the preconditions (threat, aircraft
        # availability), which need a whole game to evaluate.
        with patch.object(
            PlanCsar, "target_area_preconditions_met", return_value=True
        ), patch(
            "game.commander.tasks.packageplanningtask.PackagePlanningTask"
            ".preconditions_met",
            return_value=True,
        ):
            if task.preconditions_met(state):
                planned.append(target)
                with patch.object(type(task), "package", None):
                    task.apply_effects(state)

    assert planned == targets[:2]
    assert state.csar_flights_planned == 2


def test_csar_flight_cap_of_zero_disables_auto_planning() -> None:
    from game.commander.tasks.primitive.csar import PlanCsar

    targets = [_standalone_downed()]
    state = _csar_planning_state(targets, max_flights=0)

    task = PlanCsar(targets[0])
    with patch.object(PlanCsar, "target_area_preconditions_met", return_value=True):
        assert not task.preconditions_met(state)


def test_unreachable_pilot_does_not_consume_a_flight_slot() -> None:
    """A pilot the planner can't reach (live SAM ring) must not use up one of the
    slots, or a rescuable pilot further down the list is silently skipped."""
    from game.commander.tasks.primitive.csar import PlanCsar

    targets = [_standalone_downed() for _ in range(2)]
    state = _csar_planning_state(targets, max_flights=1)

    blocked = PlanCsar(targets[0])
    with patch.object(PlanCsar, "target_area_preconditions_met", return_value=False):
        assert not blocked.preconditions_met(state)
    assert state.csar_flights_planned == 0

    reachable = PlanCsar(targets[1])
    with patch.object(
        PlanCsar, "target_area_preconditions_met", return_value=True
    ), patch(
        "game.commander.tasks.packageplanningtask.PackagePlanningTask"
        ".preconditions_met",
        return_value=True,
    ):
        assert reachable.preconditions_met(state)


def test_csar_flight_cap_is_per_side_and_survives_cloning() -> None:
    """The allowance is per coalition, not a shared pool: TheaterCommander is
    constructed per player and builds its own TheaterState, so each side starts
    at zero. Within a side it must then survive the HTN's per-branch cloning and
    the replanning loop, or every branch would get a fresh allowance."""
    import inspect

    from game.commander.theaterstate import TheaterState
    from game.commander.theatercommander import TheaterCommander

    # Fresh per side.
    assert "csar_flights_planned=0" in inspect.getsource(TheaterState.from_game)
    planning = inspect.getsource(TheaterCommander.plan_missions)
    assert "TheaterState.from_game(self.game, self.player" in planning
    # ...but carried forward within that side's planning.
    assert "state = result.end_state" in planning
    assert "csar_flights_planned=self.csar_flights_planned" in inspect.getsource(
        TheaterState.clone
    )


def _pickup_builder(
    downed: DownedPilot,
    hover: bool,
    with_group: bool = True,
    switch_baro_fix: bool = True,
    in_sea: bool = False,
) -> Any:
    from game.missiongenerator.aircraft.waypoints.csarpickup import CsarPickupBuilder
    from game.missiongenerator.missiondata import CsarPilotGroupInfo

    builder = CsarPickupBuilder.__new__(CsarPickupBuilder)
    settings = SimpleNamespace(
        csar_hover_extraction=hover,
        use_ai_combat_landing=False,
        switch_baro_fix=switch_baro_fix,
    )
    theater = MagicMock()
    theater.is_in_sea.return_value = in_sea
    theater.is_on_land.return_value = not in_sea
    builder.flight = cast(
        Any,
        SimpleNamespace(
            is_helo=True,
            package=SimpleNamespace(target=downed),
            coalition=SimpleNamespace(
                game=SimpleNamespace(settings=settings, theater=theater)
            ),
        ),
    )
    builder.group = cast(Any, SimpleNamespace(name="Enfield 1-1"))
    groups = {}
    if with_group:
        groups[str(downed.id)] = CsarPilotGroupInfo(
            group_name="CSAR Rescuee 1234abcd",
            unit_name="CSAR Rescuee 1234abcd Unit #1",
            group_id=4242,
            blue=True,
        )
    builder.mission_data = cast(Any, SimpleNamespace(csar_pilot_groups=groups))
    return builder


def test_csar_pickup_embarks_without_a_land_task() -> None:
    """The Embarking task performs the landing itself; adding a Land task
    alongside it only fights it for control of the approach."""
    from dcs.task import Embarking, Land

    downed = _standalone_downed()
    builder = _pickup_builder(downed, hover=False)
    waypoint = MagicMock()
    waypoint.position = Point(10.0, 20.0, _TERRAIN)

    with patch.object(_PydcsWaypointBuilder, "build", return_value=waypoint):
        builder.build()

    tasks = [call.args[0] for call in waypoint.add_task.call_args_list]
    embarking = [t for t in tasks if isinstance(t, Embarking)]
    assert len(embarking) == 1
    assert embarking[0].params["groupsForEmbarking"] == {4242: 4242}
    assert not [t for t in tasks if isinstance(t, Land)]


def _layout_builder(hover: bool, target: DownedPilot) -> Any:
    from game.ato.flightplans.csar import Builder

    builder = Builder.__new__(Builder)
    builder.flight = cast(
        Any,
        SimpleNamespace(
            departure=SimpleNamespace(position=Point(50000.0, 0.0, _TERRAIN)),
            package=SimpleNamespace(target=target),
        ),
    )
    builder.settings = cast(Any, SimpleNamespace(csar_hover_extraction=hover))
    return builder


def test_landing_zone_is_clear_of_the_survivor() -> None:
    """The AI sets down exactly on its waypoint, so a landing zone on top of the
    pilot crushes them. It must still be inside the embark zone or the pilot will
    never walk out to board."""
    from game.ato.flightplans.csar import LANDING_ZONE_OFFSET
    from game.missiongenerator.csargenerator import EMBARK_ZONE_RADIUS

    downed = _standalone_downed()
    downed._position = Point(0.0, 0.0, _TERRAIN)

    builder = _layout_builder(hover=False, target=downed)
    theater = MagicMock()
    theater.is_on_land.return_value = True
    with patch.object(type(builder), "theater", property(lambda self: theater)):
        landing_zone = builder._landing_zone_for(downed)

    separation = landing_zone.distance_to_point(downed.position)
    assert separation == pytest.approx(LANDING_ZONE_OFFSET.meters, rel=0.01)
    # Far enough that the AI will actually commit to the landing. It keeps a
    # clear area around existing ground units, and the survivor is one: at 75m
    # the helicopters flew the whole embark phase without ever setting down.
    assert separation >= 125
    # ...but well inside the embark zone, leaving room for the AI's own landing
    # dispersion. A touchdown outside that radius is never reached and the rescue
    # silently fails.
    assert separation <= EMBARK_ZONE_RADIUS.meters * 0.6


def test_hover_pickup_sits_on_top_of_the_survivor() -> None:
    """A hoist has nothing to land on the pilot, so the offset that keeps the AI
    from crushing them on touchdown is just distance the winch can't cover."""
    from game.ato.flightplans.csar import HOVER_PICKUP_OFFSET, LANDING_ZONE_OFFSET

    downed = _standalone_downed()
    downed._position = Point(0.0, 0.0, _TERRAIN)

    builder = _layout_builder(hover=True, target=downed)
    theater = MagicMock()
    theater.is_on_land.return_value = True
    with patch.object(type(builder), "theater", property(lambda self: theater)):
        pickup = builder._landing_zone_for(downed)

    separation = pickup.distance_to_point(downed.position)
    assert separation == pytest.approx(HOVER_PICKUP_OFFSET.meters, rel=0.01)
    assert HOVER_PICKUP_OFFSET < LANDING_ZONE_OFFSET


def test_landing_zone_avoids_water() -> None:
    downed = _standalone_downed()
    downed._position = Point(0.0, 0.0, _TERRAIN)

    builder = _layout_builder(hover=False, target=downed)
    theater = MagicMock()
    # Reject the first (approach-side) bearing, accept the next.
    theater.is_on_land.side_effect = [False, True]
    with patch.object(type(builder), "theater", property(lambda self: theater)):
        builder._landing_zone_for(downed)
    assert theater.is_on_land.call_count == 2


# ---------------------------------------------------------------------------
# Survivors in the water
# ---------------------------------------------------------------------------


def test_pilot_in_the_water_forces_hover_extraction() -> None:
    """Nothing can land beside a survivor at sea, so they are hoisted whatever
    the setting says. The setting still forces hover for pilots on land."""
    from game.settings import Settings

    settings = Settings()
    settings.csar_hover_extraction = False

    ashore = _standalone_downed()
    ashore.in_water = False
    assert not ashore.needs_hover_extraction(settings)

    ditched = _standalone_downed()
    ditched.in_water = True
    assert ditched.needs_hover_extraction(settings)

    settings.csar_hover_extraction = True
    assert ashore.needs_hover_extraction(settings)


def test_downed_pilot_from_an_old_save_is_not_in_water() -> None:
    downed = _standalone_downed()
    state = dict(downed.__dict__)
    del state["in_water"]
    restored = DownedPilot.__new__(DownedPilot)
    restored.__setstate__(state)
    assert restored.in_water is False


def test_ditched_pilot_stays_where_they_came_down() -> None:
    """A hoist can be flown anywhere, so there is nothing to gain by putting a
    survivor ashore -- and no distance offshore at which they become unreachable."""
    from game.squadrons.csarplacement import find_downed_pilot_position

    theater = MagicMock()
    theater.is_in_sea.return_value = True
    ditched = Point(500000.0, 500000.0, _TERRAIN)

    assert find_downed_pilot_position(theater, ditched) == ditched
    # Not dragged to the coast, and never written off for being too far out.
    theater.nearest_land_pos.assert_not_called()


def test_pilot_down_on_land_is_still_snapped() -> None:
    from game.squadrons.csarplacement import find_downed_pilot_position

    theater = MagicMock()
    theater.is_in_sea.return_value = False
    theater.is_on_land.return_value = True
    theater.controlpoints = []
    theater.ground_objects = []
    ashore = Point(10.0, 20.0, _TERRAIN)

    assert find_downed_pilot_position(theater, ashore) == ashore


def test_hover_pickup_does_not_look_for_dry_land() -> None:
    """The bearing search exists to find a touchdown. A survivor in the water
    would fail it on every bearing, and it is pointless for a hoist anyway."""
    downed = _standalone_downed()
    downed._position = Point(0.0, 0.0, _TERRAIN)
    downed.in_water = True

    builder = _layout_builder(hover=False, target=downed)
    theater = MagicMock()
    theater.is_on_land.return_value = False
    with patch.object(type(builder), "theater", property(lambda self: theater)):
        pickup = builder._landing_zone_for(downed)

    theater.is_on_land.assert_not_called()
    from game.ato.flightplans.csar import HOVER_PICKUP_OFFSET

    separation = pickup.distance_to_point(downed.position)
    assert separation == pytest.approx(HOVER_PICKUP_OFFSET.meters, rel=0.01)


def test_csar_pickup_prefers_vertical_landing() -> None:
    """The pickup is unprepared ground with a survivor stood beside it, so the
    helicopter should set down vertically rather than running on."""
    from dcs.task import OptVerticalTakeoffLanding

    downed = _standalone_downed()
    builder = _pickup_builder(downed, hover=False)
    waypoint = MagicMock()
    waypoint.position = Point(10.0, 20.0, _TERRAIN)

    with patch.object(_PydcsWaypointBuilder, "build", return_value=waypoint):
        builder.build()

    tasks = [call.args[0] for call in waypoint.add_task.call_args_list]
    vtol = [t for t in tasks if isinstance(t, OptVerticalTakeoffLanding)]
    assert len(vtol) == 1
    assert vtol[0].params["action"]["params"]["value"] is True


def test_csar_start_type_setting_is_a_start_type() -> None:
    from game.ato.starttype import StartType
    from game.settings import Settings

    start_type = Settings().csar_start_type
    assert isinstance(start_type, StartType)
    # A downed pilot is on a timer, so rescues launch quicker than the rest of
    # the ATO by default.
    assert start_type is StartType.WARM


def test_settings_start_type_for_csar_overrides_both_defaults() -> None:
    """The setting exists so CSAR need not inherit the AI default, so it has to
    beat the player default too -- otherwise a crewed rescue would silently fall
    back to whatever players use."""
    from game.ato.flighttype import FlightType
    from game.ato.starttype import StartType
    from game.settings import Settings

    settings = Settings()
    settings.default_start_type = StartType.COLD
    settings.default_start_type_client = StartType.RUNWAY
    settings.csar_start_type = StartType.WARM

    assert settings.start_type_for(FlightType.CSAR, has_players=False) is StartType.WARM
    assert settings.start_type_for(FlightType.CSAR, has_players=True) is StartType.WARM
    # Everything else is unaffected.
    assert settings.start_type_for(FlightType.CAS, has_players=False) is StartType.COLD
    assert settings.start_type_for(FlightType.CAS, has_players=True) is StartType.RUNWAY


def test_package_builder_applies_the_csar_start_type() -> None:
    """The auto-planner must actually apply it rather than leaving the flight on
    the start type PackageBuilder was constructed with."""
    from game.ato.flighttype import FlightType
    from game.ato.starttype import StartType
    from game.commander.packagebuilder import PackageBuilder
    from game.settings import Settings

    settings = Settings()
    settings.default_start_type = StartType.COLD
    settings.csar_start_type = StartType.WARM

    builder = PackageBuilder.__new__(PackageBuilder)
    builder.start_type = StartType.COLD
    builder.is_player = True
    builder.package = MagicMock()
    builder.package.primary_flight = None
    builder.air_wing = MagicMock()
    builder.laser_code_registry = MagicMock()
    builder.closest_airfields = MagicMock()

    squadron = builder.air_wing.best_squadron_for.return_value
    squadron.location.required_aircraft_start_type = None
    squadron.coalition.game.settings = settings

    plan = MagicMock()
    plan.task = FlightType.CSAR

    with patch("game.commander.packagebuilder.Flight") as flight_cls, patch(
        "game.commander.packagebuilder.apply_default_player_laser_code"
    ), patch.object(PackageBuilder, "find_divert_field", return_value=None):
        flight_cls.return_value.roster.player_count = 0
        assert builder.plan_flight(plan, ignore_range=False)

    assert flight_cls.return_value.start_type is StartType.WARM


def test_package_builder_respects_a_base_that_dictates_its_start_type() -> None:
    """Carriers and off-map spawns override everything; CSAR must not undo that."""
    from game.ato.flighttype import FlightType
    from game.ato.starttype import StartType
    from game.commander.packagebuilder import PackageBuilder
    from game.settings import Settings

    settings = Settings()
    settings.csar_start_type = StartType.WARM

    builder = PackageBuilder.__new__(PackageBuilder)
    builder.start_type = StartType.COLD
    builder.is_player = True
    builder.package = MagicMock()
    builder.package.primary_flight = None
    builder.air_wing = MagicMock()
    builder.laser_code_registry = MagicMock()
    builder.closest_airfields = MagicMock()

    squadron = builder.air_wing.best_squadron_for.return_value
    squadron.location.required_aircraft_start_type = StartType.IN_FLIGHT
    squadron.coalition.game.settings = settings

    plan = MagicMock()
    plan.task = FlightType.CSAR

    with patch("game.commander.packagebuilder.Flight") as flight_cls, patch(
        "game.commander.packagebuilder.apply_default_player_laser_code"
    ), patch.object(PackageBuilder, "find_divert_field", return_value=None):
        flight_cls.return_value.roster.player_count = 0
        assert builder.plan_flight(plan, ignore_range=False)

    # Constructed with the base's start type and never reassigned.
    assert flight_cls.call_args.args[4] is StartType.IN_FLIGHT
    assert not isinstance(flight_cls.return_value.start_type, StartType)


def test_start_type_defaults_are_decided_in_one_place() -> None:
    """CSAR ended up inheriting the AI default because this rule was duplicated
    across the planner and two UI paths, and only the planner was taught about
    CSAR. Each must defer to Settings.start_type_for instead of reading the
    default_start_type* fields itself, or the next task-specific start type will
    break the same way."""
    import inspect

    from game.commander.packagebuilder import PackageBuilder
    from qt_ui.windows.mission.flight.QFlightCreator import QFlightCreator
    from qt_ui.windows.mission.flight.settings.QFlightStartType import QFlightStartType

    deciders = (
        PackageBuilder.plan_flight,
        QFlightCreator.on_pilot_selected,
        QFlightStartType.on_pilot_selected,
    )
    for decider in deciders:
        source = inspect.getsource(decider)
        assert "start_type_for" in source, decider.__qualname__
        assert "default_start_type" not in source, decider.__qualname__


def test_csar_pickup_hover_mode_hands_off_to_the_script() -> None:
    """Nothing in the .miz can hold the AI in a hover: the DCS Orbit task takes an
    MSL altitude and we have no terrain elevation here. So the waypoint only tells
    OpsCSAR.lua which flight is on station for which pilot, and the script -- which
    can ask land.getHeight -- sets up the hover itself."""
    from dcs.task import ControlledTask, Embarking, Land, RunScript
    from game.missiongenerator.aircraft.waypoints.csarpickup import HOVER_ALTITUDE

    downed = _standalone_downed()
    builder = _pickup_builder(downed, hover=True)
    waypoint = MagicMock()
    waypoint.position = Point(10.0, 20.0, _TERRAIN)

    with patch.object(_PydcsWaypointBuilder, "build", return_value=waypoint):
        builder.build()

    tasks = [call.args[0] for call in waypoint.add_task.call_args_list]
    assert not [t for t in tasks if isinstance(t, (Embarking, Land, ControlledTask))]

    scripts = [t for t in tasks if isinstance(t, RunScript)]
    assert len(scripts) == 1
    command = scripts[0].params["action"]["params"]["command"]
    assert "OpsCSAR_BeginHover('Enfield 1-1', '%s')" % downed.id in command
    # OpsCSAR.lua never defines the global if it found no CSAR data to work with,
    # and an undefined global would throw at the waypoint.
    assert command.startswith("if OpsCSAR_BeginHover then ")

    # Still arrives low, so the script's hover is a small correction rather than a
    # descent from cruise.
    assert waypoint.alt == int(HOVER_ALTITUDE.meters)
    assert waypoint.alt_type == "RADIO"


def test_hover_over_water_holds_an_amsl_altitude() -> None:
    """DCS measures AGL from the sea *bottom* -- the reason switch_baro_fix
    exists -- so a hover held on RADIO over deep water would be underwater. The
    number is the same either way; only the reference changes."""
    downed = _standalone_downed()
    downed.in_water = True
    builder = _pickup_builder(downed, hover=True, in_sea=True)
    waypoint = MagicMock()
    waypoint.position = Point(10.0, 20.0, _TERRAIN)

    with patch.object(_PydcsWaypointBuilder, "build", return_value=waypoint):
        builder.build()

    from game.missiongenerator.aircraft.waypoints.csarpickup import HOVER_ALTITUDE

    assert waypoint.alt_type == "BARO"
    assert waypoint.alt == int(HOVER_ALTITUDE.meters)


def test_hover_over_water_respects_the_setting_being_off() -> None:
    downed = _standalone_downed()
    downed.in_water = True
    builder = _pickup_builder(downed, hover=True, in_sea=True, switch_baro_fix=False)
    waypoint = MagicMock()
    waypoint.position = Point(10.0, 20.0, _TERRAIN)

    with patch.object(_PydcsWaypointBuilder, "build", return_value=waypoint):
        builder.build()

    assert waypoint.alt_type == "RADIO"


def test_hover_over_land_stays_agl() -> None:
    """Over land AGL is what we want: the hold should follow the terrain rather
    than being pinned to a sea-level reference on a hillside."""
    downed = _standalone_downed()
    builder = _pickup_builder(downed, hover=True, in_sea=False)
    waypoint = MagicMock()
    waypoint.position = Point(10.0, 20.0, _TERRAIN)

    with patch.object(_PydcsWaypointBuilder, "build", return_value=waypoint):
        builder.build()

    assert waypoint.alt_type == "RADIO"


def test_csar_pickup_hoists_a_ditched_pilot_with_the_setting_off() -> None:
    """The whole point of the flag: a survivor in the water gets the scripted
    hoist even though the mission is set up for landing pickups."""
    from dcs.task import Embarking, RunScript

    downed = _standalone_downed()
    downed.in_water = True
    builder = _pickup_builder(downed, hover=False)
    waypoint = MagicMock()
    waypoint.position = Point(10.0, 20.0, _TERRAIN)

    with patch.object(_PydcsWaypointBuilder, "build", return_value=waypoint):
        builder.build()

    tasks = [call.args[0] for call in waypoint.add_task.call_args_list]
    assert not [t for t in tasks if isinstance(t, Embarking)]
    assert [t for t in tasks if isinstance(t, RunScript)]


def test_csar_pickup_without_a_pilot_group_adds_no_task() -> None:
    downed = _standalone_downed()
    builder = _pickup_builder(downed, hover=False, with_group=False)
    waypoint = MagicMock()
    waypoint.position = Point(0.0, 0.0, _TERRAIN)

    with patch.object(_PydcsWaypointBuilder, "build", return_value=waypoint):
        builder.build()

    waypoint.add_task.assert_not_called()


def test_csar_pickup_uses_dedicated_builder() -> None:
    from game.ato.flightwaypointtype import FlightWaypointType
    from game.missiongenerator.aircraft.waypoints.csarpickup import CsarPickupBuilder
    from game.missiongenerator.aircraft.waypoints.waypointgenerator import (
        WaypointGenerator,
    )

    generator = WaypointGenerator.__new__(WaypointGenerator)
    generator.flight = MagicMock()
    generator.group = MagicMock()
    generator.mission = MagicMock()
    generator.time = MagicMock()
    generator.settings = MagicMock()
    generator.mission_data = MagicMock()
    waypoint = MagicMock()
    waypoint.waypoint_type = FlightWaypointType.CSAR_PICKUP
    assert isinstance(generator.builder_for_waypoint(waypoint), CsarPickupBuilder)


def _aircraft_named(display_name: str) -> Any:
    for aircraft in AircraftType.iter_all():
        if aircraft.display_name == display_name:
            return aircraft
    raise AssertionError(f"aircraft {display_name} not found")


# ---------------------------------------------------------------------------
# Downed pilots as real mission groups (native DCS embark)
# ---------------------------------------------------------------------------


def test_csar_generator_places_pilot_with_embark_task() -> None:
    """Each downed pilot must exist in the mission as a ground group carrying
    EmbarkToTransport: that is what lets stock DCS transport logic walk them to
    an embarking helicopter, which is the only way an AI rescue can work."""
    from dcs import Mission
    from dcs.task import EmbarkToTransport
    from dcs.terrain import Caucasus
    from game.missiongenerator.csargenerator import CsarGenerator
    from game.missiongenerator.missiondata import MissionData
    from game.theater.player import Player

    mission, mission_data, downed = _generate_csar(hover=False)

    info = mission_data.csar_pilot_groups[str(downed.id)]
    assert info.blue is True
    group = next(
        g for g in mission.country("USA").vehicle_group if g.name == info.group_name
    )
    assert group.id == info.group_id
    # OpsCSAR.lua decides whether the survivor is still on the map by looking this
    # name up in DCS's unit registry, so it has to be the unit actually placed.
    assert info.unit_name == group.units[0].name
    tasks = group.points[0].tasks
    assert [t for t in tasks if isinstance(t, EmbarkToTransport)]
    # The template Ops.CSAR is constructed against must also exist.
    assert mission_data.csar_pilot_templates["blue"] == "CSAR_PILOT_BLUE"


def test_csar_generator_omits_embark_task_for_a_ditched_pilot() -> None:
    """The embark never fires without weight off wheels, and nothing is going to
    put weight on wheels next to a survivor at sea."""
    from dcs.task import EmbarkToTransport

    mission, mission_data, downed = _generate_csar(hover=False, in_water=True)

    info = mission_data.csar_pilot_groups[str(downed.id)]
    group = next(
        g for g in mission.country("USA").vehicle_group if g.name == info.group_name
    )
    assert not [t for t in group.points[0].tasks if isinstance(t, EmbarkToTransport)]


def test_csar_generator_omits_embark_task_under_hover_extraction() -> None:
    """With hover extraction the pilot never walks aboard, so the embark task
    would be dead weight -- OpsCSAR.lua does the pickup by script."""
    from dcs.task import EmbarkToTransport

    mission, mission_data, downed = _generate_csar(hover=True)

    info = mission_data.csar_pilot_groups[str(downed.id)]
    group = next(
        g for g in mission.country("USA").vehicle_group if g.name == info.group_name
    )
    assert not [t for t in group.points[0].tasks if isinstance(t, EmbarkToTransport)]


def _generate_csar(hover: bool, in_water: bool = False) -> Any:
    from dcs import Mission
    from dcs.terrain import Caucasus
    from game.missiongenerator.csargenerator import CsarGenerator
    from game.missiongenerator.missiondata import MissionData
    from game.theater.player import Player

    mission = Mission(Caucasus())
    downed = _standalone_downed()
    downed._position = Point(-250000.0, 630000.0, mission.terrain)
    downed.in_water = in_water

    coalition = SimpleNamespace(
        player=Player.BLUE,
        downed_pilots=[downed],
        faction=SimpleNamespace(country=SimpleNamespace(name="USA")),
    )
    game = MagicMock()
    game.settings.csar_enabled = True
    game.settings.csar_enabled_red = False
    game.settings.csar_hover_extraction = hover
    game.theater.terrain = mission.terrain
    game.coalition_for.return_value = coalition

    mission_data = MissionData()
    CsarGenerator(mission, game, mission_data).generate()
    return mission, mission_data, downed


def test_csar_generator_skips_disabled_coalition() -> None:
    from dcs import Mission
    from dcs.terrain import Caucasus
    from game.missiongenerator.csargenerator import CsarGenerator
    from game.missiongenerator.missiondata import MissionData

    mission = Mission(Caucasus())
    game = MagicMock()
    game.settings.csar_enabled = False
    game.settings.csar_enabled_red = False
    mission_data = MissionData()
    CsarGenerator(mission, game, mission_data).generate()

    assert mission_data.csar_pilot_groups == {}
    assert mission_data.csar_pilot_templates == {}


# ---------------------------------------------------------------------------
# Lua data serialization
# ---------------------------------------------------------------------------


def test_generate_csar_data_serializes_and_evaluates() -> None:
    import lupa

    from game.missiongenerator.luagenerator import LuaData, LuaGenerator
    from game.missiongenerator.missiondata import CsarPilotGroupInfo, MissionData
    from game.theater.player import Player

    game = MagicMock()
    game.settings.csar_enabled = True
    game.settings.csar_enabled_red = False
    game.settings.csar_warm_start = True
    game.settings.csar_rescue_ai_pilots = True
    game.settings.csar_require_open_doors = False
    game.settings.csar_hover_extraction = True
    squadron = MagicMock()
    squadron.coalition.player = Player.BLUE
    downed = DownedPilot(
        pilot=Pilot("Ivan Doe"),
        squadron=squadron,
        _position=Point(12345.0, 67890.0, _TERRAIN),
        player=Player.BLUE,
        turn_downed=2,
        turns_remaining=3,
        was_player=False,
        aircraft_name="UH-60A",
    )
    game.blue.player = Player.BLUE
    game.blue.downed_pilots = [downed]
    game.blue.faction.country.id = 15  # Israel
    game.red.player = Player.RED
    game.red.downed_pilots = []
    game.red.faction.country.id = 18  # Syria

    mission_data = MissionData()
    mission_data.csar_pilot_templates = {"blue": "CSAR_PILOT_BLUE"}
    # CsarGenerator has already placed the pilot in the mission by this point.
    mission_data.csar_pilot_groups = {
        str(downed.id): CsarPilotGroupInfo(
            group_name="CSAR Ivan Doe abcd1234",
            unit_name="CSAR Ivan Doe abcd1234 Unit #1",
            group_id=77,
            blue=True,
        )
    }
    generator = LuaGenerator.__new__(LuaGenerator)
    generator.game = game
    generator.mission_data = mission_data

    lua_data = LuaData("dcsRetribution")
    generator.generate_csar_data(lua_data)
    serialized = lua_data.serialize()

    # The serialized table must round-trip through a real Lua interpreter with the
    # flags, downed pilot and rescue whitelist intact (LuaData silently drops
    # scalar keys on a node that also has children, so this pins the workaround).
    runtime = lupa.LuaRuntime()
    runtime.execute(serialized)
    csar = runtime.globals().dcsRetribution.CSAR
    assert csar.blueEnabled == "true"
    assert csar.redEnabled == "false"
    assert csar.blueTemplate == "CSAR_PILOT_BLUE"
    # MOOSE spawns the pilot with InitCountry(), and DCS derives coalition
    # membership from country, so these must be the faction's own countries
    # rather than MOOSE's USA/Russia defaults.
    assert csar.blueCountry == "15"
    assert csar.redCountry == "18"
    # Tells OpsCSAR.lua whether to script the pickup or leave it to DCS's embark.
    assert csar.hoverExtraction == "true"
    # Ops.CSAR's pilotmustopendoors, off by default.
    assert csar.requireOpenDoors == "false"
    # How the scripted hoist is flown. csarpickup.py owns both numbers so the
    # waypoint and the script holding the flight over it agree.
    from game.missiongenerator.aircraft.waypoints.csarpickup import (
        HOVER_ALTITUDE,
        HOVER_DURATION_SECONDS,
    )

    assert csar.hoverDurationSeconds == str(HOVER_DURATION_SECONDS)
    assert csar.hoverAltitudeMeters == str(round(HOVER_ALTITUDE.meters))
    # Shared with the pilot's EmbarkToTransport task so the signal smoke matches
    # the zone they can actually be picked up in.
    from game.missiongenerator.csargenerator import EMBARK_ZONE_RADIUS

    assert csar.embarkZoneRadius == str(round(EMBARK_ZONE_RADIUS.meters))
    assert csar.downedPilots[1].id == str(downed.id)
    assert csar.downedPilots[1].aircraft == "UH-60A"
    # The pilot is already placed in the mission; OpsCSAR.lua hands this group to
    # Ops.CSAR so a player can rescue them.
    assert csar.downedPilots[1].groupName == "CSAR Ivan Doe abcd1234"
    # The survivor's own unit, which is what OpsCSAR.lua asks the unit registry
    # about to decide whether they are still on the map.
    assert csar.downedPilots[1].unitName == "CSAR Ivan Doe abcd1234 Unit #1"
    # Decided per pilot, not per mission, so a survivor in the water can be
    # hoisted out of a mission that otherwise uses landing pickups.
    assert csar.downedPilots[1].hoverExtraction == "true"
    rescue_ids = {
        csar.rescueTypes[i].dcs_id for i in range(1, len(csar.rescueTypes) + 1)
    }
    # Transport helicopters MOOSE ships no default capacity for must still be
    # whitelisted, and fixed-wing must not appear at all.
    assert "CH-47D" in rescue_ids
    assert "Hercules" not in rescue_ids
    assert "C-130J-30" not in rescue_ids
