"""F-15EX V3 mod support: the F-15EX, F-15EX (CFTs) and F-15IA, air-to-air only."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from dcs import lua
from dcs.planes import PlaneType, plane_map

from game import persistency
from game.dcs.aircrafttype import AircraftType
from game.factions.faction import Faction
from game.theater.start_generator import ModSettings
from pydcs_extensions.f15ex.f15ex import F_15EX, F_15EX_CFT, F_15IA

TASKS = [
    "Retribution BARCAP",
    "Retribution TARCAP",
    "Retribution Intercept",
    "Retribution Escort",
    "Retribution Fighter sweep",
]
UNITS = {"F15EX": F_15EX, "F15EX_CFT": F_15EX_CFT, "F15IA": F_15IA}
NAMES = {
    "F15EX": "F-15EX Eagle II",
    "F15EX_CFT": "F-15EX Eagle II (CFTs)",
    "F15IA": "F-15IA Eagle II",
}


@pytest.fixture(autouse=True)
def _init_persistency(tmp_path_factory: pytest.TempPathFactory) -> None:
    persistency.setup(str(tmp_path_factory.mktemp("saved_games")), False, 16885)


def _fits(unit: str) -> dict[str, dict[int, str]]:
    path = Path(f"resources/customized_payloads/{unit}.lua")
    payloads = lua.loads(path.read_text(encoding="utf-8"))["unitPayloads"]
    assert payloads["unitType"] == unit
    return {
        p["name"]: {s["num"]: s["CLSID"] for s in p["pylons"].values()}
        for p in payloads["payloads"].values()
    }


def _legal(plane: type[PlaneType], station: int) -> set[str]:
    pylon = getattr(plane, f"Pylon{station}")
    return {
        value[1]["clsid"]
        for key, value in vars(pylon).items()
        if not key.startswith("__")
    }


@pytest.mark.parametrize("unit", sorted(UNITS))
def test_both_jets_are_registered_with_unit_data(unit: str) -> None:
    assert plane_map[unit] is UNITS[unit]
    assert AircraftType.named(NAMES[unit]).dcs_unit_type is UNITS[unit]


@pytest.mark.parametrize("unit", sorted(UNITS))
def test_every_task_has_a_fit_on_legal_stations(unit: str) -> None:
    fits = _fits(unit)
    assert sorted(fits) == sorted(TASKS)
    for name, fit in fits.items():
        for station, clsid in fit.items():
            assert clsid in _legal(UNITS[unit], station), f"{name} station {station}"


@pytest.mark.parametrize("unit", sorted(UNITS))
def test_fits_carry_ten_amraams_two_short_range_and_three_tanks(unit: str) -> None:
    for name, fit in _fits(unit).items():
        stores = list(fit.values())
        amraams = sum(
            2 if "_2x" in c else 1 for c in stores if "AIM-120" in c or "AIM-260" in c
        )
        assert amraams == 10, name
        short = [c for c in stores if "AIM-9X" in c or "PYTHON-5" in c]
        assert len(short) == 2, name
        assert stores.count("{F15E_EXTTANK}") == 3, name


@pytest.mark.parametrize("unit", ["F15EX", "F15EX_CFT"])
def test_the_aim_260a_flies_escort_and_sweep_on_the_f15ex_only(unit: str) -> None:
    for name, fit in _fits(unit).items():
        has_260 = any("AIM-260A" in c for c in fit.values())
        assert has_260 == (name in {"Retribution Escort", "Retribution Fighter sweep"})
    for fit in _fits("F15IA").values():
        assert not any("AIM-260A" in c for c in fit.values())


def _faction(path: str, ticked: bool) -> Faction:
    with Path(path).open(encoding="utf-8-sig") as data:
        faction = Faction.from_dict(json.load(data))
    faction.apply_mod_settings(ModSettings(f15ex_v3=ticked))
    return faction


@pytest.mark.parametrize(
    "path,names",
    [
        (
            "resources/factions/usa_2020.json",
            {"F-15EX Eagle II", "F-15EX Eagle II (CFTs)"},
        ),
        ("resources/factions/israel_2017.json", {"F-15IA Eagle II"}),
        (
            "resources/factions/bluefor_modern.json",
            {"F-15EX Eagle II", "F-15EX Eagle II (CFTs)", "F-15IA Eagle II"},
        ),
    ],
)
def test_factions_list_the_jets_only_when_the_mod_is_ticked(
    path: str, names: set[str]
) -> None:
    jets = set(NAMES.values())
    assert {a.variant_id for a in _faction(path, True).aircraft} & jets == names
    assert not {a.variant_id for a in _faction(path, False).aircraft} & jets
