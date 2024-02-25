from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, TYPE_CHECKING

from game.dcs.shipunittype import ShipUnitType

if TYPE_CHECKING:
    pass


@dataclass(frozen=True)
class CarrierConfig:
    preferred_name: str
    preferred_type: ShipUnitType

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> CarrierConfig:
        return CarrierConfig(
            str(data["preferred_name"]), ShipUnitType.named(data["preferred_type"])
        )


@dataclass(frozen=True)
class CampaignCarrierConfig:
    by_original_name: dict[str, CarrierConfig]

    @classmethod
    def from_campaign_data(
        cls, data: dict[str, Any]
    ) -> CampaignCarrierConfig:
        by_original_name: dict[str, CarrierConfig] = defaultdict()
        for original_name, carrier_config_data in data.items():
            try:
                carrier_config = CarrierConfig.from_data(carrier_config_data)
                by_original_name[original_name] = carrier_config
            except KeyError:
                logging.warning(f"Skipping invalid carrier config for '{original_name}'")

        return CampaignCarrierConfig(by_original_name)
