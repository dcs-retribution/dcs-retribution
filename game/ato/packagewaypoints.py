from __future__ import annotations

import random
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from dcs import Point

from game.ato.flightplans.waypointbuilder import WaypointBuilder
from game.flightplan import IpZoneGeometry, JoinZoneGeometry
from game.flightplan.refuelzonegeometry import RefuelZoneGeometry
from game.utils import nautical_miles

if TYPE_CHECKING:
    from game.ato import Package
    from game.coalition import Coalition


@dataclass(frozen=True)
class PackageWaypoints:
    join: Point
    ingress: Point
    initial: Point
    split: Point
    refuel: Point

    @staticmethod
    def create(package: Package, coalition: Coalition) -> PackageWaypoints:
        origin = package.departure_closest_to_target()

        # Start by picking the best IP for the attack.
        ingress_point = IpZoneGeometry(
            package.target.position,
            origin.position,
            coalition,
        ).find_best_ip()

        hdg = package.target.position.heading_between_point(ingress_point)
        dist = nautical_miles(random.random() * 2 + 7).meters
        initial_point = package.target.position.point_from_heading(hdg, dist)

        join_point = JoinZoneGeometry(
            package.target.position,
            origin.position,
            ingress_point,
            coalition,
        ).find_best_join_point()

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
        )
