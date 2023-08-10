from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Optional, TYPE_CHECKING

from dcs import Mission
from dcs.action import DoScript
from dcs.flyingunit import FlyingUnit
from dcs.task import OptReactOnThreat
from dcs.translation import String
from dcs.triggers import TriggerStart
from dcs.unit import Skill
from dcs.unitgroup import FlyingGroup

from game.ato import Flight, FlightType
from game.callsigns import callsign_for_support_unit
from game.data.weapons import Pylon, WeaponType
from game.missiongenerator.logisticsgenerator import LogisticsGenerator
from game.missiongenerator.missiondata import MissionData, AwacsInfo, TankerInfo
from game.radio.radios import RadioFrequency, RadioRegistry
from game.radio.tacan import TacanBand, TacanRegistry, TacanUsage
from game.runways import RunwayData
from game.squadrons import Pilot
from .aircraftbehavior import AircraftBehavior
from .aircraftpainter import AircraftPainter
from .flightdata import FlightData
from .waypoints import WaypointGenerator
from ...ato.flightmember import FlightMember
from ...ato.flightplans.aewc import AewcFlightPlan
from ...ato.flightplans.packagerefueling import PackageRefuelingFlightPlan
from ...ato.flightplans.theaterrefueling import TheaterRefuelingFlightPlan
from ...theater import Fob

if TYPE_CHECKING:
    from game import Game


class FlightGroupConfigurator:
    def __init__(
        self,
        flight: Flight,
        group: FlyingGroup[Any],
        game: Game,
        mission: Mission,
        time: datetime,
        radio_registry: RadioRegistry,
        tacan_registry: TacanRegistry,
        mission_data: MissionData,
        dynamic_runways: dict[str, RunwayData],
        use_client: bool,
    ) -> None:
        self.flight = flight
        self.group = group
        self.game = game
        self.mission = mission
        self.time = time
        self.radio_registry = radio_registry
        self.tacan_registry = tacan_registry
        self.mission_data = mission_data
        self.dynamic_runways = dynamic_runways
        self.use_client = use_client

    def configure(self) -> FlightData:
        AircraftBehavior(self.flight.flight_type).apply_to(self.flight, self.group)
        AircraftPainter(self.flight, self.group).apply_livery()
        self.setup_props()
        self.setup_payloads()
        self.setup_fuel()
        flight_channel = self.setup_radios()

        laser_codes: list[Optional[int]] = []
        for unit, member in zip(self.group.units, self.flight.iter_members()):
            self.configure_flight_member(unit, member, laser_codes)

        divert = None
        if self.flight.divert is not None:
            divert = self.flight.divert.active_runway(
                self.game.theater, self.game.conditions, self.dynamic_runways
            )

        if self.flight.flight_type in [
            FlightType.TRANSPORT,
            FlightType.AIR_ASSAULT,
        ] and self.game.settings.plugin_option("ctld"):
            transfer = None
            if self.flight.flight_type == FlightType.TRANSPORT:
                coalition = self.game.coalition_for(player=self.flight.blue)
                transfer = coalition.transfers.transfer_for_flight(self.flight)
            self.mission_data.logistics.append(
                LogisticsGenerator(
                    self.flight, self.group, self.mission, self.game.settings, transfer
                ).generate_logistics()
            )

        mission_start_time, waypoints = WaypointGenerator(
            self.flight,
            self.group,
            self.mission,
            self.game.conditions.start_time,
            self.time,
            self.game.settings,
            self.mission_data,
        ).create_waypoints()

        # Special handling for landing waypoints when:
        # 1. It's an AI-only flight
        # 2. Aircraft are not helicopters/VTOL
        # 3. Landing waypoint does not point to an airfield
        if (
            self.flight.client_count < 1
            and not self.flight.unit_type.helicopter
            and not self.flight.unit_type.lha_capable
            and isinstance(self.flight.squadron.location, Fob)
        ):
            # Need to set uncontrolled to false, otherwise the AI will skip the mission and just land
            self.group.uncontrolled = False

        return FlightData(
            package=self.flight.package,
            aircraft_type=self.flight.unit_type,
            squadron=self.flight.squadron,
            flight_type=self.flight.flight_type,
            units=self.group.units,
            size=len(self.group.units),
            friendly=self.flight.departure.captured,
            departure_delay=mission_start_time,
            departure=self.flight.departure.active_runway(
                self.game.theater, self.game.conditions, self.dynamic_runways
            ),
            arrival=self.flight.arrival.active_runway(
                self.game.theater, self.game.conditions, self.dynamic_runways
            ),
            divert=divert,
            waypoints=waypoints,
            intra_flight_channel=flight_channel,
            bingo_fuel=self.flight.flight_plan.bingo_fuel,
            joker_fuel=self.flight.flight_plan.joker_fuel,
            custom_name=self.flight.custom_name,
            laser_codes=laser_codes,
        )

    def configure_flight_member(
        self, unit: FlyingUnit, member: FlightMember, laser_codes: list[Optional[int]]
    ) -> None:
        self.set_skill(unit, member)
        if (code := member.tgp_laser_code) is not None:
            laser_codes.append(code.code)
        else:
            laser_codes.append(None)
        settings = self.flight.coalition.game.settings
        if not member.is_player or not settings.plugins.get("ewrj"):
            return
        jammer_required = settings.plugin_option("ewrj.ecm_required")
        if jammer_required:
            ecm = WeaponType.JAMMER
            if not member.loadout.has_weapon_of_type(ecm):
                return
        ewrj_menu_trigger = TriggerStart(comment=f"EWRJ-{unit.name}")
        ewrj_menu_trigger.add_action(DoScript(String(f'EWJamming("{unit.name}")')))
        self.mission.triggerrules.triggers.append(ewrj_menu_trigger)
        self.group.points[0].tasks[0] = OptReactOnThreat(
            OptReactOnThreat.Values.PassiveDefense
        )

    def setup_radios(self) -> RadioFrequency:
        freq = self.flight.frequency
        if freq is None and (freq := self.flight.package.frequency) is None:
            freq = self.radio_registry.alloc_uhf()
            self.flight.package.frequency = freq
        if freq not in self.radio_registry.allocated_channels:
            self.radio_registry.reserve(freq)

        if self.flight.flight_type in {FlightType.AEWC, FlightType.REFUELING}:
            self.register_air_support(freq)
        elif self.flight.client_count and self.flight.squadron.radio_presets:
            freq = self.flight.squadron.radio_presets["intra_flight"][0]
        elif self.flight.frequency is None and self.flight.client_count:
            freq = self.flight.unit_type.alloc_flight_radio(self.radio_registry)

        self.group.set_frequency(freq.mhz)
        return freq

    def register_air_support(self, channel: RadioFrequency) -> None:
        callsign = callsign_for_support_unit(self.group)
        if isinstance(self.flight.flight_plan, AewcFlightPlan):
            self.mission_data.awacs.append(
                AwacsInfo(
                    group_name=str(self.group.name),
                    callsign=callsign,
                    freq=channel,
                    depature_location=self.flight.departure.name,
                    start_time=self.flight.flight_plan.patrol_start_time,
                    end_time=self.flight.flight_plan.patrol_end_time,
                    blue=self.flight.departure.captured,
                )
            )
        elif isinstance(
            self.flight.flight_plan, TheaterRefuelingFlightPlan
        ) or isinstance(self.flight.flight_plan, PackageRefuelingFlightPlan):
            tacan = self.flight.tacan
            if tacan is None and self.flight.squadron.aircraft.dcs_unit_type.tacan:
                tacan = self.tacan_registry.alloc_for_band(
                    TacanBand.Y, TacanUsage.AirToAir
                )
            else:
                tacan = self.flight.tacan
            self.mission_data.tankers.append(
                TankerInfo(
                    group_name=str(self.group.name),
                    callsign=callsign,
                    variant=self.flight.unit_type.display_name,
                    freq=channel,
                    tacan=tacan,
                    start_time=self.flight.flight_plan.patrol_start_time,
                    end_time=self.flight.flight_plan.patrol_end_time,
                    blue=self.flight.departure.captured,
                )
            )

    def set_skill(self, unit: FlyingUnit, member: FlightMember) -> None:
        if not member.is_player:
            unit.skill = self.skill_level_for(unit, member.pilot)
            return

        if self.use_client or "Pilot #1" not in unit.name:
            unit.set_client()
        else:
            unit.set_player()

    def skill_level_for(self, unit: FlyingUnit, pilot: Optional[Pilot]) -> Skill:
        if self.flight.squadron.player:
            base_skill = Skill(self.game.settings.player_skill)
        else:
            base_skill = Skill(self.game.settings.enemy_skill)

        if pilot is None:
            logging.error(f"Cannot determine skill level: {unit.name} has not pilot")
            return base_skill

        levels = [
            Skill.Average,
            Skill.Good,
            Skill.High,
            Skill.Excellent,
        ]
        current_level = levels.index(base_skill)
        missions_for_skill_increase = 4
        increase = pilot.record.missions_flown // missions_for_skill_increase
        capped_increase = min(current_level + increase, len(levels) - 1)

        if self.game.settings.ai_pilot_levelling:
            new_level = capped_increase
        else:
            new_level = current_level

        return levels[new_level]

    def setup_props(self) -> None:
        for unit, member in zip(self.group.units, self.flight.iter_members()):
            props = dict(member.properties)
            if (code := member.weapon_laser_code) is not None:
                for laser_code_config in self.flight.unit_type.laser_code_configs:
                    props.update(laser_code_config.property_dict_for_code(code.code))
            for prop_id, value in props.items():
                unit.set_property(prop_id, value)

    def setup_payloads(self) -> None:
        for unit, member in zip(self.group.units, self.flight.iter_members()):
            self.setup_payload(unit, member)

    def setup_payload(self, unit: FlyingUnit, member: FlightMember) -> None:
        unit.pylons.clear()

        loadout = member.loadout
        if self.game.settings.restrict_weapons_by_date:
            loadout = loadout.degrade_for_date(self.flight.unit_type, self.game.date)

        for pylon_number, weapon in loadout.pylons.items():
            if weapon is None:
                continue
            pylon = Pylon.for_aircraft(self.flight.unit_type, pylon_number)
            pylon.equip(unit, weapon)

    def setup_fuel(self) -> None:
        fuel = self.flight.state.estimate_fuel()
        if fuel < 0:
            logging.warning(
                f"Flight {self.flight} is estimated to have no fuel at mission start. "
                "This estimate does not account for external fuel tanks. Setting "
                "starting fuel to 100kg."
            )
            fuel = 100
        for unit, pilot in zip(self.group.units, self.flight.roster.iter_pilots()):
            if pilot is not None and pilot.player:
                unit.fuel = fuel
            else:
                unit.fuel = self.flight.fuel
