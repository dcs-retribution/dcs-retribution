from dcs.point import MovingPoint
from dcs.task import (
    OptECMUsing,
    ControlledTask,
    EngageTargets,
    Targets,
)

from game.utils import nautical_miles
from .pydcswaypointbuilder import PydcsWaypointBuilder


class SeadSweepIngressBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        # Preemptively use ECM to better avoid getting swatted.
        ecm_option = OptECMUsing(value=OptECMUsing.Values.UseIfDetectedLockByRadar)
        waypoint.tasks.append(ecm_option)

        waypoint.add_task(
            ControlledTask(
                EngageTargets(
                    # TODO: From doctrine.
                    max_distance=int(
                        nautical_miles(
                            self.flight.coalition.game.settings.sead_sweep_engagement_range_distance
                        ).meters
                    ),
                    targets=[Targets.All.GroundUnits.AirDefence.AAA.SAMRelated],
                )
            )
        )
