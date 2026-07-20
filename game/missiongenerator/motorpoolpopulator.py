from __future__ import annotations

from typing import TYPE_CHECKING

from dcs.mapping import Point

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
        reserve = reserve_armor_for(motorpools[0].control_point)
        selected = _select_capped(reserve, cap)
        if not selected:
            return
        per_tgo: list[dict[GroundUnitType, int]] = [{} for _ in motorpools]
        slot = 0
        for unit_type, count in selected.items():
            for _ in range(count):
                bucket = per_tgo[slot % len(motorpools)]
                bucket[unit_type] = bucket.get(unit_type, 0) + 1
                slot += 1
        for tgo, counts in zip(motorpools, per_tgo):
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
        dx = (index % _COLUMNS) * _SPACING_M
        dy = (index // _COLUMNS) * _SPACING_M
        # Lay the grid in the garage's local frame, then rotate it clockwise about
        # the TGO origin so the parking lot follows the Garage_A heading (as
        # resource-site placement does). At heading 0 the rotation is a no-op and
        # the grid stays world-axis-aligned.
        pos = PointWithHeading.from_point(
            Point(origin.x + dx, origin.y + dy, origin._terrain), tgo.heading
        )
        pos.rotate(origin, tgo.heading)
        return TheaterUnit(
            self.game.next_unit_id(),
            str(unit_type),
            unit_type.dcs_unit_type,
            pos,
            tgo,
        )
