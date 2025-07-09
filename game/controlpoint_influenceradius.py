from __future__ import annotations

from typing import Iterable, List, TYPE_CHECKING
from functools import cached_property

from dcs.mapping import Polygon
from dcs.triggers import TriggerZone, TriggerZoneCircular, TriggerZoneQuadPoint

from game.theater.theatergroundobject import NAME_BY_CATEGORY

if TYPE_CHECKING:
    from dcs.mapping import Point


class ControlPointInfluenceRadiusError(RuntimeError):
    """Error for when there are insufficient conditions to create a ControlPointInfluenceRadius."""

    pass


class ControlPointInfluenceRadius:
    """Store information about a scenery objective."""

    def __init__(self, zone_def: TriggerZone, cp_name: str) -> None:
        self.zone_def = zone_def
        self.position = zone_def.position
        self.cp_name = cp_name

    @staticmethod
    def from_trigger_zones(
        trigger_zones: Iterable[TriggerZone],
    ) -> List[ControlPointInfluenceRadius]:
        """Define scenery objectives based on their encompassing blue/red circle."""
        zone_definitions = []
        cp_influence_zones = []

        for zone in trigger_zones:
            if ControlPointInfluenceRadius.is_red(zone):
                zone_definitions.append(zone)

        # For each objective definition.
        for zone_def in zone_definitions:
            if len(zone_def.properties) == 0:
                raise ControlPointInfluenceRadiusError(
                    "Undefined ControlPointInfluenceRadius category in TriggerZone: "
                    + zone_def.name
                )
            zone_def_cp_name = zone_def.properties[1].get("value")
            cp_influence_zones.append(
                ControlPointInfluenceRadius(zone_def, zone_def_cp_name)
            )
        return cp_influence_zones

    @staticmethod
    def is_red(zone: TriggerZone) -> bool:
        # Red in RGB is [1 Red], [0 Green], [0 Blue]. Ignore the fourth position: Transparency.
        return zone.color[1] == 1 and zone.color[2] == 0 and zone.color[3] == 0


def point_in_zone(zone: TriggerZone, pos: Point) -> bool:
    if isinstance(zone, TriggerZoneCircular):
        return zone.position.distance_to_point(pos) < zone.radius
    elif isinstance(zone, TriggerZoneQuadPoint):
        return Polygon(pos._terrain, zone.verticies).point_in_poly(pos)
    raise RuntimeError(f"Invalid trigger-zone: {zone.name}")
