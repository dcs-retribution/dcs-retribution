from __future__ import annotations

from typing import TYPE_CHECKING

from game.dcs.groundunittype import GroundUnitType
from game.theater.theatergroup import TheaterGroup, TheaterUnit
from game.theater.theatergroundobject import (
    MotorpoolGroundObject,
    motorpool_projected_counts,
)
from game.point_with_heading import PointWithHeading

if TYPE_CHECKING:
    from game.game import Game

# Parked vehicles laid in a grid so DCS does not reject overlapping spawns.
_SPACING_M = 12.0
_COLUMNS = 5
# Keep the Garage_A building at the authored marker; start vehicles clear of it
# behind the building. 150 ft is the authoring-friendly value.
_GRID_OFFSET_M = 45.72


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
        for tgo, counts in zip(motorpools, motorpool_projected_counts(motorpools, cap)):
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
