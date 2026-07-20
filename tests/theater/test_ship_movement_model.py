from dcs.mapping import Point

from game.theater.controlpoint import OffMapSpawn, Player
from game.theater.presetlocation import PresetLocation
from game.theater.theatergroundobject import ShipGroundObject
from game.utils import Heading, nautical_miles


def _ship() -> ShipGroundObject:
    location = PresetLocation(
        name="loc", position=Point(0, 0, None), heading=Heading(0)  # type: ignore[arg-type]
    )
    cp = OffMapSpawn(
        name="cp",
        position=Point(0, 0, None),  # type: ignore[arg-type]
        theater=None,  # type: ignore[arg-type]
        starts_blue=Player.BLUE,
    )
    return ShipGroundObject(name="ship", location=location, control_point=cp)


def test_ship_is_moveable_with_80nm_cap() -> None:
    ship = _ship()
    assert ship.moveable is True
    assert ship.max_move_distance == nautical_miles(80)


def test_ship_target_position_defaults_none() -> None:
    assert _ship().target_position is None


def test_destination_in_range_boundary() -> None:
    ship = _ship()  # ship at (0, 0)
    # 80nm in meters; just inside vs just outside.
    inside = Point(nautical_miles(80).meters - 1.0, 0, None)  # type: ignore[arg-type]
    outside = Point(nautical_miles(80).meters + 1.0, 0, None)  # type: ignore[arg-type]
    assert ship.destination_in_range(inside) is True
    assert ship.destination_in_range(outside) is False
