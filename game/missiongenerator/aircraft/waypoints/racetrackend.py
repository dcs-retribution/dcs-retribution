import logging

from dcs.point import MovingPoint
from dcs.task import (
    SetUnlimitedFuelCommand,
    RunScript,
    OptReactOnThreat,
)

from game.ato import FlightType
from game.ato.flightplans.patrolling import PatrollingFlightPlan
from .pydcswaypointbuilder import PydcsWaypointBuilder


class RaceTrackEndBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        # List of specific aircraft types that should get their own ewrj_menu_trigger and be excluded from needing a jammer
        specific_aircraft_types = [
            "CLP_E7A",
            "CLP_P8",
            "CLP_TU214R",
            "CLP_TU214",
        ]  # Replace with aircraft types e.g. E-3A

        # List of excluded aircraft types that should not get any triggers
        excluded_aircraft_types = [
            "F-16C_50"
        ]  # Replace with aircraft types with working ECM

        # Unlimited fuel option : enable at racetrack end. Must be first option to work.
        if self.flight.squadron.coalition.game.settings.ai_unlimited_fuel:
            waypoint.tasks.insert(0, SetUnlimitedFuelCommand(True))

        # Disable Offensive Jamming at Racetrack End
        if self.flight.flight_type == FlightType.AEWC:
            # Stop Offensive Jamming
            settings = self.flight.coalition.game.settings
            ai_jammer = settings.plugin_option("ewrj.ai_jammer_enabled")
            if settings.plugins.get("ewrj") and ai_jammer:
                for unit, member in zip(self.group.units, self.flight.iter_members()):
                    if unit.type in excluded_aircraft_types:
                        continue
                    if unit.type not in specific_aircraft_types:
                        continue
                    script_content = f'stopEWjamming("{unit.name}")'
                    stop_jamming_script = RunScript(script_content)
                    waypoint.tasks.append(stop_jamming_script)

                evade_fire = OptReactOnThreat(OptReactOnThreat.Values.EvadeFire)
                waypoint.tasks.append(evade_fire)

    def build(self) -> MovingPoint:
        waypoint = super().build()

        if not isinstance(self.flight.flight_plan, PatrollingFlightPlan):
            flight_plan_type = self.flight.flight_plan.__class__.__name__
            logging.error(
                f"Cannot create race track for {self.flight} because "
                f"{flight_plan_type} does not define a patrol."
            )
            return waypoint

        self.waypoint.departure_time = self.flight.flight_plan.patrol_end_time
        return waypoint
