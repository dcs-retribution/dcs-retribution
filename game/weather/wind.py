from __future__ import annotations

from dataclasses import dataclass

from dcs.weather import Wind

from game.utils import Speed, knots

# DCS itself will not model more than this, so anything above it is silently
# meaningless in the mission.
MAX_WIND_SPEED: Speed = knots(97)


@dataclass(frozen=True)
class WindConditions:
    at_0m: Wind
    at_2000m: Wind
    at_8000m: Wind
