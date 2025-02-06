from abc import ABC
from datetime import timedelta

from game.utils import Speed, knots, Distance, meters
from .patrolling import PatrollingFlightPlan, PatrollingLayout


class RefuelingFlightPlan(PatrollingFlightPlan[PatrollingLayout], ABC):
    @property
    def patrol_duration(self) -> timedelta:
        return self.flight.coalition.game.settings.desired_tanker_on_station_time

    @property
    def patrol_speed(self) -> Speed:
        # TODO: Could use self.flight.unit_type.preferred_patrol_speed(altitude).
        if self.flight.unit_type.patrol_speed is not None:
            return self.flight.unit_type.patrol_speed
        # ~280 knots IAS at 21000.
        return knots(400)

    @property
    def engagement_distance(self) -> Distance:
        # TODO: Factor out a common base of the combat and non-combat race-tracks.
        # No harm in setting this, but we ought to clean up a bit.
        return meters(0)
