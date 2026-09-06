"""DCS airfield elevation tooling for the kneeboard QFE.

Two subcommands:

    generate --terrain <Name>             build a probe .miz to fly in DCS
    apply --log <dcs.log> | --dump <file> read the probe output and update
                                          resources/airport_imagery/<terrain>.json

The probe records each airbase's DCS ``land.getHeight`` (the QFE ground truth);
``apply`` writes those into the airport-imagery JSON, replacing the SRTM-derived
elevations the kneeboard QFE was using. See scripts/README.md for the workflow.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from game.atmosprobe.model import AtmoDump, load_dump, load_dump_from_log

_IMAGERY_DIR = Path(__file__).resolve().parent.parent / "resources" / "airport_imagery"
_SOURCE = "dcs_land_getheight"
_FT_PER_M = 3.280839895


def terrain_file(terrain: str) -> Path:
    """Path of the imagery JSON for a terrain (same naming as the generator)."""
    return _IMAGERY_DIR / f"{terrain.lower().replace(' ', '')}.json"


# --------------------------------------------------------------------------- #
# generate
# --------------------------------------------------------------------------- #

_PLUGIN = _IMAGERY_DIR.parent / "plugins" / "base"
_JSON_LUA = _PLUGIN / "json.lua"
_PROBE_LUA = _PLUGIN / "dcs_atmos_probe.lua"

# A fixed weather block for the probe mission. The values are irrelevant to the
# result — ``land.getHeight`` is weather-independent — but a mission needs one.
_QNH_MMHG = 760
_TEMP_C = 15


def _terrain_classes() -> dict[str, Any]:
    import dcs.terrain as t

    return {
        "Afghanistan": t.Afghanistan,
        "Caucasus": t.Caucasus,
        "Falklands": t.Falklands,
        "GermanyColdWar": t.GermanyColdWar,
        "Iraq": t.Iraq,
        "Kola": t.Kola,
        "MarianaIslands": t.MarianaIslands,
        "Nevada": t.Nevada,
        "Normandy": t.Normandy,
        "PersianGulf": t.PersianGulf,
        "Sinai": t.Sinai,
        "Syria": t.Syria,
        "TheChannel": t.TheChannel,
    }


def _probe_script() -> str:
    """json.lua defines a global ``json``; prepend it, then the probe."""
    json_src = _JSON_LUA.read_text(encoding="utf-8")
    probe_src = _PROBE_LUA.read_text(encoding="utf-8")
    return f"{json_src}\n\n{probe_src}\n"


def build_probe_mission(terrain_name: str) -> Any:
    """Build a minimal DCS mission whose mission-start trigger runs the probe."""
    import dcs
    from dcs.action import DoScript
    from dcs.translation import String
    from dcs.triggers import TriggerStart
    from dcs.weather import Wind

    classes = _terrain_classes()
    try:
        terrain_cls = classes[terrain_name]
    except KeyError:
        valid = ", ".join(sorted(classes))
        raise ValueError(f"Unknown terrain {terrain_name!r}. Valid terrains: {valid}")
    mission = dcs.Mission(terrain_cls())

    mission.weather.qnh = _QNH_MMHG
    mission.weather.season_temperature = _TEMP_C
    mission.weather.wind_at_ground = Wind(0, 0)
    mission.weather.wind_at_2000 = Wind(0, 0)
    mission.weather.wind_at_8000 = Wind(0, 0)

    # Inline json.lua + the probe as one DoScript on a mission-start trigger.
    # DoScript takes a dcs.translation.String (same pattern as luagenerator.py).
    trigger = TriggerStart(comment="atmos probe")
    trigger.add_action(DoScript(String(_probe_script())))
    mission.triggerrules.triggers.append(trigger)
    return mission


def _cmd_generate(args: argparse.Namespace) -> int:
    mission = build_probe_mission(args.terrain)
    out: Path = args.out or Path(f"atmos_probe_{args.terrain.lower()}.miz")
    mission.save(str(out))
    print(f"wrote {out} — fly it in DCS, then run: apply --log <dcs.log>")
    return 0


# --------------------------------------------------------------------------- #
# apply
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class ElevChange:
    airbase_id: str
    name: str
    old_m: float | None  # prior elevation_m (SRTM/OSM), or None if no entry
    new_m: float  # DCS land.getHeight


def apply_elevations(
    dump: AtmoDump, data: dict[str, Any]
) -> tuple[list[ElevChange], list[str]]:
    """Update ``data['airports'][id].elevation_m`` from the dump in place.

    Existing entries keep all other fields (runways, imagery offset); only
    ``elevation_m`` and ``elevation_source`` change. Dump airbases with no entry
    get an elevation-only stub so ``field_elevation_for_airport`` still resolves.
    Returns ``(changes, untouched_ids)`` where untouched_ids are JSON airports the
    dump did not cover (left on their old SRTM value).
    """
    airports: dict[str, Any] = data.setdefault("airports", {})
    dump_ids = {ab.id for ab in dump.airbases}
    changes: list[ElevChange] = []
    for ab in dump.airbases:
        new_m = round(ab.land_height_m, 1)
        entry = airports.get(ab.id)
        if entry is None:
            airports[ab.id] = {
                "name": ab.name,
                "elevation_m": new_m,
                "elevation_source": _SOURCE,
            }
            changes.append(ElevChange(ab.id, ab.name, None, new_m))
        else:
            raw_old = entry.get("elevation_m")
            old_m = float(raw_old) if raw_old is not None else None
            entry["elevation_m"] = new_m
            entry["elevation_source"] = _SOURCE
            changes.append(ElevChange(ab.id, ab.name, old_m, new_m))
    untouched = sorted(aid for aid in airports if aid not in dump_ids)
    return changes, untouched


def _print_delta_table(changes: list[ElevChange]) -> None:
    def sort_key(c: ElevChange) -> float:
        return abs(c.new_m - c.old_m) if c.old_m is not None else float("inf")

    print(f"{'airfield':24} {'old m':>8} {'DCS m':>8} {'delta':>8} {'~ft':>6}  source")
    for c in sorted(changes, key=sort_key, reverse=True):
        if c.old_m is None:
            print(
                f"{c.name[:24]:24} {'(new)':>8} {c.new_m:8.1f} {'--':>8} {'--':>6}  added"
            )
        else:
            d = c.new_m - c.old_m
            print(
                f"{c.name[:24]:24} {c.old_m:8.1f} {c.new_m:8.1f} "
                f"{d:+8.1f} {abs(d) * _FT_PER_M:6.0f}  updated"
            )


def _cmd_apply(args: argparse.Namespace) -> int:
    dump = (
        load_dump(args.dump) if args.dump is not None else load_dump_from_log(args.log)
    )
    terrain = args.terrain or dump.terrain
    path = args.file or terrain_file(terrain)
    if not path.exists():
        print(f"error: no imagery JSON at {path}", file=sys.stderr)
        return 1

    with path.open("r", encoding="utf-8") as fh:
        data: dict[str, Any] = json.load(fh)
    changes, untouched = apply_elevations(dump, data)

    updated = sum(1 for c in changes if c.old_m is not None)
    added = sum(1 for c in changes if c.old_m is None)
    _print_delta_table(changes)
    print(
        f"\n{terrain}: {updated} updated, {added} added, "
        f"{len(untouched)} left on SRTM ({', '.join(untouched) or 'none'})"
    )
    if args.dry_run:
        print("(dry run — not written)")
        return 0

    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)
        fh.write("\n")
    tmp.replace(path)
    print(f"wrote {path}")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate the DCS elevation probe mission and apply its data."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="build the probe .miz for a terrain")
    gen.add_argument(
        "--terrain", required=True, help="pydcs terrain name, e.g. Caucasus, Syria"
    )
    gen.add_argument("--out", type=Path, default=None, help="output .miz path")
    gen.set_defaults(func=_cmd_generate)

    app = sub.add_parser("apply", help="apply the probe output to airport_imagery")
    src = app.add_mutually_exclusive_group(required=True)
    src.add_argument("--dump", type=Path, help="atmos_probe.json file")
    src.add_argument("--log", type=Path, help="dcs.log to reassemble the dump from")
    app.add_argument(
        "--terrain", default=None, help="override the terrain (default: from the dump)"
    )
    app.add_argument(
        "--file", type=Path, default=None, help="override the target JSON path"
    )
    app.add_argument(
        "--dry-run", action="store_true", help="show the change table without writing"
    )
    app.set_defaults(func=_cmd_apply)

    args = parser.parse_args(argv)
    result: int = args.func(args)
    return result


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
