import math

from dcs.point import MovingPoint
from dcs.task import (
    OptECMUsing,
    ControlledTask,
    Targets,
    EngageTargetsInZone,
)

from game.missiongenerator.motorpoolpopulator import motorpool_full_grid_extent_m
from game.theater.theatergroundobject import MotorpoolGroundObject
from game.utils import nautical_miles
from .pydcswaypointbuilder import PydcsWaypointBuilder

# Slack beyond the furthest slot of a full parked grid: 20 m = 60 ft.
_MOTORPOOL_ZONE_BUFFER_M = 20.0


class ArmedReconIngressBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        self.register_special_ingress_points()
        # Preemptively use ECM to better avoid getting swatted.
        ecm_option = OptECMUsing(value=OptECMUsing.Values.UseIfDetectedLockByRadar)
        waypoint.tasks.append(ecm_option)

        target = self.flight.package.target
        configured_range = (
            self.flight.coalition.game.settings.armed_recon_engagement_range_distance
        )
        if isinstance(target, MotorpoolGroundObject):
            # Mission spec: the motorpool zone is centered on the garage (the
            # TGO position, not the ToT waypoint) and sized to cover a FULL
            # 5x5 parked grid plus a 20 m buffer. The radius therefore stays
            # stable no matter how many vehicles are currently rendered, and
            # the configured engagement range never applies.
            zone_position = target.position
            radius = math.ceil(
                motorpool_full_grid_extent_m() + _MOTORPOOL_ZONE_BUFFER_M
            )
        else:
            zone_position = self.flight.flight_plan.tot_waypoint.position
            radius = int(nautical_miles(configured_range).meters)
        waypoint.add_task(
            ControlledTask(
                EngageTargetsInZone(
                    position=zone_position,
                    radius=radius,
                    targets=[
                        Targets.All.GroundUnits,
                        Targets.All.Air.Helicopters,
                    ],
                )
            )
        )
