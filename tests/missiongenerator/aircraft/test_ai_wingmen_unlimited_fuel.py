"""Regressions for AI wingman unlimited fuel in player-led flights.

When ``ai_unlimited_fuel`` is enabled, the AI wingmen of ordinary player-led
flights keep unlimited fuel for the whole mission: the startup waypoint carries
``SetUnlimitedFuelCommand(True)`` regardless of spawn state (cold start, air
start at the IP, combat, or late activation) and no waypoint builder disables
it at JOIN or racetrack start. Autonomous all-AI flights keep the existing
phase-based rules: unlimited fuel at startup (unless spawned at the IP or in
combat), removed at join/racetrack start, reapplied at split/racetrack end.
With the setting disabled, no fuel commands are generated for any flight.

The EW jamming configuration for player flights must replace the existing
threat reaction in place instead of overwriting the first waypoint task, which
would silently drop the startup fuel command.

DCS applies ``SetUnlimitedFuel`` to AI units only, so all-human flights are
unaffected in game; whether a human pilot stays fuel-normal is a runtime
acceptance question these tests cannot answer.

The tests drive the real ``AircraftBehavior`` + ``WaypointGenerator`` pair over
genuine pydcs waypoints/groups/missions (with a minimal concrete
``PatrollingFlightPlan`` and ``FormationAttackLayout``), so assertions read the
generated task objects and their serialized forms rather than mock call logs.
"""

from datetime import datetime, timedelta
from typing import Any
from unittest.mock import MagicMock

from dcs import Mission, Point
from dcs.point import MovingPoint
from dcs.task import (
    OptReactOnThreat,
    OptRTBOnBingoFuel,
    OptVerticalTakeoffLanding,
    SetUnlimitedFuelCommand,
    Task,
)
from dcs.terrain import Caucasus
from dcs.unitgroup import FlyingGroup

from game.ato import FlightType
from game.ato.flightplans.formationattack import FormationAttackLayout
from game.ato.flightplans.patrolling import (
    PatrollingFlightPlan,
    PatrollingLayout,
)
from game.ato.flightstate import InFlight, WaitingForStart
from game.ato.flightwaypoint import FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.ato.starttype import StartType
from game.missiongenerator.aircraft.aircraftbehavior import AircraftBehavior
from game.missiongenerator.aircraft.flightgroupconfigurator import (
    FlightGroupConfigurator,
)
from game.missiongenerator.aircraft.waypoints.waypointgenerator import (
    WaypointGenerator,
)
from game.utils import feet, knots, nautical_miles

NOW = datetime(2024, 5, 1, 9)
PATROL_START_TIME = NOW + timedelta(minutes=30)
PATROL_DURATION = timedelta(minutes=30)


def _terrain() -> Caucasus:
    return Caucasus()


def _wp(name: str, wtype: FlightWaypointType, x: float, y: float) -> FlightWaypoint:
    return FlightWaypoint(name, wtype, Point(x, y, _terrain()))


def _flight(
    *,
    unlimited_fuel: bool = True,
    client_count: int = 0,
    is_helo: bool = False,
    vtol_option: bool = False,
    at_ip: bool = False,
    in_combat: bool = False,
) -> Any:
    flight = MagicMock()
    flight.flight_type = FlightType.TARCAP
    flight.client_count = client_count
    flight.is_helo = is_helo
    for coalition in (flight.squadron.coalition, flight.coalition):
        settings = coalition.game.settings
        settings.ai_unlimited_fuel = unlimited_fuel
        settings.ai_vertical_takoff_landing = vtol_option
        settings.ai_jettison_empty_tanks = False
        settings.silence_ai_radios = False
        settings.limit_ai_radios = False
        settings.never_delay_player_flights = False
        settings.plugins = {}
        coalition.doctrine.rtb_speed = knots(300)
        coalition.doctrine.escort_engagement_range = nautical_miles(10)
        coalition.doctrine.escort_spacing = feet(3000)
    flight.state.is_at_ip = at_ip
    flight.state.in_combat = in_combat
    flight.unit_type.max_speed = knots(500)
    flight.unit_type.fuel_consumption = None
    flight.start_type = StartType.WARM
    flight.departure.is_fleet = False
    flight.departure.dcs_airport = None
    return flight


class _FakePatrolPlan(PatrollingFlightPlan[PatrollingLayout]):
    """Minimal concrete PatrollingFlightPlan for the builder valid paths."""

    def __init__(self, tot: datetime) -> None:
        self._tot = tot
        # FlightPlan.__init__ normally binds the flight; nothing in the
        # generation paths exercised here reads it, but the attribute is
        # provided so stricter trees can use the fixture unchanged.
        self.flight = _flight()

    @property
    def tot(self) -> datetime:
        return self._tot

    @property
    def patrol_duration(self) -> timedelta:
        return PATROL_DURATION

    @property
    def patrol_speed(self) -> Any:
        return knots(300)

    @property
    def engagement_distance(self) -> Any:
        return nautical_miles(10)

    def takeoff_time(self) -> datetime:
        return self._tot


def _patrol_plan(
    patrol_start: FlightWaypoint, patrol_end: FlightWaypoint
) -> _FakePatrolPlan:
    plan = _FakePatrolPlan(PATROL_START_TIME)
    plan.layout = PatrollingLayout(
        departure=_wp("DEP", FlightWaypointType.TAKEOFF, 0, 0),
        custom_waypoints=[],
        arrival=_wp("ARR", FlightWaypointType.LANDING_POINT, 900, 0),
        divert=None,
        bullseye=_wp("BULL", FlightWaypointType.BULLSEYE, 1500, 0),
        nav_to=[],
        nav_from=[],
        patrol_start=patrol_start,
        patrol_end=patrol_end,
    )
    return plan


def _mock_plan(waypoints: list[FlightWaypoint]) -> Any:
    plan = MagicMock()
    plan.waypoints = waypoints
    plan.takeoff_time.return_value = NOW
    plan.tot_for_waypoint.return_value = None
    return plan


def _configured_group(flight: Any) -> FlyingGroup[Any]:
    group: FlyingGroup[Any] = FlyingGroup(1, name="TestGroup")
    spawn = MovingPoint(Point(0, 0, _terrain()))
    spawn.name = "SPAWN"
    group.points.append(spawn)
    AircraftBehavior(flight.flight_type, MagicMock()).configure_behavior(flight, group)
    return group


def _generated(
    flight: Any, plan: Any, points: list[FlightWaypoint]
) -> FlyingGroup[Any]:
    flight.flight_plan = plan
    flight.points = points
    group = _configured_group(flight)
    mission = Mission(_terrain())
    WaypointGenerator(
        flight,
        group,
        mission,
        NOW,
        flight.coalition.game.settings,
        MagicMock(),
    ).create_waypoints()
    return group


def _full_mission_points() -> tuple[Any, list[FlightWaypoint]]:
    """DEP -> JOIN -> racetrack -> SPLIT -> ARR, as a patrol flight plan."""
    join = _wp("JOIN", FlightWaypointType.JOIN, 100, 0)
    patrol_start = _wp("RACETRACK START", FlightWaypointType.PATROL_TRACK, 500, 0)
    patrol_end = _wp("RACETRACK END", FlightWaypointType.PATROL, 700, 0)
    split = _wp("SPLIT", FlightWaypointType.SPLIT, 800, 0)
    arrival = _wp("ARR", FlightWaypointType.LANDING_POINT, 900, 0)
    plan = _patrol_plan(patrol_start, patrol_end)
    return plan, [join, patrol_start, patrol_end, split, arrival]


def _fuel_values(tasks: list[Any]) -> list[bool]:
    return [
        bool(task.params["action"]["params"]["value"])
        for task in tasks
        if isinstance(task, SetUnlimitedFuelCommand)
    ]


def _fuel_values_on_point(group: FlyingGroup[Any], name: str) -> list[bool]:
    for point in group.points:
        if point.name == name:
            return _fuel_values(point.tasks)
    raise AssertionError(f"No generated waypoint named {name}")


def _all_fuel_values(group: FlyingGroup[Any]) -> list[bool]:
    return [value for point in group.points for value in _fuel_values(point.tasks)]


# Startup: the fuel command on the spawn waypoint.


def test_player_flight_gets_startup_unlimited_fuel() -> None:
    group = _configured_group(_flight(client_count=1))
    assert _fuel_values(group.points[0].tasks) == [True]


def test_player_flight_gets_startup_unlimited_fuel_at_ip_spawn() -> None:
    group = _configured_group(_flight(client_count=1, at_ip=True))
    assert _fuel_values(group.points[0].tasks) == [True]


def test_player_flight_gets_startup_unlimited_fuel_in_combat_spawn() -> None:
    group = _configured_group(_flight(client_count=1, in_combat=True))
    assert _fuel_values(group.points[0].tasks) == [True]


def test_player_flight_at_ip_keeps_orientation_waypoint_and_fuel() -> None:
    flight = _flight(client_count=1, at_ip=True)
    join = _wp("JOIN", FlightWaypointType.JOIN, 100, 0)
    target = _wp("TARGET", FlightWaypointType.TARGET_POINT, 2000, 0)
    flight.flight_plan.layout = FormationAttackLayout(
        departure=_wp("DEP", FlightWaypointType.TAKEOFF, 0, 0),
        custom_waypoints=[],
        arrival=_wp("ARR", FlightWaypointType.LANDING_POINT, 3000, 0),
        divert=None,
        bullseye=_wp("BULL", FlightWaypointType.BULLSEYE, 1500, 0),
        nav_to=[],
        nav_from=[],
        hold=None,
        join=join,
        split=_wp("SPLIT", FlightWaypointType.SPLIT, 2500, 0),
        refuel=None,
        ingress=_wp("INGRESS", FlightWaypointType.INGRESS_STRIKE, 1800, 0),
        targets=[target],
    )
    group = _configured_group(flight)
    # The IP orientation waypoint is inserted before the fuel command is
    # appended; the orientation behavior and the fuel command coexist.
    assert group.points[1].name == "Orientation WPT"
    assert _fuel_values(group.points[0].tasks) == [True]


def test_all_ai_flight_gets_startup_unlimited_fuel_ground_spawn() -> None:
    group = _configured_group(_flight())
    assert _fuel_values(group.points[0].tasks) == [True]


def test_all_ai_flight_gets_no_startup_fuel_at_ip_spawn() -> None:
    # Existing upstream rule retained: autonomous flights spawned at the IP
    # do not get startup unlimited fuel.
    group = _configured_group(_flight(at_ip=True))
    assert _fuel_values(group.points[0].tasks) == []


# Phase behavior: full mission profiles through the real waypoint builders.


def test_player_flight_full_profile_has_no_fuel_disable() -> None:
    plan, points = _full_mission_points()
    group = _generated(_flight(client_count=1), plan, points)
    assert _fuel_values_on_point(group, "SPAWN") == [True]
    assert _fuel_values_on_point(group, "JOIN") == []
    assert _fuel_values_on_point(group, "RACETRACK START") == []
    # The split/racetrack-end re-enable is harmless for player flights: fuel
    # was never disabled, so re-enabling is a no-op.
    assert _fuel_values_on_point(group, "RACETRACK END") == [True]
    assert _fuel_values_on_point(group, "SPLIT") == [True]


def test_all_ai_flight_full_profile_keeps_phase_rules() -> None:
    plan, points = _full_mission_points()
    group = _generated(_flight(), plan, points)
    # Existing upstream rules retained: enable at startup, disable at join and
    # racetrack start, re-enable at racetrack end and split.
    assert _fuel_values_on_point(group, "SPAWN") == [True]
    assert _fuel_values_on_point(group, "JOIN") == [False]
    assert _fuel_values_on_point(group, "RACETRACK START") == [False]
    assert _fuel_values_on_point(group, "RACETRACK END") == [True]
    assert _fuel_values_on_point(group, "SPLIT") == [True]


def test_all_human_flight_full_profile_has_no_fuel_disable() -> None:
    # The gate is keyed on the flight having players, not on AI members being
    # present: all-human flights take the same no-disable path.
    plan, points = _full_mission_points()
    group = _generated(_flight(client_count=2), plan, points)
    assert _all_fuel_values(group) == [True, True, True]


def test_disabled_setting_generates_no_fuel_commands() -> None:
    for client_count in (0, 1):
        plan, points = _full_mission_points()
        group = _generated(
            _flight(unlimited_fuel=False, client_count=client_count), plan, points
        )
        assert _all_fuel_values(group) == []


# Spawn states.


def test_late_activation_player_flight_keeps_startup_fuel() -> None:
    plan, points = _full_mission_points()
    flight = _flight(client_count=1)
    flight.start_type = StartType.WARM
    state = MagicMock(spec=WaitingForStart)
    state.in_flight = False
    state.time_remaining.return_value = timedelta(minutes=30)
    flight.state = state
    flight.flight_plan = plan
    flight.points = points

    group = _configured_group(flight)
    mission = Mission(_terrain())
    WaypointGenerator(
        flight,
        group,
        mission,
        NOW,
        flight.coalition.game.settings,
        MagicMock(),
    ).create_waypoints()

    assert group.late_activation is True
    assert _fuel_values(group.points[0].tasks) == [True]


def test_all_ai_escort_join_restoration_disables_fuel_mid_flight() -> None:
    # Existing rule retained: an autonomous escort restored at its JOIN keeps
    # the join disable, replacing the startup enable on the spawn waypoint.
    join = _wp("JOIN", FlightWaypointType.JOIN, 100, 0)
    split = _wp("SPLIT", FlightWaypointType.SPLIT, 200, 0)
    arrival = _wp("ARR", FlightWaypointType.LANDING_POINT, 900, 0)
    departure = _wp("DEP", FlightWaypointType.TAKEOFF, 0, 0)
    plan = _mock_plan([departure, join, split, arrival])
    flight = _flight()
    flight.flight_type = FlightType.ESCORT
    state = MagicMock(spec=InFlight)
    state.in_flight = True
    state.is_at_ip = False
    state.in_combat = False
    state.current_waypoint = join
    state.has_passed_waypoint.side_effect = lambda point: point in []
    flight.state = state

    group = _generated(flight, plan, [join, split, arrival])

    assert _fuel_values(group.points[0].tasks) == [False]


def test_player_escort_join_restoration_keeps_fuel_mid_flight() -> None:
    join = _wp("JOIN", FlightWaypointType.JOIN, 100, 0)
    split = _wp("SPLIT", FlightWaypointType.SPLIT, 200, 0)
    arrival = _wp("ARR", FlightWaypointType.LANDING_POINT, 900, 0)
    departure = _wp("DEP", FlightWaypointType.TAKEOFF, 0, 0)
    plan = _mock_plan([departure, join, split, arrival])
    flight = _flight(client_count=1)
    flight.flight_type = FlightType.ESCORT
    state = MagicMock(spec=InFlight)
    state.in_flight = True
    state.is_at_ip = False
    state.in_combat = False
    state.current_waypoint = join
    state.has_passed_waypoint.side_effect = lambda point: point in []
    flight.state = state

    group = _generated(flight, plan, [join, split, arrival])

    assert _fuel_values(group.points[0].tasks) == [True]


# Airframe option interaction and EW jamming.


def test_player_helo_keeps_vtol_option_with_unlimited_fuel() -> None:
    flight = _flight(client_count=1, is_helo=True, vtol_option=True)
    group = _configured_group(flight)
    assert _fuel_values(group.points[0].tasks) == [True]
    assert any(
        isinstance(task, OptVerticalTakeoffLanding) for task in group.points[0].tasks
    )


def test_ew_jamming_preserves_startup_fuel_and_nonfuel_tasks() -> None:
    flight = _flight(client_count=1)
    flight.flight_type = FlightType.TARCAP
    settings = flight.coalition.game.settings
    settings.plugin_option.side_effect = lambda key: key == "ewrj"
    aircraft = flight.squadron.aircraft
    aircraft.has_built_in_ecm = False
    aircraft.has_built_in_jamming = False
    member = MagicMock()
    member.is_player = True
    member.loadout.has_weapon_of_type.return_value = False

    group = _configured_group(flight)
    configurator = object.__new__(FlightGroupConfigurator)
    configurator.flight = flight
    configurator.group = group
    configurator.mission = MagicMock()
    configurator.handle_ew_jamming(member, MagicMock(name="Pilot 1"))

    tasks: list[Task] = group.points[0].tasks
    # The startup fuel command survives the EW threat-reaction update.
    assert _fuel_values(tasks) == [True]
    threat_reactions = [task for task in tasks if isinstance(task, OptReactOnThreat)]
    assert len(threat_reactions) == 1
    assert (
        threat_reactions[0].params["action"]["params"]["value"]
        == OptReactOnThreat.Values.PassiveDefense
    )
    # Non-fuel options configured before the EW update are untouched.
    assert any(isinstance(task, OptRTBOnBingoFuel) for task in tasks)
