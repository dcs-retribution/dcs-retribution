from __future__ import annotations

import logging

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Optional, TYPE_CHECKING, Union

from game.ato.flighttype import FlightType
from game.theater.controlpoint import ControlPoint

if TYPE_CHECKING:
    from game.theater import ConflictTheater


DEFAULT_SQUADRON_SIZE = 12


@dataclass(frozen=True)
class SquadronConfig:
    primary: FlightType
    secondary: list[FlightType]
    aircraft: list[str]
    max_size: int

    name: Optional[str]
    nickname: Optional[str]
    female_pilot_percentage: Optional[int]

    @property
    def auto_assignable(self) -> set[FlightType]:
        return set(self.secondary) | {self.primary}

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> SquadronConfig:
        secondary_raw = data.get("secondary")
        if secondary_raw is None:
            secondary = []
        elif isinstance(secondary_raw, str):
            secondary = cls.expand_secondary_alias(secondary_raw)
        else:
            secondary = [FlightType(s) for s in secondary_raw]

        max_size = data.get("size", DEFAULT_SQUADRON_SIZE)

        return SquadronConfig(
            FlightType(data["primary"]),
            secondary,
            data.get("aircraft", []),
            max_size,
            data.get("name", None),
            data.get("nickname", None),
            data.get("female_pilot_percentage", None),
        )

    @staticmethod
    def expand_secondary_alias(alias: str) -> list[FlightType]:
        if alias == "any":
            return list(FlightType)
        elif alias == "air-to-air":
            return [t for t in FlightType if t.is_air_to_air]
        elif alias == "air-to-ground":
            return [t for t in FlightType if t.is_air_to_ground]
        raise KeyError(f"Unknown secondary mission type: {alias}")


@dataclass(frozen=True)
class CampaignAirWingConfig:
    by_location: dict[ControlPoint, list[SquadronConfig]]

    @classmethod
    def from_campaign_data(
        cls, data: dict[Union[str, int], Any], theater: ConflictTheater
    ) -> CampaignAirWingConfig:
        by_location: dict[ControlPoint, list[SquadronConfig]] = defaultdict(list)
        carriers = theater.find_carriers()
        lhas = theater.find_lhas()
        for base_id, squadron_configs in data.items():
            base: Optional[ControlPoint] = None
            if isinstance(base_id, int):
                base = theater.find_control_point_by_airport_id(base_id)
            else:
                try:
                    base = theater.control_point_named(base_id)
                except:
                    if base_id == "Red CV":
                        base = next((c for c in carriers if not c.captured), None)
                    elif base_id == "Blue CV":
                        base = next((c for c in carriers if c.captured), None)
                    elif base_id == "Red LHA":
                        base = next((l for l in lhas if not l.captured), None)
                    elif base_id == "Blue LHA":
                        base = next((l for l in lhas if l.captured), None)

            for squadron_data in squadron_configs:
                if base is None:
                    logging.warning(
                        f"Skipping squadron config for unknown base: {base_id}"
                    )
                else:
                    by_location[base].append(SquadronConfig.from_data(squadron_data))

        return CampaignAirWingConfig(by_location)
