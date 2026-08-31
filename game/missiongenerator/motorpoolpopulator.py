from __future__ import annotations

import math
from typing import TYPE_CHECKING

from game.dcs.groundunittype import GroundUnitType
from game.ground_forces.ai_ground_planner import reserve_armor_for
from game.theater.theatergroup import TheaterGroup, TheaterUnit
from game.theater.theatergroundobject import MotorpoolGroundObject
from game.point_with_heading import PointWithHeading

if TYPE_CHECKING:
    from game.game import Game

# Parked vehicles laid in a grid so DCS does not reject overlapping spawns.
_SPACING_M = 12.0
_COLUMNS = 5
# Keep the Garage_A building at the authored marker; start vehicles clear of it
# behind the building. 150 ft is the authoring-friendly value.
_GRID_OFFSET_M = 45.72


def _select_capped(
    reserve: dict[GroundUnitType, int], cap: int
) -> dict[GroundUnitType, int]:
    """Proportionally reduce ``reserve`` so its counts sum to at most ``cap``,
    using the largest-remainder method (keeps a representative spread of types).
    Returns a copy of ``reserve`` unchanged when it already fits under the cap."""
    total = sum(reserve.values())
    if total <= cap:
        return {ut: n for ut, n in reserve.items() if n > 0}
    exact = {ut: count * cap / total for ut, count in reserve.items()}
    floors = {ut: int(v) for ut, v in exact.items()}
    remaining = cap - sum(floors.values())
    if remaining > 0:
        by_frac = sorted(
            ((ut, exact[ut] - floors[ut]) for ut in reserve),
            key=lambda kv: kv[1],
            reverse=True,
        )
        for ut, _frac in by_frac[:remaining]:
            floors[ut] += 1
    return {ut: n for ut, n in floors.items() if n > 0}


def motorpool_full_grid_extent_m() -> float:
    """Distance from the garage origin to the furthest slot of a full grid."""
    last_row = _COLUMNS - 1
    last_column = _COLUMNS - 1
    return math.hypot(_GRID_OFFSET_M + last_row * _SPACING_M, last_column * _SPACING_M)


def _projected_counts(
    motorpools: list[MotorpoolGroundObject], cap: int
) -> list[dict[GroundUnitType, int]]:
    reserve = reserve_armor_for(motorpools[0].control_point)
    selected = _select_capped(reserve, cap)
    per_tgo: list[dict[GroundUnitType, int]] = [{} for _ in motorpools]
    slot = 0
    for unit_type, count in selected.items():
        for _ in range(count):
            bucket = per_tgo[slot % len(motorpools)]
            bucket[unit_type] = bucket.get(unit_type, 0) + 1
            slot += 1
    return per_tgo


def motorpool_rendered_unit_count(
    tgo: MotorpoolGroundObject, motorpool_enabled: bool, spawn_cap: int
) -> int:
    """Return the units in the renderer's next snapshot.

    Project the same capped reserve allocation that ``MotorpoolPopulator`` will
    render, regardless of the previous mission's ephemeral groups.
    """
    if not motorpool_enabled or spawn_cap <= 0:
        return 0
    motorpools = [
        candidate
        for candidate in tgo.control_point.ground_objects
        if isinstance(candidate, MotorpoolGroundObject)
    ]
    if tgo not in motorpools:
        return 0
    return sum(_projected_counts(motorpools, spawn_cap)[motorpools.index(tgo)].values())


class MotorpoolPopulator:
    """Rebuilds every motorpool TGO's vehicle groups from the owning CP's current
    reserve slice. Ephemeral: called once per mission generation, before the TGO
    generator renders. Nothing it writes is meant to survive the turn."""

    def __init__(self, game: Game) -> None:
        self.game = game

    def populate(self) -> None:
        cap: int = self.game.settings.motorpool_spawn_cap
        enabled: bool = self.game.settings.motorpool_enabled
        for cp in self.game.theater.controlpoints:
            motorpools = [
                tgo
                for tgo in cp.ground_objects
                if isinstance(tgo, MotorpoolGroundObject)
            ]
            for tgo in motorpools:
                tgo.groups = []
                tgo.motorpool_unit_types = {}
            if not enabled or cap <= 0 or not motorpools:
                continue
            self._populate_cp(motorpools, cap)

    def _populate_cp(self, motorpools: list[MotorpoolGroundObject], cap: int) -> None:
        # Every motorpool on a CP draws from the SAME reserve pool, so compute it
        # once and deal the capped selection round-robin across them. Populating
        # each TGO with the full reserve independently would render — and on a
        # strike decrement — the same reserve unit once per TGO, corrupting
        # base.armor when a CP has more than one authored motorpool location.
        for tgo, counts in zip(motorpools, _projected_counts(motorpools, cap)):
            self._build_groups(tgo, counts)

    def _build_groups(
        self, tgo: MotorpoolGroundObject, counts: dict[GroundUnitType, int]
    ) -> None:
        index = 0
        for unit_type, count in counts.items():
            units: list[TheaterUnit] = []
            for _ in range(count):
                units.append(self._make_unit(tgo, unit_type, index))
                index += 1
            group = TheaterGroup.from_template(
                self.game.next_group_id(),
                f"{tgo.name} ({unit_type})",
                units,
                tgo,
            )
            tgo.groups.append(group)
            tgo.motorpool_unit_types[group.id] = unit_type

    def _make_unit(
        self, tgo: MotorpoolGroundObject, unit_type: GroundUnitType, index: int
    ) -> TheaterUnit:
        origin = tgo.position
        # Park behind the garage: the first row is offset opposite its heading and
        # each additional row continues farther in that direction. Within a row,
        # vehicles are spaced along the garage's right-hand side.
        behind = tgo.heading.opposite.degrees
        lateral = tgo.heading.right.degrees
        pos = origin.point_from_heading(
            behind, _GRID_OFFSET_M + (index // _COLUMNS) * _SPACING_M
        ).point_from_heading(lateral, (index % _COLUMNS) * _SPACING_M)
        pos = PointWithHeading.from_point(pos, tgo.heading)
        return TheaterUnit(
            self.game.next_unit_id(),
            str(unit_type),
            unit_type.dcs_unit_type,
            pos,
            tgo,
        )
