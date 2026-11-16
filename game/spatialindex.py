from __future__ import annotations

import math


class LiveUnitIndex:
    """Point-proximity test over a fixed set of 2-D positions.

    Buckets positions on an R-size grid; a query scans its own bucket plus the
    eight neighbours (a point within R is at most one R-size bucket away on each
    axis) and confirms with an exact distance check.
    """

    def __init__(self, positions: list[tuple[float, float]], radius: float) -> None:
        self._radius = radius
        self._buckets: dict[tuple[int, int], list[tuple[float, float]]] = {}
        for x, z in positions:
            # A non-finite position (inf/nan) isn't anywhere; skip it rather than
            # let math.floor(x / radius) raise (OverflowError on inf, ValueError on
            # nan) and abort construction.
            if not (math.isfinite(x) and math.isfinite(z)):
                continue
            self._buckets.setdefault(self._cell(x, z), []).append((x, z))

    def _cell(self, x: float, z: float) -> tuple[int, int]:
        return (math.floor(x / self._radius), math.floor(z / self._radius))

    def occupied(self, x: float, z: float) -> bool:
        if not (math.isfinite(x) and math.isfinite(z)):
            return False
        cx, cz = self._cell(x, z)
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                for px, pz in self._buckets.get((cx + dx, cz + dz), ()):
                    if math.hypot(px - x, pz - z) <= self._radius:
                        return True
        return False
