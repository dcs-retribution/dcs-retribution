import random
from typing import List

from dcs.point import MovingPoint
from dcs.task import (
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

        if self.flight.flight_type == FlightType.ESCORT:
            self.configure_escort_tasks(
                waypoint,
                [
                    Targets.All.Air.Planes.Fighters.id,
                    Targets.All.Air.Planes.MultiroleFighters.id,
                ],
            )
        elif self.flight.flight_type == FlightType.SEAD_ESCORT:
            if isinstance(self.flight.package.target, NavalControlPoint):
                self.configure_escort_tasks(
                    waypoint,
                    [
                        Targets.All.Naval.id,
                        Targets.All.GroundUnits.AirDefence.AAA.SAMRelated.id,
                    ],
                    max_dist=40,
                    vertical_spacing=1000,
                )
            else:
                self.configure_escort_tasks(
                    waypoint,
                    [Targets.All.GroundUnits.AirDefence.AAA.SAMRelated.id],
                    max_dist=40,
                    vertical_spacing=1000,
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

        rx = (random.random() + 0.1) * 1000
        ry = feet(vertical_spacing).meters
        rz = (random.random() + 0.1) * 50 * random.choice([-1, 1])
        pos = {"x": rx, "y": ry, "z": rz}

        lastwpt = 6 if self.package.primary_task == FlightType.STRIKE else 5

        group_id = None
        if self.package.primary_flight is not None:
            group_id = self.package.primary_flight.group_id

        waypoint.tasks.append(
            EscortTaskAction(
                group_id=group_id,
                engagement_max_dist=int(nautical_miles(max_dist).meters),
                lastwpt=lastwpt,
                targets=target_types,
                position=pos)
        )
