import logging

from dcs.mapping import Vector2
from dcs.point import MovingPoint
from dcs.task import (
    Embarking,
    OptVerticalTakeoffLanding,
    RunScript,
)

from game.squadrons.downedpilot import DownedPilot
from game.utils import feet
from .pydcswaypointbuilder import PydcsWaypointBuilder

#: How long the rescue helicopter holds at the pickup waiting for the pilot.
PICKUP_DURATION_SECONDS = 300

#: How long the helicopter holds its hover before the pilot is winched aboard.
#: Long enough to read as a hoist, short enough not to leave the flight sat over a
#: threat area. OpsCSAR.lua times the hold; this is only the value it is given.
HOVER_DURATION_SECONDS = 30

#: How high above the ground the helicopter holds under hover extraction.
#:
#: Used twice: as the pickup waypoint's altitude, so the AI arrives low, and as the
#: height OpsCSAR.lua adds to the terrain elevation when it pushes the hover. The
#: script has to do the second part because the DCS Orbit task takes an MSL
#: altitude and Retribution has no terrain elevation at mission-generation time.
HOVER_ALTITUDE = feet(100)


class CsarPickupBuilder(PydcsWaypointBuilder):
    """Sets up the rescue helicopter's behaviour at the downed pilot.

    Two modes, selected by the ``csar_hover_extraction`` setting:

    * Landing (default) uses DCS's native troop transport: an ``Embarking`` task
      naming the downed pilot's group, which pairs with the
      ``EmbarkToTransport`` task the pilot carries (see CsarGenerator). The
      embark task handles the landing itself, so no separate ``Land`` task is
      added -- one would only fight it for control of the approach.

    * Hover extraction, either because the setting asks for it or because this
      particular survivor is in the water and nothing can land beside them, has no
      native mechanic behind it at all, so the waypoint
      only hands off to OpsCSAR.lua: reaching it runs a script that tells the plugin
      this helicopter is on station for this pilot. The plugin pushes the hover onto
      the flight and pops it again once the pilot is aboard. Everything that needs
      terrain elevation or runtime positions lives there rather than here.
    """

    def build(self) -> MovingPoint:
        waypoint = super().build()

        target = self.flight.package.target
        if not isinstance(target, DownedPilot):
            logging.error(
                "CSAR pickup waypoint on a flight whose target is %s, not a downed "
                "pilot. No pickup task will be added.",
                type(target).__name__,
            )
            return waypoint

        if target.needs_hover_extraction(self.flight.coalition.game.settings):
            self._build_hover_hold(waypoint, target)
        else:
            self._build_embark(waypoint, target)
        return waypoint

    def _build_embark(self, waypoint: MovingPoint, target: DownedPilot) -> None:
        pilot_group = self.mission_data.csar_pilot_groups.get(str(target.id))
        if pilot_group is None:
            logging.error(
                "No downed-pilot group was generated for %s; the rescue flight has "
                "nothing to embark.",
                target.name,
            )
            return

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

    def _build_hover_hold(self, waypoint: MovingPoint, target: DownedPilot) -> None:
        """Hands the flight to OpsCSAR.lua, which holds it in a hover."""
        waypoint.alt = int(HOVER_ALTITUDE.meters)
        waypoint.alt_type = "RADIO"
        # We have just overwritten what the base builder decided, so re-apply the
        # AMSL switch (the switch_baro_fix setting). It matters most exactly where
        # this waypoint is most likely to sit -- over the sea, for a survivor in
        # the water -- because DCS measures AGL from the sea *bottom*, which would
        # put a 100ft hold well under water. The number is unchanged either way:
        # at sea, AMSL and height above the surface are the same thing.
        if self.flight.is_helo and self.flight.coalition.game.settings.switch_baro_fix:
            self.switch_to_baro_if_in_sea(waypoint)
        # Nothing in the .miz can hold the AI here: the DCS Orbit task's altitude is
        # MSL, and we have no terrain elevation to convert our AGL hold to, so the
        # script sets the hover up instead. Guarded because OpsCSAR.lua leaves the
        # global undefined if it found no CSAR data to work with.
        waypoint.add_task(
            RunScript(
                "if OpsCSAR_BeginHover then "
                f"OpsCSAR_BeginHover('{self.group.name}', '{target.id}') end"
            )
        )
