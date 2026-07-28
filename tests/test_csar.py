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


def _make_squadron(pilots: list[Pilot]) -> Any:
    from game.squadrons.squadron import Squadron

    sqn = Squadron.__new__(Squadron)
    sqn.current_roster = pilots
    settings = SimpleNamespace(
        squadron_pilot_limit=10, enable_squadron_pilot_limits=True
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


def test_csar_pickup_embarks_the_matching_pilot_group() -> None:
    """The rescue helicopter's pickup waypoint must carry an Embarking task
    naming the downed pilot's own group; that is the half of DCS's native troop
    transport that pairs with the pilot's EmbarkToTransport task."""
    from dcs.task import Embarking, Land
    from game.missiongenerator.aircraft.waypoints.csarpickup import CsarPickupBuilder
    from game.missiongenerator.missiondata import CsarPilotGroupInfo

    downed = _standalone_downed()
    builder = CsarPickupBuilder.__new__(CsarPickupBuilder)
    builder.flight = cast(Any, SimpleNamespace(package=SimpleNamespace(target=downed)))
    builder.mission_data = cast(
        Any,
        SimpleNamespace(
            csar_pilot_groups={
                str(downed.id): CsarPilotGroupInfo(
                    group_name="CSAR Rescuee 1234abcd", group_id=4242, blue=True
                )
            }
        ),
    )
    waypoint = MagicMock()
    waypoint.position = Point(10.0, 20.0, _TERRAIN)

    with patch.object(_PydcsWaypointBuilder, "build", return_value=waypoint):
        builder.build()

    tasks = [call.args[0] for call in waypoint.add_task.call_args_list]
    embarking = [t for t in tasks if isinstance(t, Embarking)]
    assert len(embarking) == 1
    assert embarking[0].params["groupsForEmbarking"] == {4242: 4242}
    # No Land task: the pickup site is unprepared terrain the AI often refuses to
    # set down on, and the embark works from a hover.
    assert not [t for t in tasks if isinstance(t, Land)]


def test_csar_pickup_without_a_pilot_group_adds_no_task() -> None:
    from game.missiongenerator.aircraft.waypoints.csarpickup import CsarPickupBuilder

    downed = _standalone_downed()
    builder = CsarPickupBuilder.__new__(CsarPickupBuilder)
    builder.flight = cast(Any, SimpleNamespace(package=SimpleNamespace(target=downed)))
    builder.mission_data = cast(Any, SimpleNamespace(csar_pilot_groups={}))
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

    mission = Mission(Caucasus())
    downed = _standalone_downed()
    downed._position = Point(-250000.0, 630000.0, mission.terrain)

    coalition = SimpleNamespace(
        player=Player.BLUE,
        downed_pilots=[downed],
        faction=SimpleNamespace(country=SimpleNamespace(name="USA")),
    )
    game = MagicMock()
    game.settings.csar_enabled = True
    game.settings.csar_enabled_red = False
    game.theater.terrain = mission.terrain
    game.coalition_for.return_value = coalition

    mission_data = MissionData()
    CsarGenerator(mission, game, mission_data).generate()

    info = mission_data.csar_pilot_groups[str(downed.id)]
    assert info.blue is True
    group = next(
        g for g in mission.country("USA").vehicle_group if g.name == info.group_name
    )
    assert group.id == info.group_id
    tasks = group.points[0].tasks
    assert [t for t in tasks if isinstance(t, EmbarkToTransport)]
    # The template Ops.CSAR is constructed against must also exist.
    assert mission_data.csar_pilot_templates["blue"] == "CSAR_PILOT_BLUE"


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
            group_name="CSAR Ivan Doe abcd1234", group_id=77, blue=True
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
    assert csar.downedPilots[1].id == str(downed.id)
    assert csar.downedPilots[1].aircraft == "UH-60A"
    # The pilot is already placed in the mission; OpsCSAR.lua hands this group to
    # Ops.CSAR so a player can rescue them.
    assert csar.downedPilots[1].groupName == "CSAR Ivan Doe abcd1234"
    rescue_ids = {
        csar.rescueTypes[i].dcs_id for i in range(1, len(csar.rescueTypes) + 1)
    }
    # Transport helicopters MOOSE ships no default capacity for must still be
    # whitelisted, and fixed-wing must not appear at all.
    assert "CH-47D" in rescue_ids
    assert "Hercules" not in rescue_ids
    assert "C-130J-30" not in rescue_ids
