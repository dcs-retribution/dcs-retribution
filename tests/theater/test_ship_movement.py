from types import SimpleNamespace
from typing import Any

from dcs.mapping import Point

from game.theater.controlpoint import OffMapSpawn, Player
from game.theater.presetlocation import PresetLocation
from game.theater.shipmovement import move_and_reparent_ships
from game.theater.theatergroundobject import ShipGroundObject
from game.utils import Heading


def _cp(name: str, x: float, y: float, blue: bool) -> OffMapSpawn:
    player = Player.BLUE if blue else Player.RED
    cp = OffMapSpawn(
        name=name,
        position=Point(x, y, None),  # type: ignore[arg-type]
        theater=None,  # type: ignore[arg-type]
        starts_blue=player,
    )
    # Inject a minimal fake coalition so cp.captured works without a full Game.
    cp._coalition = SimpleNamespace(player=player)  # type: ignore[assignment]
    return cp


def _ship_on(cp: OffMapSpawn, x: float, y: float) -> ShipGroundObject:
    location = PresetLocation(
        name="loc", position=Point(x, y, None), heading=Heading(0)  # type: ignore[arg-type]
    )
    ship = ShipGroundObject(name="ship", location=location, control_point=cp)
    cp.connected_objectives.append(ship)
    return ship


def test_snap_moves_position_and_units_and_clears_target() -> None:
    home = _cp("home", 0, 0, blue=True)
    ship = _ship_on(home, 0, 0)
    # Fake group with one unit so tgo.units yields a unit with a mutable position.
    unit: Any = SimpleNamespace(position=Point(0, 0, None))  # type: ignore[arg-type]
    ship.groups.append(SimpleNamespace(units=[unit]))  # type: ignore[arg-type]
    ship.target_position = Point(1000, 2000, None)  # type: ignore[arg-type]

    move_and_reparent_ships([home])

    assert ship.position.x == 1000 and ship.position.y == 2000
    assert unit.position.x == 1000 and unit.position.y == 2000
    assert ship.target_position is None


def test_reparent_to_closest_same_faction_cp() -> None:
    home = _cp("home", 0, 0, blue=True)
    near = _cp("near_blue", 1100, 2000, blue=True)
    far = _cp("far_blue", 50000, 50000, blue=True)
    ship = _ship_on(home, 0, 0)
    ship.target_position = Point(1000, 2000, None)  # type: ignore[arg-type]

    move_and_reparent_ships([home, near, far])

    assert ship.control_point is near
    assert ship in near.connected_objectives
    assert ship not in home.connected_objectives
    # Must be registered with exactly one CP — not left behind or double-added.
    assert ship not in far.connected_objectives


def test_reparent_follows_owner_when_origin_captured() -> None:
    # Ship's home CP is now red (its base was captured this turn); the ship
    # re-parents to the closest *red* CP. Captured-port-captures-ships, accepted v1.
    home = _cp("home", 0, 0, blue=False)  # red now
    red_near = _cp("red_near", 1100, 2000, blue=False)
    blue_near = _cp("blue_near", 1000, 2000, blue=True)
    ship = _ship_on(home, 0, 0)
    ship.target_position = Point(1000, 2000, None)  # type: ignore[arg-type]

    move_and_reparent_ships([home, red_near, blue_near])

    assert ship.control_point is red_near
    assert ship in red_near.connected_objectives
    # The old CP's objective list must be cleaned up (no double-parenting).
    assert ship not in home.connected_objectives


def test_ship_without_target_is_untouched() -> None:
    home = _cp("home", 0, 0, blue=True)
    other = _cp("other", 1000, 0, blue=True)
    ship = _ship_on(home, 0, 0)  # no target_position

    move_and_reparent_ships([home, other])

    assert ship.control_point is home
    assert ship.position.x == 0 and ship.position.y == 0
