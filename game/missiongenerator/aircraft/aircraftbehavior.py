import logging
from typing import Any, Optional, Type, List

from dcs.point import MovingPoint
from dcs.task import (
    AWACS,
    AWACSTaskAction,
    AntishipStrike,
    CAP,
    CAS,
    EPLRS,
    Escort,
    FighterSweep,
    GroundAttack,
    Nothing,
    OptROE,
    OptRTBOnBingoFuel,
    OptRTBOnOutOfAmmo,
    OptReactOnThreat,
    OptRestrictJettison,
    Refueling,
    RunwayAttack,
    Transport,
    SEAD,
    OptJettisonEmptyTanks,
    MainTask,
    PinpointStrike,
    AFAC,
    SetUnlimitedFuelCommand,
    OptNoReportWaypointPass,
    OptRadioUsageContact,
    OptRadioSilence,
    Tanker,
    RecoveryTanker,
    ActivateBeaconCommand,
    ControlledTask,
)
from dcs.unitgroup import FlyingGroup, ShipGroup

from game.ato import Flight, FlightType, Package
from game.ato.flightplans.aewc import AewcFlightPlan
from game.ato.flightplans.formationattack import FormationAttackLayout
from game.ato.flightplans.packagerefueling import PackageRefuelingFlightPlan
from game.ato.flightplans.shiprecoverytanker import RecoveryTankerFlightPlan
from game.ato.flightplans.theaterrefueling import TheaterRefuelingFlightPlan
from game.missiongenerator.missiondata import MissionData
from game.utils import nautical_miles, knots, feet


class AircraftBehavior:
    def __init__(self, task: FlightType, mission_data: MissionData) -> None:
        self.task = task
        self.mission_data = mission_data

    def apply_to(
        self,
        flight: Flight,
        group: FlyingGroup[Any],
    ) -> None:
        if self.task in [
            FlightType.BARCAP,
            FlightType.TARCAP,
            FlightType.INTERCEPTION,
        ]:
            self.configure_cap(group, flight)
        elif self.task == FlightType.SWEEP:
            self.configure_sweep(group, flight)
        elif self.task == FlightType.AEWC:
            self.configure_awacs(group, flight)
        elif self.task == FlightType.REFUELING:
            self.configure_refueling(group, flight)
        elif self.task == FlightType.RECOVERY:
            self.configure_recovery(group, flight)
        elif self.task in [FlightType.CAS, FlightType.BAI]:
            self.configure_cas(group, flight)
        elif self.task == FlightType.ARMED_RECON:
            self.configure_armed_recon(group, flight)
        elif self.task == FlightType.DEAD:
            self.configure_dead(group, flight)
        elif self.task in [FlightType.SEAD, FlightType.SEAD_SWEEP]:
            self.configure_sead(group, flight)
        elif self.task == FlightType.SEAD_ESCORT:
            self.configure_sead_escort(group, flight)
        elif self.task == FlightType.STRIKE:
            self.configure_strike(group, flight)
        elif self.task == FlightType.ANTISHIP:
            self.configure_anti_ship(group, flight)
        elif self.task == FlightType.ESCORT:
            self.configure_escort(group, flight)
        elif self.task == FlightType.OCA_RUNWAY:
            self.configure_runway_attack(group, flight)
        elif self.task == FlightType.OCA_AIRCRAFT:
            self.configure_oca_strike(group, flight)
        elif self.task in [
            FlightType.TRANSPORT,
            FlightType.AIR_ASSAULT,
        ]:
            self.configure_transport(group, flight)
        elif self.task == FlightType.FERRY:
            self.configure_ferry(group, flight)
        else:
            self.configure_unknown_task(group, flight)

        self.configure_eplrs(group, flight)

    def configure_behavior(
        self,
        flight: Flight,
        group: FlyingGroup[Any],
        react_on_threat: OptReactOnThreat.Values = OptReactOnThreat.Values.EvadeFire,
        roe: Optional[int] = None,
        rtb_winchester: Optional[OptRTBOnOutOfAmmo.Values] = None,
        restrict_jettison: Optional[bool] = None,
        mission_uses_gun: bool = True,
        rtb_on_bingo: bool = True,
        ai_unlimited_fuel: Optional[bool] = None,
    ) -> None:
        group.points[0].tasks.clear()
        if ai_unlimited_fuel is None:
            ai_unlimited_fuel = (
                flight.squadron.coalition.game.settings.ai_unlimited_fuel
            )

        # at IP, insert waypoint to orient aircraft in correct direction
        layout = flight.flight_plan.layout
        at_ip_or_combat = flight.state.is_at_ip or flight.state.in_combat
        if at_ip_or_combat and isinstance(layout, FormationAttackLayout):
            a = group.points[0].position
            b = layout.targets[0].position
            pos = a.point_from_heading(
                a.heading_between_point(b), nautical_miles(1).meters
            )
            point = MovingPoint(pos)
            point.alt = group.points[0].alt
            point.alt_type = group.points[0].alt_type
            point.ETA_locked = False
            point.speed = group.points[0].speed
            point.name = "Orientation WPT"
            group.points.insert(1, point)

        # Activate AI unlimited fuel for all flights at startup
        if ai_unlimited_fuel and not at_ip_or_combat:
            group.points[0].tasks.append(SetUnlimitedFuelCommand(True))

        group.points[0].tasks.append(OptReactOnThreat(react_on_threat))
        if roe is not None:
            group.points[0].tasks.append(OptROE(roe))
        if restrict_jettison is not None:
            group.points[0].tasks.append(OptRestrictJettison(restrict_jettison))
        if rtb_winchester is not None:
            group.points[0].tasks.append(OptRTBOnOutOfAmmo(rtb_winchester))

        # Confiscate the bullets of AI missions that do not rely on the gun. There is no
        # "all but gun" RTB winchester option, so air to ground missions with mixed
        # weapon types will insist on using all of their bullets after running out of
        # missiles and bombs. Take away their bullets so they don't strafe a Tor.
        #
        # Exceptions are made for player flights and for airframes where the gun is
        # essential like the A-10 or warbirds.
        if not mission_uses_gun and not self.flight_always_keeps_gun(flight):
            for unit in group.units:
                unit.gun = 0

        group.points[0].tasks.append(OptRTBOnBingoFuel(rtb_on_bingo))
        if flight.coalition.game.settings.ai_jettison_empty_tanks:
            group.points[0].tasks.append(OptJettisonEmptyTanks())
        # Do not restrict afterburner.
        # https://forums.eagle.ru/forum/english/digital-combat-simulator/dcs-world-2-5/bugs-and-problems-ai/ai-ad/7121294-ai-stuck-at-high-aoa-after-making-sharp-turn-if-afterburner-is-restricted

        if flight.client_count and flight.flight_type != FlightType.AEWC:
            # configure AI radio usage for player flights to avoid AI spamming the channel
            if flight.coalition.game.settings.silence_ai_radios:
                group.points[0].tasks.append(OptRadioSilence(True))
            elif flight.coalition.game.settings.limit_ai_radios:
                # the pydcs api models this in a quite strange way for some reason,
                # and has no proper support to choose "nothing"
                radio_usage = OptRadioUsageContact()
                radio_usage.params["action"]["params"]["value"] = "none;"
                group.points[0].tasks.append(radio_usage)

            group.points[0].tasks.append(OptNoReportWaypointPass(True))

    @staticmethod
    def configure_eplrs(group: FlyingGroup[Any], flight: Flight) -> None:
        if flight.unit_type.eplrs_capable:
            group.points[0].tasks.append(EPLRS(group.id))

    def configure_cap(self, group: FlyingGroup[Any], flight: Flight) -> None:
        self.configure_task(flight, group, CAP)
        if not flight.unit_type.gunfighter:
            ammo_type = OptRTBOnOutOfAmmo.Values.AAM
        else:
            ammo_type = OptRTBOnOutOfAmmo.Values.Cannon

        self.configure_behavior(flight, group, rtb_winchester=ammo_type)

    def configure_sweep(self, group: FlyingGroup[Any], flight: Flight) -> None:
        self.configure_task(flight, group, FighterSweep)
        if not flight.unit_type.gunfighter:
            ammo_type = OptRTBOnOutOfAmmo.Values.AAM
        else:
            ammo_type = OptRTBOnOutOfAmmo.Values.Cannon

        self.configure_behavior(flight, group, rtb_winchester=ammo_type)

    def configure_cas(self, group: FlyingGroup[Any], flight: Flight) -> None:
        self.configure_task(flight, group, CAS, [AFAC, AntishipStrike])
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            rtb_winchester=OptRTBOnOutOfAmmo.Values.Unguided,
            restrict_jettison=True,
        )

    def configure_armed_recon(self, group: FlyingGroup[Any], flight: Flight) -> None:
        self.configure_task(flight, group, CAS, [AFAC, AntishipStrike])
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            rtb_winchester=OptRTBOnOutOfAmmo.Values.All,
            restrict_jettison=True,
        )

    def configure_dead(self, group: FlyingGroup[Any], flight: Flight) -> None:
        # Only CAS and SEAD are capable of the Attack Group task. SEAD is arguably more
        # appropriate but it has an extremely limited list of capable aircraft, whereas
        # CAS has a much wider selection of units.
        #
        # Note that the only effect that the DCS task type has is in determining which
        # waypoint actions the group may perform.

        self.configure_task(flight, group, SEAD, [CAS, AFAC, AntishipStrike])
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            rtb_winchester=OptRTBOnOutOfAmmo.Values.All,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_sead(self, group: FlyingGroup[Any], flight: Flight) -> None:
        # CAS is able to perform all the same tasks as SEAD using a superset of the
        # available aircraft, and F-14s are not able to be SEAD despite having TALDs.
        # https://forums.eagle.ru/topic/272112-cannot-assign-f-14-to-sead/

        self.configure_task(flight, group, SEAD, [CAS, AFAC, AntishipStrike])
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            # Guided includes ARMs and TALDs (among other things, but those are the useful
            # weapons for SEAD).
            rtb_winchester=OptRTBOnOutOfAmmo.Values.Guided,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_strike(self, group: FlyingGroup[Any], flight: Flight) -> None:
        self.configure_task(flight, group, GroundAttack, [PinpointStrike, AFAC])
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_anti_ship(self, group: FlyingGroup[Any], flight: Flight) -> None:
        self.configure_task(flight, group, AntishipStrike, [CAS, AFAC, SEAD])
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_runway_attack(self, group: FlyingGroup[Any], flight: Flight) -> None:
        self.configure_task(flight, group, RunwayAttack)
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_oca_strike(self, group: FlyingGroup[Any], flight: Flight) -> None:
        self.configure_task(flight, group, CAS, [AFAC, SEAD])
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            restrict_jettison=True,
        )

    def configure_awacs(self, group: FlyingGroup[Any], flight: Flight) -> None:
        self.configure_task(flight, group, AWACS)
        if not isinstance(flight.flight_plan, AewcFlightPlan):
            logging.error(
                f"Cannot configure AEW&C tasks for {flight} because it does not have "
                "an AEW&C flight plan."
            )
            return

        # Awacs task action
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.WeaponHold,
            restrict_jettison=True,
        )

        group.points[0].tasks.append(AWACSTaskAction())

    def configure_refueling(self, group: FlyingGroup[Any], flight: Flight) -> None:
        self.configure_task(flight, group, Refueling)
        if not (
            isinstance(flight.flight_plan, TheaterRefuelingFlightPlan)
            or isinstance(flight.flight_plan, PackageRefuelingFlightPlan)
            or isinstance(flight.flight_plan, RecoveryTankerFlightPlan)
        ):
            logging.error(
                f"Cannot configure racetrack refueling tasks for {flight} because it "
                "does not have an racetrack refueling flight plan."
            )
            return

        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.WeaponHold,
            restrict_jettison=True,
        )

    def configure_recovery(
        self,
        group: FlyingGroup[Any],
        flight: Flight,
    ) -> None:
        self.configure_refueling(group, flight)
        if not isinstance(flight.flight_plan, RecoveryTankerFlightPlan):
            logging.error(
                f"Cannot configure recovery task for {flight} because it "
                "does not have an recovery tanker flight plan."
            )
            return

        self.configure_tanker_tacan(flight, group)

        clouds = flight.squadron.coalition.game.conditions.weather.clouds
        speed = knots(250).meters_per_second
        altitude = feet(6000).meters
        if clouds is not None:
            if abs(clouds.base - altitude) < feet(1000).meters:
                altitude = clouds.base - feet(1000).meters
            if altitude < feet(2000).meters:
                altitude = clouds.base + feet(6000).meters

        naval_group = self._get_carrier_group(flight.package)
        last_waypoint = len(naval_group.points)  # last waypoint of the CVN/LHA

        tanker_tos = flight.coalition.game.settings.desired_tanker_on_station_time
        lua_predicate = f"""
                local lowfuel = false
                for i, unitObject in pairs(Group.getByName('{group.name}'):getUnits()) do
                    if Unit.getFuel(unitObject) < 0.2 then lowfuel = true end
                end
                return lowfuel
            """

        tanker = ControlledTask(Tanker())
        tanker.stop_after_duration(int(tanker_tos.total_seconds()) + 1)
        tanker.stop_if_lua_predicate(lua_predicate)
        group.points[0].add_task(tanker)

        recovery = ControlledTask(
            RecoveryTanker(naval_group.id, speed, altitude, last_waypoint)
        )
        recovery.stop_if_lua_predicate(lua_predicate)
        recovery.stop_after_duration(int(tanker_tos.total_seconds()) + 1)
        group.points[0].add_task(recovery)

    def configure_tanker_tacan(self, flight: Flight, group: FlyingGroup[Any]) -> None:
        tanker_info = self.mission_data.tankers[-1]
        tacan = tanker_info.tacan
        if flight.unit_type.dcs_unit_type.tacan and tacan:
            if flight.tcn_name is None:
                cs = tanker_info.callsign[:-2]
                csn = tanker_info.callsign[-1]
                tacan_callsign = {
                    "Texaco": "TX",
                    "Arco": "AC",
                    "Shell": "SH",
                }.get(cs)
                if tacan_callsign:
                    tacan_callsign = tacan_callsign + csn
                else:
                    tacan_callsign = cs[0:2] + csn
            else:
                tacan_callsign = flight.tcn_name

            group.points[0].add_task(
                ActivateBeaconCommand(
                    tacan.number,
                    tacan.band.value,
                    tacan_callsign.upper(),
                    bearing=True,
                    unit_id=group.units[0].id,
                    aa=True,
                )
            )

    def _get_carrier_group(self, package: Package) -> ShipGroup:
        name = package.target.name
        carrier_position = package.target.position
        for carrier in self.mission_data.carriers:
            if carrier.ship_group.position == carrier_position:
                return carrier.ship_group
        raise RuntimeError(
            f"Could not find a carrier in the mission matching {name} at "
            f"({carrier_position.x}, {carrier_position.y})"
        )

    def configure_escort(self, group: FlyingGroup[Any], flight: Flight) -> None:
        self.configure_task(flight, group, Escort)
        self.configure_behavior(
            flight, group, roe=OptROE.Values.OpenFire, restrict_jettison=True
        )

    def configure_sead_escort(self, group: FlyingGroup[Any], flight: Flight) -> None:
        self.configure_task(flight, group, SEAD)
        self.configure_behavior(
            flight,
            group,
            roe=OptROE.Values.OpenFire,
            # Guided includes ARMs and TALDs (among other things, but those are the useful
            # weapons for SEAD).
            rtb_winchester=OptRTBOnOutOfAmmo.Values.Guided,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_transport(self, group: FlyingGroup[Any], flight: Flight) -> None:
        self.configure_task(flight, group, Transport)
        roe = OptROE.Values.WeaponHold
        if flight.is_hercules:
            group.task = GroundAttack.name
            roe = OptROE.Values.OpenFire
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=roe,
            restrict_jettison=True,
        )

    def configure_ferry(self, group: FlyingGroup[Any], flight: Flight) -> None:
        # Every aircraft is capable of 'Nothing', but pydcs doesn't always export it
        group.task = Nothing.name
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.WeaponHold,
            restrict_jettison=True,
            rtb_on_bingo=False,
        )

    def configure_unknown_task(self, group: FlyingGroup[Any], flight: Flight) -> None:
        logging.error(f"Unhandled flight type: {flight.flight_type}")
        self.configure_behavior(flight, group)

    @staticmethod
    def flight_always_keeps_gun(flight: Flight) -> bool:
        # Never take bullets from players. They're smart enough to know when to use it
        # and when to RTB.
        if flight.client_count > 0:
            return True

        return flight.unit_type.always_keeps_gun

    @staticmethod
    def configure_task(
        flight: Flight,
        group: FlyingGroup[Any],
        preferred_task: Type[MainTask],
        fallback_tasks: Optional[List[Type[MainTask]]] = None,
    ) -> None:
        ac_type = flight.unit_type.dcs_unit_type.id

        # Not all aircraft are always compatible with the preferred task,
        # so a common fallback is to use CAS instead.
        # Sometimes it's also the other way around,
        # i.e. the preferred task is available while CAS isn't
        # This method should allow for dynamic choice between tasks,
        # obviously depending on what's preferred and compatible...

        if preferred_task in flight.unit_type.dcs_unit_type.tasks:
            group.task = preferred_task.name
            return
        if fallback_tasks:
            for task in fallback_tasks:
                if task in flight.unit_type.dcs_unit_type.tasks:
                    group.task = task.name
                    return
        if flight.unit_type.dcs_unit_type.task_default and preferred_task == Nothing:
            group.task = flight.unit_type.dcs_unit_type.task_default.name
            logging.warning(
                f"{ac_type} is not capable of 'Nothing', using default task '{group.task}'"
            )
            return
        if flight.roster.members and flight.roster.members[0].is_player:
            group.task = (
                flight.unit_type.dcs_unit_type.task_default.name
                if flight.unit_type.dcs_unit_type.task_default
                else group.task  # even if this is incompatible, if it's a client we don't really care...
            )
            logging.warning(
                f"Client override: {ac_type} is not capable of '{preferred_task}', using default task '{group.task}'"
            )
            return

        fallback_part = (
            f" nor any of the following fall-back tasks: {[task.name for task in fallback_tasks]}"
            if fallback_tasks
            else ""
        )
        raise RuntimeError(
            f"{ac_type} is neither capable of {preferred_task.name}"
            f"{fallback_part}. Can't generate {flight.flight_type} flight."
        )
