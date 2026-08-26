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


# Standard ICAO VOR/TACAN channelling plan: every 50 kHz VHF nav frequency in the
# civil VOR band (108.00-117.95 MHz) is paired 1:1 with a TACAN channel/band.
# https://www.flightsim-corner.com/wp-content/uploads/VOR-Frequencies-to-TACAN-Channel-list.pdf
_VOR_TACAN_STEP_HZ = 50_000
_VOR_TACAN_LOW_BAND = (108_000_000, 112_250_000, 17)  # 108.00-112.25 MHz -> 17-59
_VOR_TACAN_HIGH_BAND = (112_300_000, 117_950_000, 70)  # 112.30-117.95 MHz -> 70-126


def _tacan_channel_from_vor_frequency(hertz: Optional[int]) -> Optional[TacanChannel]:
    """Derives the TACAN channel/band paired with a VOR/DME frequency, if any.

    DCS beacon data frequently omits the TACAN channel for VOR/DME beacons even
    though the frequency uniquely determines it, per the ICAO channelling plan.
    """
    if hertz is None:
        return None
    for start, end, first_channel in (_VOR_TACAN_LOW_BAND, _VOR_TACAN_HIGH_BAND):
        if start <= hertz <= end:
            index = (hertz - start) // _VOR_TACAN_STEP_HZ
            band = TacanBand.X if index % 2 == 0 else TacanBand.Y
            return TacanChannel(first_channel + index // 2, band)
    return None


@dataclass(frozen=True)
class Beacon:
    name: str
    callsign: str
    beacon_type: BeaconType
    # DCS's beacons.lua omits the frequency for some beacons (e.g. TACAN-only ground
    # stations with no VHF pairing).
    hertz: Optional[int]
    channel: Optional[int]

    @property
    def frequency(self) -> RadioFrequency:
        return RadioFrequency(self.hertz or 0)

    @property
    def is_tacan(self) -> bool:
        return self.beacon_type in (
            BeaconType.BEACON_TYPE_VORTAC,
            BeaconType.BEACON_TYPE_TACAN,
        )

    @property
    def occupies_tacan_channel(self) -> bool:
        """True if a dynamically allocated TACAN on the same channel/band would
        conflict with this beacon.

        DME and VOR-DME beacons share TACAN's channelization (the DME portion is
        transmitted on the paired TACAN channel/frequency), so they must also be
        blacklisted even though they aren't TACAN beacons themselves.
        """
        return self.is_tacan or self.beacon_type in (
            BeaconType.BEACON_TYPE_DME,
            BeaconType.BEACON_TYPE_VOR_DME,
        )

    @property
    def tacan_channel(self) -> Optional[TacanChannel]:
        """The TACAN channel/band that would conflict with this beacon, if any.

        Prefers the channel/band derived from the VHF frequency (accurate for any
        beacon in the civil VOR band, including ones DCS didn't tag with a channel),
        falling back to the raw channel field (assumed X band, since DCS doesn't
        expose the actual band for TACAN-only ground beacons outside the VOR band).
        """
        assert self.occupies_tacan_channel
        if (channel := _tacan_channel_from_vor_frequency(self.hertz)) is not None:
            return channel
        if self.channel is not None:
            return TacanChannel(self.channel, TacanBand.X)
        return None


class Beacons:
    _by_terrain: dict[str, dict[str, Beacon]] = {}

    @classmethod
    def _load_for_theater_if_needed(cls, theater: ConflictTheater) -> None:
        if theater.terrain.name in cls._by_terrain:
            return

        beacons_filename_mapper = {
            "sinaimap": "sinai",
            "germanycw": "germanycoldwar",
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
