from dcs.point import MovingPoint
from dcs.task import OptECMUsing, OptFormation, RunScript, SetUnlimitedFuelCommand

from game.settings import Settings

from .pydcswaypointbuilder import PydcsWaypointBuilder


class SplitPointBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        # Unlimited fuel option : disable on non-player flights. Must be first option to work.
        if (
            self.flight.squadron.coalition.game.settings.ai_unlimited_fuel
            and not self.flight.client_count
        ):
            waypoint.tasks.insert(0, SetUnlimitedFuelCommand(False))

        if not self.flight.flight_type.is_air_to_air:
            # Capture any non A/A type to avoid issues with SPJs that use the primary radar such as the F/A-18C.
            # You can bully them with STT to not be able to fire radar guided missiles at you,
            # so best choice is to not let them perform jamming for now.

            # Let the AI use ECM to defend themselves.
            ecm_option = OptECMUsing(value=OptECMUsing.Values.UseIfOnlyLockByRadar)
            waypoint.tasks.append(ecm_option)

        if self.flight.is_helo:
            waypoint.tasks.append(OptFormation.rotary_wedge())
        else:
            waypoint.tasks.append(OptFormation.finger_four_close())
        if not self.flight.is_helo:
            waypoint.speed_locked = True
            waypoint.speed = self.flight.coalition.doctrine.rtb_speed.meters_per_second
            waypoint.ETA_locked = False
        if self.flight is self.package.primary_flight:
            script = RunScript(
                f'trigger.action.setUserFlag("split-{id(self.package)}", true)'
            )
            waypoint.tasks.append(script)
