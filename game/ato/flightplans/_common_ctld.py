from __future__ import annotations

import random
from typing import Union, TYPE_CHECKING, Tuple

from game.theater.interfaces.CTLD import CTLD

if TYPE_CHECKING:
    from dcs import Point

    from game.theater import ControlPoint


def generate_random_ctld_point(cp: Union[ControlPoint, CTLD]) -> Point:
    if isinstance(cp, CTLD) and cp.ctld_zones:
        zone: Tuple[Point, float] = random.choice(cp.ctld_zones)
        pos, radius = zone
        return pos.random_point_within(radius)
    elif isinstance(cp, CTLD) and isinstance(cp, ControlPoint):
        return cp.position.random_point_within(2000, 200)
    raise RuntimeError("Could not generate CTLD point")
