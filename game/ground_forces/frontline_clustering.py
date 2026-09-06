"""Pure, game-object-free helpers for frontline cluster planning.

Kept dependency-free (no imports from game.*) so the planner can import these
without a circular dependency and so they are trivially unit-testable.
"""

from __future__ import annotations

import math
from typing import TypeVar

T = TypeVar("T")


def allocate_largest_remainder(weights: dict[T, float], total: int) -> dict[T, int]:
    """Distribute integer units across keys proportional to ``weights``.

    Allocates ``min(total, round(sum(weights)))`` units. Each key gets the floor
    of its proportional share; the leftover units go to the keys with the largest
    fractional remainders. Guarantees the returned counts sum to the target.
    """
    if not weights:
        return {}
    weight_sum = sum(weights.values())
    if weight_sum <= 0:
        return {key: 0 for key in weights}
    target = min(total, round(weight_sum))
    if target <= 0:
        return {key: 0 for key in weights}

    exact = {key: value / weight_sum * target for key, value in weights.items()}
    floored = {key: math.floor(value) for key, value in exact.items()}
    remainder = target - sum(floored.values())
    # Hand out the remaining units to the largest fractional parts first.
    by_frac = sorted(
        exact, key=lambda k: (exact[k] - floored[k], weights[k]), reverse=True
    )
    for key in by_frac[:remainder]:
        floored[key] += 1
    return floored


def even_slot_centers(count: int, size: int) -> list[float]:
    """Return ``count`` evenly-spaced centers across the segment ``[0, size]``."""
    if count <= 0:
        return []
    step = size / count
    return [(i + 0.5) * step for i in range(count)]
