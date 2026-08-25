"""Curated per-hull carrier comms plans.

DCS auto-generates a "CV Operations Data" kneeboard page straight from the
mission file, so the only way to make it read like a real boat card is to put
real data in the miz. Before this table the generator dealt the boat whatever
came out of the allocators: TACAN 1X with a random ident re-rolled every turn,
ICLS channel 1, a Link 4 on a random inter-flight UHF like 255.0, and a fresh
random ATC frequency each mission.

These plans follow the pro-campaign "Mother card" convention (Raven One's
HOMEPLATE row is the model): TACAN channel matches the hull number with a
boat-name ident, ICLS is hull-keyed, Link 4 lives in the real ACLS 336 MHz
band, and the ATC frequency is a stable, memorable UHF. Every value is a
default, not a mandate — a channel already reserved (map beacon, another
boat) falls back to the legacy allocator, and values stored on the control
point (user-set or persisted from an earlier turn) always win.

Keyed by the pydcs ship type id. Hulls without an entry (mod carriers) keep
the legacy allocator behavior end to end.
"""

from dataclasses import dataclass
from typing import Optional

from dcs.ships import (
    CVN_71,
    CVN_72,
    CVN_73,
    CVN_75,
    CV_1143_5,
    Forrestal,
    KUZNECOW,
    LHA_Tarawa,
    Stennis,
)

from game.radio.radios import MHz, RadioFrequency
from game.radio.tacan import TacanBand, TacanChannel


@dataclass(frozen=True)
class CarrierCommsPlan:
    """The signature comms data for one hull."""

    tacan: TacanChannel
    tacan_ident: str
    atc: RadioFrequency
    icls: Optional[int] = None
    link4: Optional[RadioFrequency] = None


def _cv(
    tacan_channel: int,
    ident: str,
    atc_mhz: int,
    icls: Optional[int] = None,
    link4_khz: Optional[int] = None,
) -> CarrierCommsPlan:
    return CarrierCommsPlan(
        tacan=TacanChannel(tacan_channel, TacanBand.X),
        tacan_ident=ident,
        atc=MHz(atc_mhz),
        icls=icls,
        link4=MHz(336, link4_khz) if link4_khz is not None else None,
    )


# TACAN channels follow the hull number where that channel is legal for a
# ground/ship transmit-receive beacon (channels 2-30 and 47-63 X are not; see
# UNAVAILABLE in game/radio/tacan.py) -- Forrestal (59) and Tarawa (hull 1)
# take the nearest legal channels instead. A channel a map's real beacons
# already own (Bagram is 74X on Afghanistan) degrades at generation to the
# nearest free channel, not to the bottom of the band.
CARRIER_COMMS_PLANS: dict[str, CarrierCommsPlan] = {
    Forrestal.id: _cv(64, "FID", 304, icls=9, link4_khz=900),
    CVN_71.id: _cv(71, "TRO", 305, icls=11, link4_khz=100),
    CVN_72.id: _cv(72, "ABE", 306, icls=12, link4_khz=200),
    CVN_73.id: _cv(73, "GWN", 307, icls=13, link4_khz=300),
    Stennis.id: _cv(74, "STN", 308, icls=14, link4_khz=400),
    CVN_75.id: _cv(75, "HST", 309, icls=15, link4_khz=500),
    LHA_Tarawa.id: _cv(41, "TAR", 310, icls=1),
    KUZNECOW.id: _cv(35, "KUZ", 311),
    CV_1143_5.id: _cv(36, "KUZ", 312),
}
