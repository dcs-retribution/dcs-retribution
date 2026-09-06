import logging

from dcs.point import MovingPoint
from dcs.task import OptECMUsing

from game.theater import TheaterGroundObject
from .pydcswaypointbuilder import PydcsWaypointBuilder


class SeadIngressBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        self.register_special_strike_points(self.waypoint.targets)
        self.register_special_ingress_points()

        target = self.package.target
        if not isinstance(target, TheaterGroundObject):
            logging.error(
                "Unexpected target type for SEAD mission: %s",
                target.__class__.__name__,
            )
            return

        # Plain SEAD no longer fires a point-in-time AttackGroup at ingress; it loiters
        # at the SEAD_LOITER anchor and engages radars reactively (SEAD main task) as
        # they come up. Keep ECM on for survivability during the loiter.
        ecm_option = OptECMUsing(value=OptECMUsing.Values.UseIfDetectedLockByRadar)
        waypoint.tasks.append(ecm_option)
