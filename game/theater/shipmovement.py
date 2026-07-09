"""End-of-turn movement + re-parenting for movable ship TGOs.

Carriers apply their movement inside ControlPoint.process_turn, but ships
re-parent to a new owner, so a per-CP loop is wrong. This theater-level pass
runs from Game.finish_turn AFTER mission-results processing (and therefore
after captures are committed), so re-parenting sees post-capture ownership.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from game.theater.theatergroundobject import ShipGroundObject

if TYPE_CHECKING:
    from game.theater.controlpoint import ControlPoint


def move_and_reparent_ships(control_points: list[ControlPoint]) -> None:
    # Collect first: we mutate connected_objectives below, so we must not
    # iterate it live.
    movers = [
        tgo
        for cp in control_points
        for tgo in cp.connected_objectives
        if isinstance(tgo, ShipGroundObject) and tgo.target_position is not None
    ]

    for ship in movers:
        if ship.target_position is None:
            continue

        # Snap: teleport the ship and its units to the destination (same math as
        # the carrier block in ControlPoint.process_turn).
        delta = ship.target_position - ship.position
        ship.position.x = ship.position.x + delta.x
        ship.position.y = ship.position.y + delta.y
        for unit in ship.units:
            unit.position.x = unit.position.x + delta.x
            unit.position.y = unit.position.y + delta.y
        ship.target_position = None

        # Re-parent: move to the closest CP owned by the ship's current owner.
        owner = ship.control_point.captured
        candidates = [cp for cp in control_points if cp.captured == owner]
        if not candidates:
            continue
        closest = min(
            candidates,
            key=lambda cp: cp.position.distance_to_point(ship.position),
        )
        old_cp = ship.control_point
        if closest is not old_cp:
            old_cp.connected_objectives.remove(ship)
            closest.connected_objectives.append(ship)
            ship.control_point = closest
