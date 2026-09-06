from __future__ import annotations

from datetime import datetime, timedelta

from dcs.point import MovingPoint
from dcs.task import OrbitAction

from game.ato.flightplans.sead import SeadFlightPlan
from game.utils import meters
from .pydcswaypointbuilder import PydcsWaypointBuilder


def _loiter_stop_seconds(loiter_end: datetime, now: datetime) -> int:
    """Mission-elapsed seconds at which the loiter orbit is force-stopped.

    `loiter_end` is the absolute mission time the loiter should break off
    (`SeadFlightPlan.loiter_end_time`). Floored at 1 s so an end time at or before
    mission start can never produce a stop time of 0, which DCS treats as "fire
    immediately" and would kill the orbit at mission start.
    """
    return max(1, int((loiter_end - now).total_seconds()))


class SeadLoiterBuilder(PydcsWaypointBuilder):
    """Plain-SEAD standoff loiter: the flight holds here and engages radars
    reactively (via the SEAD main task) until it RTBs on winchester. The orbit is
    bounded by a computed window (the latest a package-mate leaves the target area) so
    it never loiters forever."""

    def add_tasks(self, waypoint: MovingPoint) -> None:
        # Base add_tasks only injects an AI-despawn RunScript at the *arrival*
        # waypoint; this anchor is not the arrival, so it is a no-op here.
        super().add_tasks(waypoint)
        flight_plan = self.flight.flight_plan
        if isinstance(flight_plan, SeadFlightPlan):
            loiter_end = flight_plan.loiter_end_time
        else:
            # A user who edits a SEAD flight's waypoints degrades it to a
            # CustomFlightPlan, but the SEAD_LOITER waypoint survives and still routes
            # here -- and a custom plan has no loiter_end_time. Fall back to the
            # configured window so we still emit a valid, bounded orbit (mirrors how
            # HoldPointBuilder guards against a degraded plan type).
            window = self.flight.coalition.game.settings.sead_loiter_max_window_seconds
            loiter_end = self.now + timedelta(seconds=window)
        stop = _loiter_stop_seconds(loiter_end, self.now)
        speed = self.flight.squadron.aircraft.preferred_patrol_speed(
            meters(waypoint.alt)
        )
        self.add_stopping_orbit(
            waypoint,
            speed_kph=speed.kph,
            pattern=OrbitAction.OrbitPattern.Circle,
            stop_time=stop,
        )
