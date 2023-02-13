from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator, Optional

from game.armedforces.forcegroup import ForceGroup


@dataclass(frozen=True)
class TgoConfig:
    by_original_name: dict[str, ForceGroup]

    def __iter__(self) -> Iterator[str]:
        return self.by_original_name.__iter__()

    def __getitem__(self, name: str) -> Optional[ForceGroup]:
        return self.by_original_name.get(name)

    @classmethod
    def from_campaign_data(cls, data: dict[str, str]) -> TgoConfig:
        by_original_name: dict[str, ForceGroup] = defaultdict()
        for tgo_name, force_group in data.items():
            by_original_name[tgo_name] = ForceGroup.from_preset_group(force_group)
        return TgoConfig(by_original_name)
