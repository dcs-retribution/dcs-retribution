import logging
from typing import Any, Optional, Type

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
)
from dcs.unitgroup import FlyingGroup

from game.ato import Flight, FlightType
from game.ato.flightplans.aewc import AewcFlightPlan
from game.ato.flightplans.packagerefueling import PackageRefuelingFlightPlan
from game.ato.flightplans.theaterrefueling import TheaterRefuelingFlightPlan


class AircraftBehavior:
    def __init__(self, task: FlightType) -> None:
        self.task = task

    def apply_to(self, flight: Flight, group: FlyingGroup[Any]) -> None:
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
        elif self.task in [FlightType.CAS, FlightType.BAI]:
            self.configure_cas(group, flight)
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

        # Activate AI unlimited fuel for all flights at startup
        if ai_unlimited_fuel and not (flight.state.is_at_ip or flight.state.in_combat):
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
        group.points[0].tasks.append(OptJettisonEmptyTanks())
        # Do not restrict afterburner.
        # https://forums.eagle.ru/forum/english/digital-combat-simulator/dcs-world-2-5/bugs-and-problems-ai/ai-ad/7121294-ai-stuck-at-high-aoa-after-making-sharp-turn-if-afterburner-is-restricted

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
        self.configure_task(flight, group, CAS, AFAC)
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            rtb_winchester=OptRTBOnOutOfAmmo.Values.Unguided,
            restrict_jettison=True,
        )

    def configure_dead(self, group: FlyingGroup[Any], flight: Flight) -> None:
        # Only CAS and SEAD are capable of the Attack Group task. SEAD is arguably more
        # appropriate but it has an extremely limited list of capable aircraft, whereas
        # CAS has a much wider selection of units.
        #
        # Note that the only effect that the DCS task type has is in determining which
        # waypoint actions the group may perform.

        self.configure_task(flight, group, SEAD, CAS)
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

        self.configure_task(flight, group, SEAD, CAS)
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
        self.configure_task(flight, group, GroundAttack, PinpointStrike)
        self.configure_behavior(
            flight,
            group,
            react_on_threat=OptReactOnThreat.Values.EvadeFire,
            roe=OptROE.Values.OpenFire,
            restrict_jettison=True,
            mission_uses_gun=False,
        )

    def configure_anti_ship(self, group: FlyingGroup[Any], flight: Flight) -> None:
        self.configure_task(flight, group, AntishipStrike, CAS)
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
        self.configure_task(flight, group, CAS)
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
        fallback_task: Optional[Type[MainTask]] = None,
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
        elif fallback_task and fallback_task in flight.unit_type.dcs_unit_type.tasks:
            group.task = fallback_task.name
        elif flight.unit_type.dcs_unit_type.task_default and preferred_task == Nothing:
            group.task = flight.unit_type.dcs_unit_type.task_default.name
            logging.warning(
                f"{ac_type} is not capable of 'Nothing', using default task '{group.task}'"
            )
        else:
            fallback_part = f" nor {fallback_task.name}" if fallback_task else ""
            raise RuntimeError(
                f"{ac_type} is neither capable of {preferred_task.name}"
                f"{fallback_part}. Can't generate {flight.flight_type} flight."
            )
