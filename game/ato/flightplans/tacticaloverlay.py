from __future__ import annotations

import abc
import math
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from dcs import Point
from shapely.geometry import LineString, Point as ShapelyPoint, Polygon
from shapely.ops import unary_union

from game.utils import Distance, Speed, meters


@dataclass(frozen=True)
class ReachShape:
    """Engagement geometry. filled=True -> shaded 'actually projected';
    filled=False -> outline-only 'planned but barely used'."""

    geometry: Polygon
    filled: bool


@dataclass(frozen=True)
class TacticalTarget:
    position: Point


@dataclass(frozen=True)
class TacticalOverlay:
    """What an AI flight actually does, for honest map rendering."""

    reach: list[ReachShape] = field(default_factory=list)
    actual_path: list[Point] | None = None
    targets: list[TacticalTarget] = field(default_factory=list)


class TacticalOverlayDisplay(abc.ABC):
    @abc.abstractmethod
    def tactical_overlay(self) -> TacticalOverlay: ...


# ---- pure geometry helpers (all in DCS x/y meter space) ----


def reach_circle(center: Point, radius: Distance) -> Polygon:
    return ShapelyPoint(center.x, center.y).buffer(radius.meters)


def asymmetric_capsule(a: Point, b: Point, r_a: Distance, r_b: Distance) -> Polygon:
    """Convex hull of two disks of differing radii -> a stadium fat at one end."""
    disk_a = ShapelyPoint(a.x, a.y).buffer(r_a.meters)
    disk_b = ShapelyPoint(b.x, b.y).buffer(r_b.meters)
    return unary_union([disk_a, disk_b]).convex_hull


def reach_corridor(points: list[Point], radius: Distance) -> Polygon:
    return LineString([(p.x, p.y) for p in points]).buffer(radius.meters)


def orbit_loop(center: Point, radius: Distance, segments: int = 24) -> list[Point]:
    r = radius.meters
    return [
        center.new_in_same_map(
            center.x + r * math.cos(2 * math.pi * i / segments),
            center.y + r * math.sin(2 * math.pi * i / segments),
        )
        for i in range(segments + 1)
    ]


def orbit_radius(speed: Speed, bank_deg: float = 25.0) -> Distance:
    """Level-turn radius r = v^2 / (g * tan(bank))."""
    v = speed.meters_per_second
    return meters(v * v / (9.81 * math.tan(math.radians(bank_deg))))


def attack_run_overlay(
    ingress: Point, target_position: Point, split: Point
) -> TacticalOverlay:
    return TacticalOverlay(
        reach=[],
        actual_path=[ingress, target_position, split],
        targets=[TacticalTarget(position=target_position)],
    )


if TYPE_CHECKING:
    from game.ato.flightplans.patrolling import PatrollingFlightPlan


def _orbit_anchor(
    flight_plan: "PatrollingFlightPlan[Any]",
) -> Point:
    # Confirmed in-DCS: CAP orbits the END (discrepancy log D6).
    return flight_plan.layout.patrol_end.position


def cap_overlay(
    flight_plan: "PatrollingFlightPlan[Any]",
) -> TacticalOverlay:
    anchor = _orbit_anchor(flight_plan)
    eng = flight_plan.engagement_distance
    r_orbit = orbit_radius(flight_plan.patrol_speed)
    far = meters(eng.meters + r_orbit.meters)
    outline = asymmetric_capsule(
        flight_plan.layout.patrol_start.position, anchor, eng, far
    )
    return TacticalOverlay(
        reach=[
            ReachShape(geometry=outline, filled=False),
            ReachShape(geometry=reach_circle(anchor, far), filled=True),
        ],
        actual_path=orbit_loop(anchor, r_orbit),
    )


def loiter_overlay(
    orbit_center: Point,
    loiter_radius: Distance,
    engagement_center: Point,
    engagement_range: Distance,
    target_position: Point,
) -> TacticalOverlay:
    """Loiter-and-react overlay: an orbit ring at the standoff loiter point, a
    filled engagement bubble, and the revealed target. Used by the SEAD family,
    which orbits at standoff and engages air-defence radars reactively."""
    return TacticalOverlay(
        reach=[
            ReachShape(
                geometry=reach_circle(engagement_center, engagement_range), filled=True
            )
        ],
        actual_path=orbit_loop(orbit_center, loiter_radius),
        targets=[TacticalTarget(position=target_position)],
    )


def escort_overlay(route: list[Point], engagement_range: Distance) -> TacticalOverlay:
    return TacticalOverlay(
        reach=[
            ReachShape(geometry=reach_corridor(route, engagement_range), filled=True)
        ],
    )


def cas_overlay(
    patrol_start: Point, patrol_end: Point, engagement_range: Distance
) -> TacticalOverlay:
    # Loiters ALONG the front line, so the reach is a corridor down the FLOT
    # bounds, not a single circle at the midpoint.
    return TacticalOverlay(
        reach=[
            ReachShape(
                geometry=reach_corridor([patrol_start, patrol_end], engagement_range),
                filled=True,
            )
        ],
    )
