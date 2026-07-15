from types import SimpleNamespace
from typing import Any

from dcs.mapping import Point

from game.missiongenerator.tgogenerator import GroundObjectGenerator


def _generator(ground_object: Any) -> GroundObjectGenerator:
    return GroundObjectGenerator(
        ground_object, None, None, None, None  # type: ignore[arg-type]
    )


def test_sail_to_destination_adds_waypoint_and_speed() -> None:
    rotated: list[Any] = []
    ground_object = SimpleNamespace(rotate=lambda h: rotated.append(h))
    gen = _generator(ground_object)

    waypoints: list[tuple[Point, float]] = []
    start = SimpleNamespace(position=Point(0, 0, None), speed=0.0)  # type: ignore[arg-type]
    group = SimpleNamespace(
        points=[start],
        add_waypoint=lambda p, kph: waypoints.append((p, kph)),
    )
    destination = Point(10000, 0, None)  # type: ignore[arg-type]

    heading = gen.sail_to_destination(destination, group)  # type: ignore[arg-type]

    assert len(waypoints) == 1
    wp_point, wp_kph = waypoints[0]
    assert wp_point.x == 10000 and wp_point.y == 0
    assert wp_kph > 0
    assert start.speed > 0
    assert rotated == [heading]
