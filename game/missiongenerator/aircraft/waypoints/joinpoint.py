import random
from typing import List

from dcs.point import MovingPoint
from dcs.task import (
    ControlledTask,
    EscortTaskAction,
    OptECMUsing,
    OptFormation,
    Targets,
    OptROE,
    SetUnlimitedFuelCommand,
)

from game.ato import FlightType
from game.theater import NavalControlPoint
from game.utils import nautical_miles, feet
from .pydcswaypointbuilder import PydcsWaypointBuilder


class JoinPointBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        # Unlimited fuel option : disable at racetrack start. Must be first option to work.
        if self.flight.squadron.coalition.game.settings.ai_unlimited_fuel:
            if waypoint.tasks and isinstance(
                waypoint.tasks[0], SetUnlimitedFuelCommand
            ):
                waypoint.tasks[0] = SetUnlimitedFuelCommand(False)
            else:
                waypoint.tasks.insert(0, SetUnlimitedFuelCommand(False))

        if self.flight.is_helo:
            waypoint.tasks.append(OptFormation.rotary_wedge())
        else:
            waypoint.tasks.append(OptFormation.finger_four_open())

        doctrine = self.flight.coalition.doctrine

        if self.flight.flight_type == FlightType.ESCORT:
            targets = [
                Targets.All.Air.Planes.Fighters.id,
                Targets.All.Air.Planes.MultiroleFighters.id,
            ]
            if self.flight.is_helo:
                targets = [
                    Targets.All.Air.Helicopters.id,
                    Targets.All.GroundUnits.AirDefence.id,
                    Targets.All.GroundUnits.Infantry.id,
                    Targets.All.GroundUnits.GroundVehicles.ArmoredVehicles.id,
                    Targets.All.Naval.Ships.ArmedShips.LightArmedShips.id,
                ]
            self.configure_escort_tasks(
                waypoint,
                targets,
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
        if self.flight.is_helo:
            # Make helicopters a bit more aggressive
            waypoint.tasks.append(OptROE(value=OptROE.Values.OpenFireWeaponFree))
        else:
            waypoint.tasks.append(OptROE(value=OptROE.Values.OpenFire))

        rx = (random.random() + 0.1) * 333
        ry = feet(vertical_spacing).meters
        rz = (random.random() + 0.1) * 166 * random.choice([-1, 1])
        pos = {"x": rx, "y": ry, "z": rz}
        engage_dist = int(nautical_miles(max_dist).meters)

        if self.flight.is_helo:
            for key in pos:
                pos[key] *= 0.25
            engage_dist = int(engage_dist * 0.25)

        group_id = None
        if self.package.primary_flight is not None:
            group_id = self.package.primary_flight.group_id

        escort = ControlledTask(
            EscortTaskAction(
                group_id=group_id,
                engagement_max_dist=engage_dist,
                targets=target_types,
                position=pos,
            )
        )

        escort.stop_if_user_flag(f"split-{id(self.package)}", True)

        waypoint.tasks.append(escort)
