import logging

from dcs.point import MovingPoint
from dcs.task import EngageTargets, EngageTargetsInZone, Targets

from game.ato.flightplans.cas import CasFlightPlan
from game.utils import nautical_miles
from .pydcswaypointbuilder import PydcsWaypointBuilder


class CasIngressBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        self.register_special_ingress_points()
        if isinstance(self.flight.flight_plan, CasFlightPlan):
            patrol_center = (
                self.flight.flight_plan.layout.patrol_start.position
                + self.flight.flight_plan.layout.patrol_end.position
            ) / 2
            waypoint.add_task(
                EngageTargetsInZone(
                    position=patrol_center,
                    radius=int(self.flight.flight_plan.engagement_distance.meters),
                    targets=[
                        Targets.All.GroundUnits.GroundVehicles,
                        Targets.All.GroundUnits.AirDefence.AAA,
                        Targets.All.GroundUnits.Infantry,
                    ],
                )
            )
        else:
            logging.error("No CAS waypoint found. Falling back to search and engage")
            waypoint.add_task(
                EngageTargets(
                    max_distance=int(
                        nautical_miles(
                            self.flight.coalition.game.settings.cas_engagement_range_distance
                        ).meters
                    ),
                    targets=[
                        Targets.All.GroundUnits.GroundVehicles,
                        Targets.All.GroundUnits.AirDefence.AAA,
                        Targets.All.GroundUnits.Infantry,
                    ],
                )
            )
