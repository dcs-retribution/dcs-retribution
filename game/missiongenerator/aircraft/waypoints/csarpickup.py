import logging

from dcs.mapping import Vector2
from dcs.point import MovingPoint
from dcs.task import Embarking, Land

from game.squadrons.downedpilot import DownedPilot
from .pydcswaypointbuilder import PydcsWaypointBuilder

#: How long the rescue helicopter holds at the pickup waiting for the pilot.
PICKUP_DURATION_SECONDS = 300

#: Small jitter so a multi-ship flight doesn't try to set down on one spot.
_TOUCHDOWN_SPREAD = 40
_TOUCHDOWN_MIN = 15


class CsarPickupBuilder(PydcsWaypointBuilder):
    """Sets up the rescue helicopter's behaviour at the downed pilot.

    Two modes, selected by the ``csar_hover_extraction`` setting:

    * Landing (default) uses DCS's native troop transport. The helicopter is
      given a ``Land`` task plus an ``Embarking`` task naming the downed pilot's
      group, which pairs with the ``EmbarkToTransport`` task the pilot carries
      (see CsarGenerator), and DCS walks the pilot aboard. The ``Land`` task is
      required: the embark only fires once the helicopter is actually down with
      weight off wheels, so an ``Embarking`` task alone does nothing.

    * Hover extraction adds neither task. The helicopter holds at the waypoint
      and OpsCSAR.lua performs the extraction by script once it is in a low hover
      near the pilot. Less authentic, but immune to terrain the AI refuses to
      land on.
    """

    def build(self) -> MovingPoint:
        waypoint = super().build()

        if self.flight.coalition.game.settings.csar_hover_extraction:
            # Scripted extraction; deliberately no land or embark tasking.
            return waypoint

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

        landing_point = waypoint.position.random_point_within(
            _TOUCHDOWN_SPREAD, _TOUCHDOWN_MIN
        )
        combat_land = self.flight.coalition.game.settings.use_ai_combat_landing
        waypoint.add_task(
            Land(
                landing_point,
                duration=PICKUP_DURATION_SECONDS,
                combat_landing=combat_land,
            )
        )
        waypoint.add_task(
            Embarking(
                position=Vector2(waypoint.position.x, waypoint.position.y),
                groupids=[pilot_group.group_id],
                duration=PICKUP_DURATION_SECONDS,
            )
        )
        return waypoint
