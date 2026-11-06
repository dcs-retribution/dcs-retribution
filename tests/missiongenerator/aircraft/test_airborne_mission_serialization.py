from __future__ import annotations

from itertools import combinations
from pathlib import Path
from zipfile import ZipFile

import pytest
from dcs import Mission, Point
from dcs.helicopters import UH_1H
from dcs.planes import F_16C_50, MQ_9_Reaper
from dcs.terrain import Caucasus

from game.missiongenerator.aircraft.formation import (
    is_airborne_start,
    space_airborne_group,
)


@pytest.mark.parametrize("country_name", ["USA", "Russia"])
@pytest.mark.parametrize("delayed", [False, True])
def test_serialized_airborne_groups_preserve_non_geometry_fields(
    tmp_path: Path, country_name: str, delayed: bool
) -> None:
    mission = Mission(Caucasus())
    country = mission.country(country_name)
    for index, aircraft in enumerate((F_16C_50, UH_1H, MQ_9_Reaper)):
        group = mission.flight_group(
            country,
            f"Airborne {index}",
            aircraft,
            airport=None,
            position=Point(12345, 67890, mission.terrain),
            altitude=1234,
            speed=200,
            group_size=4 if index < 2 else 1,
        )
        group.add_waypoint(Point(13345, 68890, mission.terrain), altitude=1500)
        group.start_time = 300 if delayed else 0
        before = group.dict()
        leader = group.units[0].position
        assert is_airborne_start(group)
        space_airborne_group(group)
        after = group.dict()
        assert group.units[0].position == leader
        for key in before:
            if key not in ("units", "manualHeading"):
                assert after[key] == before[key]
        for unit_index, unit_before in before["units"].items():
            unit_after = after["units"][unit_index]
            for key in unit_before:
                if key not in ("x", "y", "heading"):
                    assert unit_after[key] == unit_before[key]
        serialized_units = list(after["units"].values())
        for first, second in combinations(serialized_units, 2):
            distance = (
                (first["x"] - second["x"]) ** 2 + (first["y"] - second["y"]) ** 2
            ) ** 0.5
            assert distance >= 50 - 1e-6
            assert first["heading"] == second["heading"]
    miz_path = tmp_path / "airborne.miz"
    mission.save(str(miz_path))
    with ZipFile(miz_path) as archive:
        serialized_mission = archive.read("mission").decode("utf-8")
    assert "Airborne 0" in serialized_mission
    assert "Airborne 1" in serialized_mission
    assert "Airborne 2" in serialized_mission
