from dcs.point import MovingPoint
from dcs.task import Land

from .pydcswaypointbuilder import PydcsWaypointBuilder

#: How long the rescue helicopter waits on the ground for the pilot to board.
#: The shared LandingZoneBuilder only waits 30s, which is not enough for a pilot
#: to cover the distance from where the terrain-aware Lua search actually placed
#: them (up to ~150m away) and board.
LAND_DURATION_SECONDS = 180

#: Small jitter so a multi-ship flight doesn't try to set down on one spot.
_TOUCHDOWN_SPREAD = 40
_TOUCHDOWN_MIN = 15


class CsarPickupBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        landing_point = waypoint.position.random_point_within(
            _TOUCHDOWN_SPREAD, _TOUCHDOWN_MIN
        )
        combat_land = self.flight.coalition.game.settings.use_ai_combat_landing
        waypoint.add_task(
            Land(
                landing_point,
                duration=LAND_DURATION_SECONDS,
                combat_landing=combat_land,
            )
        )
        return waypoint
