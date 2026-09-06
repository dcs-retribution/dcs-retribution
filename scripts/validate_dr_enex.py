"""Validation for dr-enex: squadron mission_types auto-assignable limit.

Run from the repo root:
    PATH=".venv/bin:$PATH" PYTHONPATH=. python scripts/validate_dr_enex.py

Exercises section B (load-path behavior) of
docs/superpowers/validation/2026-06-29-dr-enex-squadron-mission-types-validation.md.
No DCS install required.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any, Optional

import yaml

import game.persistency as persistency

# Point persistency at a temp dir so aircraft loading works without a DCS install
# (mirrors tests/conftest.py).
persistency._dcs_saved_game_folder = tempfile.mkdtemp(prefix="dr_enex_validate_")

from game.ato.flighttype import FlightType  # noqa: E402
from game.dcs.aircrafttype import (  # noqa: E402
    AircraftType,
    derived_task_types,
)
from game.squadrons.squadron import Squadron  # noqa: E402
from game.squadrons.squadrondef import SquadronDef  # noqa: E402

_results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    _results.append((name, bool(ok), detail))


def _write(tmp: Path, aircraft: AircraftType, mission_types: Any = ...) -> Path:
    data: dict[str, Any] = {
        "name": "v",
        "country": "USA",
        "role": "t",
        "aircraft": aircraft.variant_id,
    }
    if mission_types is not ...:
        data["mission_types"] = mission_types
    path = tmp / "s.yaml"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    return path


def main() -> int:
    tmp = Path(tempfile.mkdtemp())
    cas = AircraftType.priority_list_for_task(FlightType.CAS)[0]
    caps = set(cas.iter_task_capabilities())

    # B1: absent key -> all caps
    sd = SquadronDef.from_yaml(_write(tmp, cas))
    check("absent -> all caps", sd.auto_assignable_mission_types == caps)

    # B2a: real shipped YAML loads, restricted to caps, derives ARMED_RECON.
    # (Its curated list may or may not be narrower than this airframe's caps, so we
    # don't assert strict restriction here -- that's covered by B2b on a constructed
    # narrower case.)
    real = Path("resources/squadrons/A-10C Warthog I/81st FS.yaml")
    sd = SquadronDef.from_yaml(real)
    rcaps = set(sd.aircraft.iter_task_capabilities())
    aset = sd.auto_assignable_mission_types
    check("81st FS subset of caps", aset <= rcaps)
    check("81st FS keeps listed CAS", FlightType.CAS in aset)
    check("81st FS derives ARMED_RECON", FlightType.ARMED_RECON in aset)

    # B2b: constructed restriction -- listing only CAS yields {CAS, ARMED_RECON}, a
    # strict subset of a multi-capability airframe's caps.
    check("test airframe is multi-capability", len(caps) > 2, f"{len(caps)} caps")
    sd = SquadronDef.from_yaml(_write(tmp, cas, [FlightType.CAS.value]))
    restricted = sd.auto_assignable_mission_types
    check(
        "list [CAS] -> {CAS, ARMED_RECON} strictly restricted",
        restricted == {FlightType.CAS, FlightType.ARMED_RECON} and restricted < caps,
        f"{sorted(t.value for t in restricted)}",
    )

    # B3: empty list -> empty set
    sd = SquadronDef.from_yaml(_write(tmp, cas, []))
    check("empty -> empty", sd.auto_assignable_mission_types == set())

    # B4: unknown value -> KeyError
    try:
        SquadronDef.from_yaml(_write(tmp, cas, ["BogusType"]))
        check("unknown -> KeyError", False, "no error raised")
    except KeyError:
        check("unknown -> KeyError", True)

    # B5: scalar (non-list) -> KeyError
    try:
        SquadronDef.from_yaml(_write(tmp, cas, FlightType.CAS.value))
        check("scalar -> KeyError", False, "no error raised")
    except KeyError:
        check("scalar -> KeyError", True)

    # B6: subtract-only -- a listed non-capable task cannot grant a derived sibling
    found: Optional[str] = None
    for aircraft in AircraftType.iter_all():
        cap_set = set(aircraft.iter_task_capabilities())
        incapable = next(
            (
                f
                for f in FlightType
                if f not in cap_set
                and derived_task_types({f}, aircraft.carrier_capable) & cap_set
            ),
            None,
        )
        if incapable is None:
            continue
        sd = SquadronDef.from_yaml(_write(tmp, aircraft, [incapable.value]))
        check(
            "subtract-only (no back-door sibling)",
            sd.auto_assignable_mission_types == set(),
            aircraft.variant_id,
        )
        found = aircraft.variant_id
        break
    if found is None:
        check("subtract-only (no back-door sibling)", True, "no airframe exposes it")

    # B7: read-time gate (set membership AND airframe capability)
    sqn: Squadron = object.__new__(Squadron)
    sqn.aircraft = cas
    incap = next(f for f in FlightType if f not in caps)
    sqn.auto_assignable_mission_types = {FlightType.CAS, incap}
    check("read-time: in-set + capable -> True", sqn.can_auto_assign(FlightType.CAS))
    check("read-time: in-set + incapable -> False", not sqn.can_auto_assign(incap))

    passed = sum(1 for _, ok, _ in _results if ok)
    for name, ok, detail in _results:
        suffix = f" - {detail}" if detail else ""
        print(f"[{'PASS' if ok else 'FAIL'}] {name}{suffix}")
    print(f"\n{passed}/{len(_results)} checks passed")
    return 0 if passed == len(_results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
