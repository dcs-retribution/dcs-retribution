from __future__ import annotations

from itertools import combinations

import pytest
from dcs import Mission, Point
from dcs.planes import F_16C_50
from dcs.terrain import Caucasus

from game.missiongenerator.aircraft.formation import (
    is_airborne_start,
    space_airborne_group,
)


@pytest.mark.parametrize(
    "route_points,expected_heading",
    [
        ([(0, 0), (0, 1000)], 90.0),
        ([(0, 0), (1000, 0)], 0.0),
        ([(0, 0), (1000, 1000)], 45.0),
        ([(0, 0), (0, 0), (-1000, 1000)], 135.0),
        ([(0, 0), (0, 0)], 0.0),
    ],
)
@pytest.mark.parametrize("group_size", [1, 2, 4])
def test_airborne_formation_spacing_serializes_with_shared_route_heading(
    route_points: list[tuple[float, float]], expected_heading: float, group_size: int
) -> None:
    mission = Mission(Caucasus())
    group = mission.flight_group(
        mission.country("USA"),
        "Formation test",
        F_16C_50,
        airport=None,
        position=Point(0, 0, mission.terrain),
        altitude=2000,
        speed=500,
        group_size=group_size,
    )
    for x, y in route_points:
        group.add_waypoint(Point(x, y, mission.terrain), altitude=2000)

    initial_route = [point.position for point in group.points]
    leader_position = group.units[0].position
    space_airborne_group(group)

    assert [point.position for point in group.points] == initial_route
    assert group.units[0].position == leader_position
    if group_size > 1:
        assert [unit.heading for unit in group.units] == [expected_heading] * group_size
    serialized = group.dict()
    headings = [
        serialized["units"][index + 1]["heading"] for index in range(group_size)
    ]
    serialized_heading = expected_heading if group_size > 1 else 0.0
    assert headings == pytest.approx(
        [serialized_heading * 3.141592653589793 / 180] * group_size
    )

    positions = [unit.position for unit in group.units]
    for first, second in combinations(positions, 2):
        assert first.distance_to_point(second) >= 50.0 - 1e-6


@pytest.mark.parametrize(
    "start_type,expected_airborne",
    [
        ("TakeOff", False),
        ("TakeOffParking", False),
        ("Turning Point", True),
    ],
)
def test_start_classification_preserves_ground_start_exclusions(
    start_type: str, expected_airborne: bool
) -> None:
    mission = Mission(Caucasus())
    group = mission.flight_group(
        mission.country("USA"),
        "Start classification",
        F_16C_50,
        airport=None,
        position=Point(0, 0, mission.terrain),
        altitude=2000,
        speed=500,
        group_size=2,
    )
    group.points[0].type = start_type

    assert is_airborne_start(group) is expected_airborne


def test_singleton_dormant_aircraft_remains_unchanged_by_spacing_operation() -> None:
    mission = Mission(Caucasus())
    group = mission.flight_group(
        mission.country("USA"),
        "Dormant singleton",
        F_16C_50,
        airport=None,
        position=Point(123, 456, mission.terrain),
        altitude=2000,
        speed=500,
        group_size=1,
    )
    group.points[0].type = "Turning Point"
    position = group.units[0].position
    heading = group.units[0].heading

    if is_airborne_start(group):
        space_airborne_group(group)

    assert group.units[0].position == position
    assert group.units[0].heading == heading
