"""Typed model + JSON loader for the DCS atmosphere/elevation probe dump (dr-g1tk).

The schema is the contract between the Lua exporter (writes it in-sim) and the
Python ingest (reads it here). Bump SCHEMA_VERSION on any breaking change.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
LADDER_TOP_M = 12192.0  # 40,000 ft
LADDER_STEP_M = 152.4  # 500 ft
# 0 m .. 12192 m inclusive; derived from TOP/STEP so it can't silently drift.
LADDER_RUNG_COUNT = int(LADDER_TOP_M / LADDER_STEP_M) + 1


@dataclass(frozen=True)
class WindSample:
    dir_from_deg: float
    speed_mps: float


@dataclass(frozen=True)
class AtmoSample:
    alt_msl_m: float
    wind: WindSample
    wind_turb: WindSample
    temp_c: float
    pressure_hpa: float


@dataclass(frozen=True)
class Airbase:
    id: str
    name: str
    x: float
    z: float
    land_height_m: float
    surface: AtmoSample


@dataclass(frozen=True)
class Column:
    label: str
    x: float
    z: float
    rungs: list[AtmoSample]


@dataclass(frozen=True)
class ConfiguredWind:
    at_0m: WindSample
    at_2000m: WindSample
    at_8000m: WindSample


@dataclass(frozen=True)
class ConfiguredWeather:
    qnh_mmhg: float
    qnh_inhg: float
    temperature_c: float
    wind: ConfiguredWind


@dataclass(frozen=True)
class AtmoDump:
    schema_version: int
    terrain: str
    configured: ConfiguredWeather
    airbases: list[Airbase]
    columns: list[Column]


def _wind(d: dict[str, Any]) -> WindSample:
    return WindSample(
        dir_from_deg=float(d["dir_from_deg"]), speed_mps=float(d["speed_mps"])
    )


def _sample(d: dict[str, Any]) -> AtmoSample:
    return AtmoSample(
        alt_msl_m=float(d["alt_msl_m"]),
        wind=_wind(d["wind"]),
        wind_turb=_wind(d["wind_turb"]),
        temp_c=float(d["temp_c"]),
        pressure_hpa=float(d["pressure_hpa"]),
    )


def load_dump(path: Path) -> AtmoDump:
    """Parse a JSON dump file written by the probe (io-enabled DCS env)."""
    with path.open("r", encoding="utf-8") as fh:
        data: dict[str, Any] = json.load(fh)
    return _parse_dump(data, str(path))


# `[ATMOS] JSON <i>/<n> <chunk>` lines streamed to dcs.log when io was sanitized.
_LOG_CHUNK_RE = re.compile(r"\[ATMOS\] JSON (\d+)/(\d+) (.*)$")


def load_dump_from_log(path: Path) -> AtmoDump:
    """Reassemble a dump from the chunked JSON the probe streams to dcs.log.

    Used when DCS's MissionScripting.lua sanitizes ``io`` and the probe cannot
    write a file. Concatenates the ordered ``[ATMOS] JSON i/n`` chunks.
    """
    chunks: dict[int, str] = {}
    expected: int | None = None
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            m = _LOG_CHUNK_RE.search(line)
            if m is None:
                continue
            expected = int(m.group(2))
            chunks[int(m.group(1))] = m.group(3).rstrip("\r\n")
    if not chunks or expected is None:
        raise ValueError(
            f"{path}: no '[ATMOS] JSON i/n' chunks found — did the probe run and "
            f"stream to this log? (Look for a [ATMOS] JSON-BEGIN line.)"
        )
    missing = [i for i in range(1, expected + 1) if i not in chunks]
    if missing:
        raise ValueError(
            f"{path}: incomplete probe log, missing chunks {missing} of {expected}."
        )
    payload = "".join(chunks[i] for i in range(1, expected + 1))
    return _parse_dump(json.loads(payload), str(path))


def _parse_dump(data: dict[str, Any], source: str) -> AtmoDump:
    raw_version = data.get("schema_version")
    if raw_version is None:
        raise ValueError(
            f"{source}: no schema_version field — not a probe dump or a truncated write."
        )
    try:
        version = int(raw_version)
    except (TypeError, ValueError):
        raise ValueError(f"{source}: non-integer schema_version {raw_version!r}.")
    if version != SCHEMA_VERSION:
        # The schema is the Lua<->Python contract; a mismatch means silently
        # wrong fields, so fail loudly with the actual versions rather than
        # parsing on and surfacing a confusing KeyError deep in _sample().
        raise ValueError(
            f"{source}: unsupported probe schema_version {version} "
            f"(this build reads {SCHEMA_VERSION}); regenerate the dump."
        )
    cw: dict[str, Any] = data["configured_weather"]
    wind: dict[str, dict[str, Any]] = cw["wind"]
    configured = ConfiguredWeather(
        qnh_mmhg=float(cw["qnh_mmhg"]),
        qnh_inhg=float(cw["qnh_inhg"]),
        temperature_c=float(cw["temperature_c"]),
        wind=ConfiguredWind(
            at_0m=_wind(wind["at_0m"]),
            at_2000m=_wind(wind["at_2000m"]),
            at_8000m=_wind(wind["at_8000m"]),
        ),
    )
    airbases = [
        Airbase(
            id=str(a["id"]),
            name=str(a["name"]),
            x=float(a["x"]),
            z=float(a["z"]),
            land_height_m=float(a["land_height_m"]),
            surface=_sample(a["surface"]),
        )
        for a in data["airbases"]
    ]
    columns = [
        Column(
            label=str(c["label"]),
            x=float(c["x"]),
            z=float(c["z"]),
            rungs=[_sample(r) for r in c["rungs"]],
        )
        for c in data["columns"]
    ]
    return AtmoDump(
        schema_version=version,
        terrain=str(data["terrain"]),
        configured=configured,
        airbases=airbases,
        columns=columns,
    )
