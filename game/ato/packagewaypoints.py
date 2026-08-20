from __future__ import annotations

import random
from dataclasses import dataclass, replace
from typing import Optional, TYPE_CHECKING

from dcs import Point

from game.ato.flightplans.waypointbuilder import WaypointBuilder
from game.data.doctrine import Doctrine
from game.flightplan import JoinZoneGeometry
from game.flightplan.ipsolver import IpSolver
from game.flightplan.refuelzonegeometry import RefuelZoneGeometry
from game.persistency import waypoint_debug_directory
from game.utils import Distance, dcs_to_shapely_point
from game.utils import meters, nautical_miles

if TYPE_CHECKING:
    from game.ato import Package
    from game.coalition import Coalition


@dataclass
class PackageWaypoints:
    join: Point
    ingress: Point
    initial: Point
    split: Point
    refuel: Point

    #: The package's longest stand-off launch range at the time these waypoints were
    #: built. Used to detect when a payload change invalidates the ingress point.
    standoff_range: Optional[Distance] = None

    @staticmethod
    def doctrine_for_standoff_range(
        doctrine: Doctrine,
        standoff_range: Optional[Distance],
        distance_to_target: Distance,
    ) -> Doctrine:
        """Raise the doctrine's max ingress distance to the given stand-off range.

        Cruise/stand-off-armed flights (e.g. Tu-16s with Kh-22s) should begin their
        attack run from a realistic launch distance instead of being dragged all the
        way in to the doctrine ingress point. The override is capped at the
        departure-target distance: some IpSolver strategies (the backtracking
        fallbacks used when the primary ones find no safe IP) do not otherwise bound
        the search area, and a 100+ nm cruise-missile range on a much shorter route
        could send the IP far off the route or off the map.
        """
        if standoff_range is None:
            return doctrine
        effective_max_ingress = min(standoff_range, distance_to_target)
        if effective_max_ingress <= doctrine.max_ingress_distance:
            return doctrine
        return replace(doctrine, max_ingress_distance=effective_max_ingress)

    @staticmethod
    def create(
        package: Package, coalition: Coalition, dump_debug_info: bool
    ) -> PackageWaypoints:
        origin = package.departure_closest_to_target()

        standoff_range = package.max_standoff_range()
        distance_to_target = meters(
            origin.position.distance_to_point(package.target.position)
        )
        doctrine = PackageWaypoints.doctrine_for_standoff_range(
            coalition.doctrine, standoff_range, distance_to_target
        )

        # Start by picking the best IP for the attack.
        ip_solver = IpSolver(
            dcs_to_shapely_point(origin.position),
            dcs_to_shapely_point(package.target.position),
            doctrine,
            coalition.opponent.threat_zone.air_defenses,
        )
        ip_solver.set_debug_properties(
            waypoint_debug_directory() / "IP", coalition.game.theater.terrain
        )
        ingress_point_shapely = ip_solver.solve()
        if dump_debug_info:
            ip_solver.dump_debug_info()

        ingress_point = origin.position.new_in_same_map(
            ingress_point_shapely.x, ingress_point_shapely.y
        )

        tgt_point = package.target.position
        initial_point = PackageWaypoints.get_initial_point(ingress_point, tgt_point)

        join_point = JoinZoneGeometry(
            package.target.position,
            origin.position,
            ingress_point,
            coalition,
        ).find_best_join_point()

        # Join/split are derived from this base join_point. JoinZoneGeometry
        # fixes the base join distance between 35% and 36% of the home-to-target
        # leg, and WaypointBuilder.perturb then applies a small offset to
        # produce the final join/split waypoints.

        refuel_point = RefuelZoneGeometry(
            origin.position,
            join_point,
            coalition,
        ).find_best_refuel_point()

        # And the split point based on the best route from the IP. Since that's no
        # different than the best route *to* the IP, this is the same as the join point.
        # TODO: Estimate attack completion point based on the IP and split from there?
        return PackageWaypoints(
            WaypointBuilder.perturb(join_point),
            ingress_point,
            initial_point,
            WaypointBuilder.perturb(join_point),
            refuel_point,
            standoff_range,
        )

    @staticmethod
    def get_initial_point(ingress_point: Point, tgt_point: Point) -> Point:
        hdg = tgt_point.heading_between_point(ingress_point)
        # Generate a waypoint randomly between 7 & 9 NM
        dist = nautical_miles(random.random() * 2 + 7).meters
        initial_point = tgt_point.point_from_heading(hdg, dist)
        return initial_point
