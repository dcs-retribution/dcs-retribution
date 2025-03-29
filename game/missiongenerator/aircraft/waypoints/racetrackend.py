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
        # Unlimited fuel option : enable at racetrack end. Must be first option to work.
        if self.flight.squadron.coalition.game.settings.ai_unlimited_fuel:
            waypoint.tasks.insert(0, SetUnlimitedFuelCommand(True))

        # Disable Offensive Jamming at Racetrack End
        if self.flight.flight_type == FlightType.AEWC:
            # Stop Offensive Jamming for all AWACS flights
            settings = self.flight.coalition.game.settings
            ai_jammer = settings.plugin_option("ewrj.ai_jammer_enabled")
            if settings.plugins.get("ewrj") and ai_jammer:
                # all units in group are AWACS, no specific checks needed
                for unit, member in zip(self.group.units, self.flight.iter_members()):
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
