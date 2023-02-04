import random
from typing import List

from dcs.point import MovingPoint
from dcs.task import (
    ControlledTask,
    EscortTaskAction,
    OptECMUsing,
    OptFormation,
    Targets,
)

from game.ato import FlightType
from game.theater import NavalControlPoint
from game.utils import nautical_miles, feet
from .pydcswaypointbuilder import PydcsWaypointBuilder


class JoinPointBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        waypoint.tasks.append(OptFormation.finger_four_open())

        doctrine = self.flight.coalition.doctrine

        if self.flight.flight_type == FlightType.ESCORT:
            self.configure_escort_tasks(
                waypoint,
                [
                    Targets.All.Air.Planes.Fighters.id,
                    Targets.All.Air.Planes.MultiroleFighters.id,
                ],
                max_dist=doctrine.escort_engagement_range.nautical_miles,
                vertical_spacing=doctrine.escort_spacing.feet,
            )
        elif self.flight.flight_type == FlightType.SEAD_ESCORT:
            if isinstance(self.flight.package.target, NavalControlPoint):
                self.configure_escort_tasks(
                    waypoint,
                    [
                        Targets.All.Naval.id,
                        Targets.All.GroundUnits.AirDefence.AAA.SAMRelated.id,
                    ],
                    max_dist=doctrine.sead_escort_engagement_range.nautical_miles,
                    vertical_spacing=doctrine.sead_escort_spacing.feet,
                )
            else:
                self.configure_escort_tasks(
                    waypoint,
                    [Targets.All.GroundUnits.AirDefence.AAA.SAMRelated.id],
                    max_dist=doctrine.sead_escort_engagement_range.nautical_miles,
                    vertical_spacing=doctrine.sead_escort_spacing.feet,
                )

            # Let the AI use ECM to preemptively defend themselves.
            ecm_option = OptECMUsing(value=OptECMUsing.Values.UseIfDetectedLockByRadar)
            waypoint.tasks.append(ecm_option)

        elif not self.flight.flight_type.is_air_to_air:
            # Capture any non A/A type to avoid issues with SPJs that use the primary radar such as the F/A-18C.
            # You can bully them with STT to not be able to fire radar guided missiles at you,
            # so best choice is to not let them perform jamming for now.

            # Let the AI use ECM to defend themselves.
            ecm_option = OptECMUsing(value=OptECMUsing.Values.UseIfOnlyLockByRadar)
            waypoint.tasks.append(ecm_option)

    def configure_escort_tasks(
        self,
        waypoint: MovingPoint,
        target_types: List[str],
        max_dist: float = 30.0,
        vertical_spacing: float = 2000.0,
    ) -> None:
        rx = (random.random() + 0.1) * 333
        ry = feet(vertical_spacing).meters
        rz = (random.random() + 0.1) * 166 * random.choice([-1, 1])
        pos = {"x": rx, "y": ry, "z": rz}

        group_id = None
        if self.package.primary_flight is not None:
            group_id = self.package.primary_flight.group_id

        escort = ControlledTask(
            EscortTaskAction(
                group_id=group_id,
                engagement_max_dist=int(nautical_miles(max_dist).meters),
                targets=target_types,
                position=pos,
            )
        )

        escort.stop_if_user_flag(f"split-{id(self.package)}", True)

        waypoint.tasks.append(escort)
