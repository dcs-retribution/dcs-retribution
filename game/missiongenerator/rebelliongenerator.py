from __future__ import annotations

import logging
import random
from typing import TYPE_CHECKING

import numpy as np
import shapely.geometry
from dcs import Mission, Point
from dcs.country import Country
from dcs.triggers import TriggerZone, TriggerZoneCircular, TriggerZoneQuadPoint
from dcs.vehicles import vehicle_map

from game.dcs.groundunittype import GroundUnitType
from game.naming import namegen
from game.theater import Player

if TYPE_CHECKING:
    from game import Game


class RebellionGenerator:
    def __init__(self, mission: Mission, game: Game) -> None:
        self.mission = mission
        self.game = game

    def generate(self) -> None:
        ownfor_country = self.mission.country(
            self.game.coalition_for(player=Player.BLUE).faction.country.name
        )
        for rz in self.game.theater.ownfor_rebel_zones:
            self._generate_rebel_zone(ownfor_country, rz)
        opfor_country = self.mission.country(
            self.game.coalition_for(player=Player.RED).faction.country.name
        )
        for rz in self.game.theater.opfor_rebel_zones:
            self._generate_rebel_zone(opfor_country, rz)

    def _generate_rebel_zone(self, ownfor_country: Country, rz: TriggerZone) -> None:
        for i, key_value_dict in rz.properties.items():
            unit_id = key_value_dict["key"]
            count_range = key_value_dict["value"]
            if unit_id not in vehicle_map:
                logging.warning(
                    f"Invalid unit_id '{unit_id}' in rebel zone '{rz.name}'"
                )
                continue

            count, success = self._get_random_count_for_type(count_range)
            if not success:
                logging.warning(
                    f"Invalid count/range ({count_range}) for '{unit_id}' in rebel-zone '{rz.name}'"
                )
                continue
            unit_type = vehicle_map[unit_id]
            for _ in range(count):
                location = self.get_random_point_in_zone(rz)
                group = self.mission.vehicle_group(
                    ownfor_country,
                    namegen.next_unit_name(
                        ownfor_country, next(GroundUnitType.for_dcs_type(unit_type))
                    ),
                    unit_type,
                    location,
                    heading=random.random() * 360,
                )
                group.hidden_on_mfd = True
                group.hidden_on_planner = True

    def get_random_point_in_zone(self, zone: TriggerZone) -> Point:
        if isinstance(zone, TriggerZoneCircular):
            shape = shapely.geometry.Point(zone.position.x, zone.position.y).buffer(
                zone.radius
            )
        elif isinstance(zone, TriggerZoneQuadPoint):
            shape = shapely.geometry.Polygon([[p.x, p.y] for p in zone.verticies])
        else:
            raise RuntimeError("Incompatible trigger-zone")
        minx, miny, maxx, maxy = shape.bounds
        p = self._random_shapely_point(maxx, maxy, minx, miny)
        while not shape.contains(p):
            p = self._random_shapely_point(maxx, maxy, minx, miny)
        return zone.position.new_in_same_map(p.x, p.y)

    @staticmethod
    def _random_shapely_point(
        maxx: float, maxy: float, minx: float, miny: float
    ) -> shapely.geometry.Point:
        x = np.random.uniform(minx, maxx)
        y = np.random.uniform(miny, maxy)
        p = shapely.geometry.Point(x, y)
        return p

    @staticmethod
    def _get_random_count_for_type(bounds: str) -> tuple[int, bool]:
        parts = bounds.split("-")
        if len(parts) == 1 and parts[0].isdigit():
            return int(parts[0]), True
        elif len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return random.randint(int(parts[0]), int(parts[1])), True
        else:
            return 0, False
