from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from dcs.mapping import Point
from dcs.unitgroup import StaticGroup, ShipGroup, VehicleGroup

from game.point_with_heading import PointWithHeading
from game.utils import Heading

GroupT = TypeVar("GroupT", StaticGroup, ShipGroup, VehicleGroup)


class PresetLocation(PointWithHeading):
    """Store information about the Preset Location set by the campaign designer"""

    # This allows to store original name and force a specific type or template
    original_name: str  # Store the original name from the campaign miz

    def __init__(
        self, name: str, position: Point, heading: Heading = Heading.from_degrees(0)
    ) -> None:
        super().__init__(position.x, position.y, heading, position._terrain)
        self.original_name = name

    @classmethod
    def from_group(cls, group: GroupT) -> PresetLocation:
        """Creates a PresetLocation from a placeholder group in the campaign miz"""
        preset = PresetLocation(
            group.name,
            group.position,
            Heading.from_degrees(group.units[0].heading),
        )
        return preset


@dataclass(frozen=True)
class ExactSiteUnit:
    """One unit of a hand-placed site, at its absolute campaign-miz position."""

    type_id: str
    position: Point
    heading: float


class ExactSitePreset(PresetLocation):
    """A campaign-miz air-defense group kept exactly as drawn (the FIXED prefix).

    The preset's own point and heading are the group's first unit, so template
    extras added around it are placed the way a marker's would be.
    """

    units: list[ExactSiteUnit]

    def __init__(
        self,
        name: str,
        position: Point,
        heading: Heading,
        units: list[ExactSiteUnit],
    ) -> None:
        super().__init__(name, position, heading)
        self.units = units

    @classmethod
    def from_vehicle_group(cls, group: VehicleGroup) -> ExactSitePreset:
        return ExactSitePreset(
            group.name,
            group.position,
            Heading.from_degrees(group.units[0].heading),
            [
                ExactSiteUnit(
                    unit.type,
                    Point(unit.position.x, unit.position.y, unit.position._terrain),
                    unit.heading,
                )
                for unit in group.units
            ],
        )
