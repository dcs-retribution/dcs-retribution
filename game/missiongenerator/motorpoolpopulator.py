from __future__ import annotations

from typing import TYPE_CHECKING

from game.point_with_heading import PointWithHeading

from game.dcs.groundunittype import GroundUnitType
from game.ground_forces.ai_ground_planner import reserve_armor_for
from game.theater.controlpoint import ControlPoint, ControlPointType
from game.theater.theatergroup import TheaterGroup, TheaterUnit
from game.theater.theatergroundobject import MotorpoolGroundObject

if TYPE_CHECKING:
    from game.game import Game
    from game.sim.gameupdateevents import GameUpdateEvents

# Parked vehicles laid in a grid so DCS does not reject overlapping spawns.
_SPACING_M = 12.0
_COLUMNS = 5
# Keep the Garage_A building at the authored marker; start vehicles clear of it
# behind the building. 150 ft is the authoring-friendly value.
_GRID_OFFSET_M = 45.72

MotorpoolIdentity = tuple[str, float, float, float]


def motorpool_identity(
    original_name: str, location: PointWithHeading
) -> MotorpoolIdentity:
    return (original_name, location.x, location.y, location.heading.degrees)


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

    def _rehome_motorpools(self, events: GameUpdateEvents | None = None) -> None:
        """Attach each motorpool to its nearest eligible land control point.

        Motorpool ownership is persisted as which control point's
        ``connected_objectives`` the TGO lives in, so an existing save can park a
        motorpool under the wrong (possibly enemy) base and nothing re-decides it.
        FARPs/FOBs are themselves land control points with their own separate
        ground inventory, so a motorpool parked at a FARP belongs to that FARP --
        not to a far-away base whose influence zone happens to contain the point.

        This pass runs during migration before ordinary population, converting
        existing saves on load without changing mission-generation behavior.
        Naval and off-map control points never own motorpools.
        """
        control_points = self.game.theater.controlpoints
        eligible: list[ControlPoint] = []
        for cp in control_points:
            if getattr(cp, "cptype", None) in (
                ControlPointType.AIRCRAFT_CARRIER_GROUP,
                ControlPointType.LHA_GROUP,
                ControlPointType.OFF_MAP,
            ):
                continue
            if getattr(cp, "position", None) is None:
                continue
            eligible.append(cp)
        # Gather the complete current authored marker set first.  Persisted TGOs
        # are projections of these markers; an identity absent from the set was
        # removed from the campaign and must not survive migration.
        authored: set[MotorpoolIdentity] = {
            motorpool_identity(location.original_name, location)
            for owner in control_points
            for location in getattr(owner.preset_locations, "motorpools", [])
        }

        # Gather each authored TGO once, even if a malformed save references it
        # from more than one control point.  The first instance for a marker
        # identity wins; all duplicate references/objects are discarded below.
        motorpools: dict[MotorpoolIdentity, MotorpoolGroundObject] = {}
        for owner in control_points:
            for tgo in getattr(owner, "connected_objectives", []):
                if not isinstance(tgo, MotorpoolGroundObject):
                    continue
                identity = (
                    tgo.original_name,
                    tgo.position.x,
                    tgo.position.y,
                    tgo.heading.degrees,
                )
                if identity in authored:
                    motorpools.setdefault(identity, tgo)

        for owner in control_points:
            owner.connected_objectives[:] = [
                tgo
                for tgo in owner.connected_objectives
                if not isinstance(tgo, MotorpoolGroundObject)
            ]

        if not eligible:
            for tgo in motorpools.values():
                tgo.control_point.connected_objectives.append(tgo)
            return

        for tgo in motorpools.values():
            previous_owner = tgo.control_point
            closest = min(
                eligible,
                key=lambda cp: cp.position.distance_to_point(tgo.position),
            )
            closest.connected_objectives.append(tgo)
            tgo.control_point = closest
            if events is not None and closest is not previous_owner:
                events.update_tgo(tgo)

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
