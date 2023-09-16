import logging
import random
import re
from typing import Any, Tuple

from dcs import Mission
from dcs.country import Country
from dcs.mapping import Vector2, Point
from dcs.terrain import NoParkingSlotError
from dcs.unitgroup import (
    FlyingGroup,
    ShipGroup,
    StaticGroup,
)

from game.ato import Flight
from game.ato.flightstate import InFlight
from game.ato.starttype import StartType
from game.missiongenerator.aircraft.flightgroupspawner import (
    FlightGroupSpawner,
    MINIMUM_MID_MISSION_SPAWN_ALTITUDE_AGL,
    MINIMUM_MID_MISSION_SPAWN_ALTITUDE_MSL,
    STACK_SEPARATION,
)
from game.missiongenerator.missiondata import MissionData
from game.naming import NameGenerator
from game.theater import Airfield, ControlPoint, Fob, NavalControlPoint, OffMapSpawn
from game.utils import feet, meters


class PretenseNameGenerator(NameGenerator):
    @classmethod
    def next_pretense_aircraft_name(cls, cp: ControlPoint, flight: Flight) -> str:
        cls.aircraft_number += 1
        cp_name_trimmed = "".join([i for i in cp.name.lower() if i.isalnum()])
        return "{}-{}-{}".format(
            cp_name_trimmed, str(flight.flight_type).lower(), cls.aircraft_number
        )


namegen = PretenseNameGenerator


class PretenseFlightGroupSpawner(FlightGroupSpawner):
    def __init__(
        self,
        flight: Flight,
        country: Country,
        mission: Mission,
        helipads: dict[ControlPoint, list[StaticGroup]],
        ground_spawns_roadbase: dict[ControlPoint, list[Tuple[StaticGroup, Point]]],
        ground_spawns: dict[ControlPoint, list[Tuple[StaticGroup, Point]]],
        mission_data: MissionData,
    ) -> None:
        super().__init__(
            flight,
            country,
            mission,
            helipads,
            ground_spawns_roadbase,
            ground_spawns,
            mission_data,
        )

        self.flight = flight
        self.country = country
        self.mission = mission
        self.helipads = helipads
        self.ground_spawns_roadbase = ground_spawns_roadbase
        self.ground_spawns = ground_spawns
        self.mission_data = mission_data

    def generate_flight_at_departure(self) -> FlyingGroup[Any]:
        cp = self.flight.departure
        name = namegen.next_pretense_aircraft_name(cp, self.flight)
        cp_side = 2 if cp.captured else 1
        cp_name_trimmed = "".join([i for i in cp.name.lower() if i.isalnum()])
        flight_type = self.flight.flight_type.name
        if cp_name_trimmed not in self.flight.coalition.game.pretense_air[cp_side]:
            self.flight.coalition.game.pretense_air[cp_side][cp_name_trimmed] = {}
        if (
            flight_type
            not in self.flight.coalition.game.pretense_air[cp_side][cp_name_trimmed]
        ):
            self.flight.coalition.game.pretense_air[cp_side][cp_name_trimmed][
                flight_type
            ] = list()

        try:
            if self.start_type is StartType.IN_FLIGHT:
                self.flight.coalition.game.pretense_air[cp_side][cp_name_trimmed][
                    self.flight.flight_type.name
                ].append(name)
                group = self._generate_over_departure(name, cp)
                return group
            elif isinstance(cp, NavalControlPoint):
                group_name = cp.get_carrier_group_name()
                carrier_group = self.mission.find_group(group_name)
                if not isinstance(carrier_group, ShipGroup):
                    raise RuntimeError(
                        f"Carrier group {carrier_group} is a "
                        f"{carrier_group.__class__.__name__}, expected a ShipGroup"
                    )
                self.flight.coalition.game.pretense_air[cp_side][cp_name_trimmed][
                    self.flight.flight_type.name
                ].append(name)
                return self._generate_at_group(name, carrier_group)
            elif isinstance(cp, Fob):
                is_heli = self.flight.squadron.aircraft.helicopter
                is_vtol = not is_heli and self.flight.squadron.aircraft.lha_capable
                if not is_heli and not is_vtol and not cp.has_ground_spawns:
                    raise RuntimeError(
                        f"Cannot spawn fixed-wing aircraft at {cp} because of insufficient ground spawn slots."
                    )
                pilot_count = len(self.flight.roster.pilots)
                if (
                    not is_heli
                    and self.flight.roster.player_count != pilot_count
                    and not self.flight.coalition.game.settings.ground_start_ai_planes
                ):
                    raise RuntimeError(
                        f"Fixed-wing aircraft at {cp} must be piloted by humans exclusively because"
                        f' the "AI fixed-wing aircraft can use roadbases / bases with only ground'
                        f' spawns" setting is currently disabled.'
                    )
                if cp.has_helipads and (is_heli or is_vtol):
                    pad_group = self._generate_at_cp_helipad(name, cp)
                    if pad_group is not None:
                        return pad_group
                if cp.has_ground_spawns and (self.flight.client_count > 0 or is_heli):
                    pad_group = self._generate_at_cp_ground_spawn(name, cp)
                    if pad_group is not None:
                        return pad_group
                self.flight.coalition.game.pretense_air[cp_side][cp_name_trimmed][
                    self.flight.flight_type.name
                ].append(name)
                return self._generate_over_departure(name, cp)
            elif isinstance(cp, Airfield):
                is_heli = self.flight.squadron.aircraft.helicopter
                if cp.has_helipads and is_heli:
                    pad_group = self._generate_at_cp_helipad(name, cp)
                    if pad_group is not None:
                        return pad_group
                if (
                    cp.has_ground_spawns
                    and len(self.ground_spawns[cp])
                    + len(self.ground_spawns_roadbase[cp])
                    >= self.flight.count
                    and (self.flight.client_count > 0 or is_heli)
                ):
                    pad_group = self._generate_at_cp_ground_spawn(name, cp)
                    if pad_group is not None:
                        return pad_group
                self.flight.coalition.game.pretense_air[cp_side][cp_name_trimmed][
                    self.flight.flight_type.name
                ].append(name)
                return self._generate_at_airfield(name, cp)
            else:
                raise NotImplementedError(
                    f"Aircraft spawn behavior not implemented for {cp} ({cp.__class__})"
                )
        except NoParkingSlotError:
            # Generated when there is no place on Runway or on Parking Slots
            logging.warning(
                "No room on runway or parking slots. Starting from the air."
            )
            self.flight.start_type = StartType.IN_FLIGHT
            group = self._generate_over_departure(name, cp)
            return group

    def generate_mid_mission(self) -> FlyingGroup[Any]:
        assert isinstance(self.flight.state, InFlight)
        name = namegen.next_pretense_aircraft_name(self.flight.departure, self.flight)
        speed = self.flight.state.estimate_speed()
        pos = self.flight.state.estimate_position()
        pos += Vector2(random.randint(100, 1000), random.randint(100, 1000))
        alt, alt_type = self.flight.state.estimate_altitude()
        cp = self.flight.squadron.location.id

        if cp not in self.mission_data.cp_stack:
            self.mission_data.cp_stack[cp] = MINIMUM_MID_MISSION_SPAWN_ALTITUDE_AGL

        # We don't know where the ground is, so just make sure that any aircraft
        # spawning at an MSL altitude is spawned at some minimum altitude.
        # https://github.com/dcs-liberation/dcs_liberation/issues/1941
        if alt_type == "BARO" and alt < MINIMUM_MID_MISSION_SPAWN_ALTITUDE_MSL:
            alt = MINIMUM_MID_MISSION_SPAWN_ALTITUDE_MSL

        # Set a minimum AGL value for 'alt' if needed,
        # otherwise planes might crash in trees and stuff.
        if alt_type == "RADIO" and alt < self.mission_data.cp_stack[cp]:
            alt = self.mission_data.cp_stack[cp]
            self.mission_data.cp_stack[cp] += STACK_SEPARATION

        group = self.mission.flight_group(
            country=self.country,
            name=name,
            aircraft_type=self.flight.unit_type.dcs_unit_type,
            airport=None,
            position=pos,
            altitude=alt.meters,
            speed=speed.kph,
            maintask=None,
            group_size=self.flight.count,
        )

        group.points[0].alt_type = alt_type
        return group
