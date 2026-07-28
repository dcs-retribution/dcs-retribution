import logging

from dcs.mapping import Vector2
from dcs.point import MovingPoint
from dcs.task import Embarking

from game.squadrons.downedpilot import DownedPilot
from .pydcswaypointbuilder import PydcsWaypointBuilder

#: How long the rescue helicopter waits at the pickup for the pilot to board.
EMBARK_DURATION_SECONDS = 300


class CsarPickupBuilder(PydcsWaypointBuilder):
    """Wires the rescue helicopter into DCS's native troop-transport pickup.

    The helicopter gets an ``Embarking`` task naming the downed pilot's group,
    which pairs with the ``EmbarkToTransport`` task the pilot carries (see
    CsarGenerator). DCS then walks the pilot over and loads them aboard.

    Deliberately *no* ``Land`` task: the pickup site is unprepared terrain and the
    AI frequently refuses to set down on it, leaving the flight circling. The
    embark logic works from a hover, so the helicopter is left to hold at the
    waypoint instead.
    """

    def build(self) -> MovingPoint:
        waypoint = super().build()

        target = self.flight.package.target
        if not isinstance(target, DownedPilot):
            logging.error(
                "CSAR pickup waypoint on a flight whose target is %s, not a downed "
                "pilot. No embark task will be added.",
                type(target).__name__,
            )
            return waypoint

        pilot_group = self.mission_data.csar_pilot_groups.get(str(target.id))
        if pilot_group is None:
            logging.error(
                "No downed-pilot group was generated for %s; the rescue flight has "
                "nothing to embark.",
                target.name,
            )
            return waypoint

        waypoint.add_task(
            Embarking(
                position=Vector2(waypoint.position.x, waypoint.position.y),
                groupids=[pilot_group.group_id],
                duration=EMBARK_DURATION_SECONDS,
            )
        )
        return waypoint
