from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from dcs.task import Modulation

from game.missiongenerator.missiondata import AtisInfo
from game.radio.radios import RadioFrequency
from game.theater.controlpoint import Airfield

if TYPE_CHECKING:
    from game.ato.airtaaskingorder import AirTaskingOrder
    from game.radio.radios import RadioRegistry
    from game.theater.player import Player

logger = logging.getLogger(__name__)


class AtisGenerator:
    """Allocates one unique VHF-AM ATIS frequency per player-relevant airfield.

    Only airfields a player (client) flight departs from, arrives at, or
    diverts to get an ATIS station. DCS renders every concurrent
    ``trigger.action.radioTransmission`` into one shared audio mixer with a
    small (undocumented) number of voice slots, so an ATIS at every blue
    airfield saturates it and makes all stations stutter. Restricting to the
    handful of fields the player actually uses keeps the simultaneous-station
    count low enough for clean audio.

    Frequencies are reserved on the shared ``RadioRegistry`` so they cannot
    collide with package / intra-flight / AWACS / tanker frequencies already
    allocated. Allocation order is deterministic (airfield-name sort) so a
    field keeps the same ATIS frequency across regenerated turns where the
    covered-field set is unchanged.
    """

    def __init__(
        self,
        ato: "AirTaskingOrder",
        radio_registry: "RadioRegistry",
        friendly: "Player",
        *,
        base_mhz: float = 131.0,
        spacing_khz: int = 500,
        window_max_mhz: float = 140.0,
    ) -> None:
        self.ato = ato
        self.radio_registry = radio_registry
        self.friendly = friendly
        self.base_mhz = base_mhz
        self.spacing_khz = spacing_khz
        self.window_max_mhz = window_max_mhz

    def _atis_airfields(self) -> list[Airfield]:
        # Collect the departure / arrival / divert airfields of every player
        # (client) flight, deduped by name. AI-only flights are excluded so an
        # all-AI turn produces no ATIS at all.
        airfields: dict[str, Airfield] = {}
        for package in self.ato.packages:
            for flight in package.flights:
                if not flight.client_count:
                    continue
                for cp in (flight.departure, flight.arrival, flight.divert):
                    if isinstance(cp, Airfield) and cp.is_friendly(self.friendly):
                        airfields[cp.full_name] = cp
        return sorted(airfields.values(), key=lambda cp: cp.full_name)

    def _next_free_frequency(self, start_slot: int) -> tuple[RadioFrequency, int]:
        """Return the next unreserved VHF-AM frequency at/after ``start_slot``.

        Raises ``StopIteration`` when the window is exhausted.
        """
        slot = start_slot
        window_max_hz = int(round(self.window_max_mhz * 1_000_000))
        base_hz = int(round(self.base_mhz * 1_000_000))
        step_hz = self.spacing_khz * 1_000
        while True:
            hertz = base_hz + slot * step_hz
            if hertz >= window_max_hz:
                raise StopIteration
            freq = RadioFrequency(hertz, Modulation.AM)
            slot += 1
            if freq not in self.radio_registry.allocated_channels:
                self.radio_registry.reserve(freq)
                return freq, slot

    def generate(self) -> list[AtisInfo]:
        result: list[AtisInfo] = []
        slot = 0
        for airfield in self._atis_airfields():
            try:
                freq, slot = self._next_free_frequency(slot)
            except StopIteration:
                logger.warning(
                    "ATIS frequency band exhausted (base %.3f MHz, %d kHz spacing, "
                    "max %.3f MHz); skipping ATIS for %s and any remaining fields.",
                    self.base_mhz,
                    self.spacing_khz,
                    self.window_max_mhz,
                    airfield.full_name,
                )
                break
            result.append(AtisInfo(airfield_name=airfield.full_name, frequency=freq))
        return result
