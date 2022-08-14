from __future__ import annotations
from typing import Iterable, List

from dcs.triggers import TriggerZone, TriggerZoneCircular, TriggerZoneQuadPoint

from game.theater.theatergroundobject import NAME_BY_CATEGORY


def _deduce_radius_from_quad(tz: TriggerZoneQuadPoint) -> float:
    pos = tz.position
    radius = 0.0
    mids = []
    for i in range(len(tz.verticies)):
        for j in range(i, len(tz.verticies)):
            if i is j:
                continue
            mids.append(tz.verticies[i].midpoint(tz.verticies[j]))
    for point in mids:
        dist = pos.distance_to_point(point)
        if dist > radius:
            radius = dist
    return radius


class SceneryGroupError(RuntimeError):
    """Error for when there are insufficient conditions to create a SceneryGroup."""

    pass


class SceneryGroup:
    """Store information about a scenery objective."""

    def __init__(
        self, zone_def: TriggerZone, zones: Iterable[TriggerZone], category: str
    ) -> None:

        self.zone_def = zone_def
        self.zones = zones
        self.position = zone_def.position
        self.category = category

    @staticmethod
    def from_trigger_zones(trigger_zones: Iterable[TriggerZone]) -> List[SceneryGroup]:
        """Define scenery objectives based on their encompassing blue/red circle."""
        zone_definitions = []
        white_zones = []

        scenery_groups = []

        # Aggregate trigger zones into different groups based on color.
        for zone in trigger_zones:
            if SceneryGroup.is_blue(zone):
                zone_definitions.append(zone)
            if SceneryGroup.is_white(zone):
                white_zones.append(zone)

        # For each objective definition.
        for zone_def in zone_definitions:
            if isinstance(zone_def, TriggerZoneCircular):
                zone_def_radius = zone_def.radius
            elif isinstance(zone_def, TriggerZoneQuadPoint):
                zone_def_radius = _deduce_radius_from_quad(zone_def)
            else:
                raise RuntimeError(f"Invalid trigger-zone: {zone_def}")
            print(zone_def_radius, zone_def.__dict__)
            zone_def_position = zone_def.position
            zone_def_name = zone_def.name

            if len(zone_def.properties) == 0:
                raise SceneryGroupError(
                    "Undefined SceneryGroup category in TriggerZone: " + zone_def_name
                )

            # Arbitrary campaign design requirement:  First property must define the category.
            zone_def_category = zone_def.properties[1].get("value").lower()

            valid_white_zones = []

            for zone in list(white_zones):
                if zone.position.distance_to_point(zone_def_position) < zone_def_radius:
                    valid_white_zones.append(zone)
                    white_zones.remove(zone)

            if len(valid_white_zones) > 0 and zone_def_category in NAME_BY_CATEGORY:
                scenery_groups.append(
                    SceneryGroup(zone_def, valid_white_zones, zone_def_category)
                )
            elif len(valid_white_zones) == 0:
                raise SceneryGroupError(
                    "No white triggerzones found in: " + zone_def_name
                )
            elif zone_def_category not in NAME_BY_CATEGORY:
                raise SceneryGroupError(
                    "Incorrect TriggerZone category definition for: "
                    + zone_def_name
                    + " in campaign definition.  TriggerZone category: "
                    + zone_def_category
                )

        return scenery_groups

    @staticmethod
    def is_blue(zone: TriggerZone) -> bool:
        # Blue in RGB is [0 Red], [0 Green], [1 Blue]. Ignore the fourth position: Transparency.
        return zone.color[1] == 0 and zone.color[2] == 0 and zone.color[3] == 1

    @staticmethod
    def is_white(zone: TriggerZone) -> bool:
        # White in RGB is [1 Red], [1 Green], [1 Blue]. Ignore the fourth position: Transparency.
        return zone.color[1] == 1 and zone.color[2] == 1 and zone.color[3] == 1
