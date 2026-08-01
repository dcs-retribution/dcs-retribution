import logging

from dcs.mapping import Vector2
from dcs.point import MovingPoint
from dcs.task import (
    ControlledTask,
    Embarking,
    OptVerticalTakeoffLanding,
    OrbitAction,
)

from game.squadrons.downedpilot import DownedPilot
from game.utils import feet, kph
from .pydcswaypointbuilder import PydcsWaypointBuilder

#: How long the rescue helicopter holds at the pickup waiting for the pilot.
PICKUP_DURATION_SECONDS = 300

#: Altitude the helicopter holds at under hover extraction. Low enough that
#: OpsCSAR.lua counts it as on station (HOVER_MAX_AGL) and that it reads as a
#: hoist rather than an overflight.
HOVER_ALTITUDE = feet(100)

#: Speed of the hold orbit. Slow, so the helicopter stays over the survivor.
HOVER_ORBIT_SPEED = kph(90)


class CsarPickupBuilder(PydcsWaypointBuilder):
    """Sets up the rescue helicopter's behaviour at the downed pilot.

    Two modes, selected by the ``csar_hover_extraction`` setting:

    * Landing (default) uses DCS's native troop transport: an ``Embarking`` task
      naming the downed pilot's group, which pairs with the
      ``EmbarkToTransport`` task the pilot carries (see CsarGenerator). The
      embark task handles the landing itself, so no separate ``Land`` task is
      added -- one would only fight it for control of the approach.

    * Hover extraction holds the helicopter in a low orbit over the pickup and
      lets OpsCSAR.lua perform the extraction by script. Nothing in DCS will stop
      the flight here on its own, so the hold is explicit: without it the AI
      simply flies through the waypoint and the script never sees it on station.
    """

    def build(self) -> MovingPoint:
        waypoint = super().build()

        if self.flight.coalition.game.settings.csar_hover_extraction:
            self._build_hover_hold(waypoint)
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

        # Set down vertically rather than running on. The pickup is unprepared
        # ground with a survivor stood next to it, so a rolling landing is both
        # unrealistic and more likely to end badly.
        waypoint.add_task(OptVerticalTakeoffLanding(True))
        waypoint.add_task(
            Embarking(
                position=Vector2(waypoint.position.x, waypoint.position.y),
                groupids=[pilot_group.group_id],
                duration=PICKUP_DURATION_SECONDS,
            )
        )
        return waypoint

    def _build_hover_hold(self, waypoint: MovingPoint) -> None:
        """Holds the flight in a low orbit so the script can extract the pilot."""
        waypoint.alt = int(HOVER_ALTITUDE.meters)
        waypoint.alt_type = "RADIO"
        orbit = ControlledTask(
            OrbitAction(
                altitude=int(HOVER_ALTITUDE.meters),
                speed=int(HOVER_ORBIT_SPEED.kph),
                pattern=OrbitAction.OrbitPattern.Circle,
            )
        )
        orbit.stop_after_duration(PICKUP_DURATION_SECONDS)
        waypoint.add_task(orbit)
