from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import Optional, TYPE_CHECKING

from game.radio.radios import RadioFrequency
from game.radio.tacan import TacanBand, TacanChannel

if TYPE_CHECKING:
    from game.theater import ConflictTheater

BEACONS_RESOURCE_PATH = Path("resources/dcs/beacons")


class BeaconType(IntEnum):
    BEACON_TYPE_NULL = 0
    BEACON_TYPE_VOR = 1
    BEACON_TYPE_DME = 2
    BEACON_TYPE_VOR_DME = 3
    BEACON_TYPE_TACAN = 4
    BEACON_TYPE_VORTAC = 5
    BEACON_TYPE_RSBN = 128
    BEACON_TYPE_BROADCAST_STATION = 1024

    BEACON_TYPE_HOMER = 8
    BEACON_TYPE_AIRPORT_HOMER = 4104
    BEACON_TYPE_AIRPORT_HOMER_WITH_MARKER = 4136
    BEACON_TYPE_ILS_FAR_HOMER = 16408
    BEACON_TYPE_ILS_NEAR_HOMER = 16424

    BEACON_TYPE_ILS_LOCALIZER = 16640
    BEACON_TYPE_ILS_GLIDESLOPE = 16896

    BEACON_TYPE_PRMG_LOCALIZER = 33024
    BEACON_TYPE_PRMG_GLIDESLOPE = 33280

    BEACON_TYPE_ICLS_LOCALIZER = 131328
    BEACON_TYPE_ICLS_GLIDESLOPE = 131584

    BEACON_TYPE_NAUTICAL_HOMER = 65536

    BEACON_TYPE_TACAN_RANGE = 262144


@dataclass(frozen=True)
class Beacon:
    name: str
    callsign: str
    beacon_type: BeaconType
    hertz: int
    channel: Optional[int]

    @property
    def frequency(self) -> RadioFrequency:
        return RadioFrequency(self.hertz)

    @property
    def is_tacan(self) -> bool:
        return self.beacon_type in (
            BeaconType.BEACON_TYPE_VORTAC,
            BeaconType.BEACON_TYPE_TACAN,
        )

    @property
    def tacan_channel(self) -> TacanChannel:
        assert self.is_tacan
        assert self.channel is not None
        return TacanChannel(self.channel, TacanBand.X)


class Beacons:
    _by_terrain: dict[str, dict[str, Beacon]] = {}

    @classmethod
    def _load_for_theater_if_needed(cls, theater: ConflictTheater) -> None:
        if theater.terrain.name in cls._by_terrain:
            return

        beacons_filename_mapper = {
            "sinaimap": "sinai",
        }
        filename = theater.terrain.name.lower()
        filename = beacons_filename_mapper.get(filename, filename)
        beacons_path = BEACONS_RESOURCE_PATH / f"{filename}.json"
        if not beacons_path.exists():
            raise RuntimeError(f"Beacon file {beacons_path.resolve()} is missing")

        beacons = {}
        for bid, beacon in json.loads(beacons_path.read_text()).items():
            beacons[bid] = Beacon(
                name=beacon["name"],
                callsign=beacon["callsign"],
                beacon_type=BeaconType(beacon["beacon_type"]),
                hertz=beacon["hertz"],
                channel=beacon["channel"],
            )
        cls._by_terrain[theater.terrain.name] = beacons

    @classmethod
    def _dict_for_theater(cls, theater: ConflictTheater) -> dict[str, Beacon]:
        cls._load_for_theater_if_needed(theater)
        return cls._by_terrain[theater.terrain.name]

    @classmethod
    def iter_theater(cls, theater: ConflictTheater) -> Iterator[Beacon]:
        yield from cls._dict_for_theater(theater).values()

    @classmethod
    def with_id(cls, beacon_id: str, theater: ConflictTheater) -> Beacon:
        return cls._dict_for_theater(theater)[beacon_id]
