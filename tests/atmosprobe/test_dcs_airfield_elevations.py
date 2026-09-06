# tests/atmosprobe/test_dcs_airfield_elevations.py
import json
from pathlib import Path
from typing import Any

from game.atmosprobe.model import load_dump
from scripts.dcs_airfield_elevations import (
    ElevChange,
    apply_elevations,
    build_probe_mission,
    main,
    terrain_file,
)

FIXTURE = Path(__file__).parent / "fixtures" / "sample_dump.json"


def test_terrain_file_naming() -> None:
    assert terrain_file("Caucasus").name == "caucasus.json"
    assert terrain_file("MarianaIslands").name == "marianaislands.json"


def test_build_probe_mission_sets_weather_and_trigger() -> None:
    mission = build_probe_mission("Caucasus")
    assert mission.weather.qnh == 760
    serialized = "\n".join(str(r.actions) for r in mission.triggerrules.triggers)
    assert "[ATMOS]" in serialized


def test_build_probe_mission_unknown_terrain_raises() -> None:
    import pytest

    with pytest.raises(ValueError, match="Valid terrains"):
        build_probe_mission("NotARealTerrain")


def test_apply_updates_existing_capturing_old_and_preserving_fields() -> None:
    dump = load_dump(FIXTURE)  # airbase id "12" land_height_m 42.0
    data: dict[str, Any] = {
        "airports": {
            "12": {
                "name": "Anapa-Vityazevo",
                "elevation_m": 30.0,  # stale SRTM
                "elevation_source": "open_elevation_dem",
                "runways": [{"ref": "03/21"}],
            }
        }
    }
    changes, untouched = apply_elevations(dump, data)
    assert changes == [ElevChange("12", "Anapa-Vityazevo", 30.0, 42.0)]
    assert untouched == []
    assert data["airports"]["12"]["elevation_m"] == 42.0
    assert data["airports"]["12"]["elevation_source"] == "dcs_land_getheight"
    assert data["airports"]["12"]["runways"] == [{"ref": "03/21"}]


def test_apply_adds_stub_for_missing_airport() -> None:
    dump = load_dump(FIXTURE)
    data: dict[str, Any] = {"airports": {}}
    changes, _ = apply_elevations(dump, data)
    assert changes == [ElevChange("12", "Anapa-Vityazevo", None, 42.0)]
    assert data["airports"]["12"]["elevation_m"] == 42.0


def test_apply_reports_untouched_srtm_airports() -> None:
    dump = load_dump(FIXTURE)
    data: dict[str, Any] = {
        "airports": {"12": {"elevation_m": 30.0}, "999": {"elevation_m": 5.0}}
    }
    _, untouched = apply_elevations(dump, data)
    assert untouched == ["999"]


def test_main_apply_writes_terrain_file(tmp_path: Path) -> None:
    target = tmp_path / "caucasus.json"
    target.write_text(
        json.dumps({"airports": {"12": {"name": "Anapa", "elevation_m": 30.0}}}),
        encoding="utf-8",
    )
    rc = main(["apply", "--dump", str(FIXTURE), "--file", str(target)])
    assert rc == 0
    written = json.loads(target.read_text(encoding="utf-8"))
    assert written["airports"]["12"]["elevation_m"] == 42.0
    assert written["airports"]["12"]["elevation_source"] == "dcs_land_getheight"


def test_main_apply_dry_run_does_not_write(tmp_path: Path) -> None:
    target = tmp_path / "caucasus.json"
    original = json.dumps({"airports": {"12": {"name": "Anapa", "elevation_m": 30.0}}})
    target.write_text(original, encoding="utf-8")
    rc = main(["apply", "--dump", str(FIXTURE), "--file", str(target), "--dry-run"])
    assert rc == 0
    assert (
        json.loads(target.read_text(encoding="utf-8"))["airports"]["12"]["elevation_m"]
        == 30.0
    )
