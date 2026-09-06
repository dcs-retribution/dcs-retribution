from pathlib import Path
from typing import Optional

import pytest
import yaml

from game.ato.flighttype import FlightType
from game.dcs.aircrafttype import AircraftType, derived_task_types
from game.squadrons.squadrondef import SquadronDef


def _write_squadron_yaml(
    tmp_path: Path,
    aircraft: AircraftType,
    mission_types: Optional[list[str]] = None,
) -> Path:
    data: dict[str, object] = {
        "name": "Test Sqn",
        "country": "USA",
        "role": "test",
        "aircraft": aircraft.variant_id,
    }
    if mission_types is not None:
        data["mission_types"] = mission_types
    path = tmp_path / "sqn.yaml"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    return path


def _cas_aircraft() -> AircraftType:
    return AircraftType.priority_list_for_task(FlightType.CAS)[0]


def test_absent_mission_types_is_all_caps(tmp_path: Path) -> None:
    aircraft = _cas_aircraft()
    sqn = SquadronDef.from_yaml(_write_squadron_yaml(tmp_path, aircraft))
    assert sqn.auto_assignable_mission_types == set(aircraft.iter_task_capabilities())


def test_mission_types_limits_to_listed_plus_derived(tmp_path: Path) -> None:
    aircraft = _cas_aircraft()
    caps = set(aircraft.iter_task_capabilities())
    sqn = SquadronDef.from_yaml(
        _write_squadron_yaml(tmp_path, aircraft, [FlightType.CAS.value])
    )
    # Concrete (not helper-recomputed) expectation: CAS plus its derived sibling
    # ARMED_RECON, and nothing else. A CAS-capable airframe always has ARMED_RECON in
    # caps (the airframe derives it), so listing CAS yields exactly these two.
    expected = {FlightType.CAS, FlightType.ARMED_RECON}
    assert sqn.auto_assignable_mission_types == expected
    # Genuinely limited: capabilities outside the list are dropped.
    excluded = caps - expected
    assert excluded, "test needs a CAS aircraft with capabilities beyond CAS"
    for task in excluded:
        assert task not in sqn.auto_assignable_mission_types


def test_types_outside_airframe_caps_are_dropped(tmp_path: Path) -> None:
    aircraft = _cas_aircraft()
    caps = set(aircraft.iter_task_capabilities())
    outside = next(t for t in FlightType if t not in caps)
    sqn = SquadronDef.from_yaml(
        _write_squadron_yaml(tmp_path, aircraft, [FlightType.CAS.value, outside.value])
    )
    assert outside not in sqn.auto_assignable_mission_types
    assert FlightType.CAS in sqn.auto_assignable_mission_types


def test_unknown_mission_type_raises_keyerror(tmp_path: Path) -> None:
    aircraft = _cas_aircraft()
    path = _write_squadron_yaml(tmp_path, aircraft, ["NotARealMissionType"])
    with pytest.raises(KeyError):
        SquadronDef.from_yaml(path)


def test_scalar_mission_types_raises_keyerror(tmp_path: Path) -> None:
    # A bare scalar (not a list) must fail clearly, not iterate char-by-char.
    aircraft = _cas_aircraft()
    data: dict[str, object] = {
        "name": "Test Sqn",
        "country": "USA",
        "role": "test",
        "aircraft": aircraft.variant_id,
        "mission_types": FlightType.CAS.value,  # scalar string, not a list
    }
    path = tmp_path / "sqn.yaml"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    with pytest.raises(KeyError):
        SquadronDef.from_yaml(path)


def test_empty_mission_types_yields_empty_set(tmp_path: Path) -> None:
    # An explicit empty list means "auto-plan nothing" (distinct from an absent key,
    # which means all caps). Locks the documented behavior.
    aircraft = _cas_aircraft()
    sqn = SquadronDef.from_yaml(_write_squadron_yaml(tmp_path, aircraft, []))
    assert sqn.auto_assignable_mission_types == set()


def test_listed_incapable_type_does_not_grant_derived_sibling(tmp_path: Path) -> None:
    # Regression: derivation must run AFTER clamping to airframe caps, so listing a task
    # the airframe cannot fly cannot back-door a derived sibling that IS in caps (e.g.
    # listing SEAD on a SEAD_ESCORT-only airframe must not grant SEAD_SWEEP).
    tested = 0
    for aircraft in AircraftType.iter_all():
        caps = set(aircraft.iter_task_capabilities())
        incapable = next(
            (
                f
                for f in FlightType
                if f not in caps
                and derived_task_types({f}, aircraft.carrier_capable) & caps
            ),
            None,
        )
        if incapable is None:
            continue
        sqn = SquadronDef.from_yaml(
            _write_squadron_yaml(tmp_path, aircraft, [incapable.value])
        )
        assert sqn.auto_assignable_mission_types == set(), aircraft.variant_id
        tested += 1
    if tested == 0:
        pytest.skip("no aircraft exposes the derive-from-incapable scenario")
