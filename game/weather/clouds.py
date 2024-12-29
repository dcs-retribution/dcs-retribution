from __future__ import annotations

import random
from dataclasses import dataclass, field
from math import ceil, floor
from typing import Optional

from dcs.cloud_presets import CLOUD_PRESETS
from dcs.weather import Weather as PydcsWeather, CloudPreset


@dataclass(frozen=True)
class Clouds:
    base: int
    density: int
    thickness: int
    precipitation: PydcsWeather.Preceptions
    preset: Optional[CloudPreset] = field(default=None)

    @classmethod
    def random_preset(cls, rain: bool) -> Clouds:
        clouds = (p.value for _, p in CLOUD_PRESETS.items())
        if rain:
            presets = [p for p in clouds if "Rain" in p.name]
        else:
            presets = [p for p in clouds if "Rain" not in p.name]
        preset = random.choice(presets)
        return Clouds(
            base=random.randint(ceil(preset.min_base), floor(preset.max_base)),
            density=0,
            thickness=0,
            precipitation=PydcsWeather.Preceptions.None_,
            preset=preset,
        )
