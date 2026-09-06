from pathlib import Path

import yaml

from game.ato.flighttype import FlightType
from game.dcs.aircrafttype import AircraftType
from game.squadrons.squadron import Squadron
from game.squadrons.squadrondef import SquadronDef


def _cas_aircraft() -> AircraftType:
    return AircraftType.priority_list_for_task(FlightType.CAS)[0]


def _squadron(aircraft: AircraftType, auto_set: set[FlightType]) -> Squadron:
    """Construct a minimal Squadron stub — only the attrs can_auto_assign reads."""
    sqn: Squadron = object.__new__(Squadron)
    sqn.aircraft = aircraft
    sqn.auto_assignable_mission_types = set(auto_set)
    return sqn


def test_in_set_and_capable_is_true() -> None:
    aircraft = _cas_aircraft()
    sqn = _squadron(aircraft, {FlightType.CAS})
    assert sqn.can_auto_assign(FlightType.CAS) is True


def test_in_set_but_not_capable_is_false() -> None:
    aircraft = _cas_aircraft()
    caps = set(aircraft.iter_task_capabilities())
    incapable = next((t for t in FlightType if t not in caps), None)
    assert incapable is not None, "no FlightType outside this airframe's caps"
    sqn = _squadron(aircraft, {FlightType.CAS, incapable})
    assert sqn.can_auto_assign(incapable) is False


def test_capable_but_not_in_set_is_false() -> None:
    aircraft = _cas_aircraft()
    caps = set(aircraft.iter_task_capabilities())
    other_cap = next((t for t in caps if t != FlightType.CAS), None)
    assert other_cap is not None, "test needs a CAS aircraft with caps beyond CAS"
    sqn = _squadron(aircraft, {FlightType.CAS})
    assert sqn.can_auto_assign(other_cap) is False


def test_squadrondef_can_auto_assign_respects_set(tmp_path: Path) -> None:
    aircraft = _cas_aircraft()
    data: dict[str, object] = {
        "name": "t",
        "country": "USA",
        "role": "t",
        "aircraft": aircraft.variant_id,
        "mission_types": [FlightType.CAS.value],
    }
    path = tmp_path / "sqn.yaml"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    sqn_def = SquadronDef.from_yaml(path)
    others = [
        t
        for t in aircraft.iter_task_capabilities()
        if t not in sqn_def.auto_assignable_mission_types
    ]
    assert others, "test needs a CAS aircraft with caps beyond its mission_types"
    other_cap = others[0]
    assert sqn_def.can_auto_assign(FlightType.CAS) is True
    assert sqn_def.can_auto_assign(other_cap) is False
