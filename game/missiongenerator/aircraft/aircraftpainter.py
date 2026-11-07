from __future__ import annotations

import random
from typing import Any, Optional

from dcs.unitgroup import FlyingGroup

from game.ato import Flight
from game.dcs.aircrafttype import AircraftType
from game.factions import Faction
from .liveryallocator import LiveryAllocator
from .modex import MODEX_AIRCRAFT_IDS


class AircraftPainter:
    def __init__(
        self,
        flight: Flight,
        group: FlyingGroup[Any],
        livery_allocator: Optional[LiveryAllocator] = None,
    ) -> None:
        self.flight = flight
        self.group = group
        # None falls back to the random round-robin (tests, un-plumbed callers).
        self.livery_allocator = livery_allocator

    def livery_from_unit_type(self) -> Optional[str]:
        return self.flight.unit_type.default_livery

    def livery_from_faction(self) -> Optional[str]:
        faction = self.flight.squadron.coalition.faction
        if (
            choices := faction.liveries_overrides.get(self.flight.unit_type)
        ) is not None:
            return random.choice(choices)
        return None

    def livery_from_squadron(self) -> Optional[str]:
        return self.flight.squadron.livery

    def livery_from_squadron_set(
        self, member_uses_livery_set: bool, board_number: Optional[int] = None
    ) -> Optional[str]:
        if not (
            self.flight.squadron.livery_set
            and (self.flight.squadron.use_livery_set or member_uses_livery_set)
        ):
            return None
        # Navy only: other squadrons keep the random round-robin.
        if self.livery_allocator is not None and self._is_modex_squadron():
            return self.livery_allocator.next_livery(self.flight.squadron, board_number)
        return self.flight.squadron.random_round_robin_livery_from_set()

    def determine_livery(
        self, member_uses_livery_set: bool, board_number: Optional[int] = None
    ) -> Optional[str]:
        livery = self.livery_from_squadron_set(member_uses_livery_set, board_number)
        if livery is not None:
            return livery
        if (livery := self.livery_from_squadron()) is not None:
            return livery
        if (livery := self.livery_from_faction()) is not None:
            return livery
        if (livery := self.livery_from_unit_type()) is not None:
            return livery
        return None

    def apply_livery(self) -> None:
        for unit, member in zip(self.group.units, self.flight.iter_members()):
            livery = self.determine_livery(
                member.use_livery_set, self._meaningful_board_number(unit.onboard_num)
            )
            if not (livery or member.livery):
                continue
            unit.livery_id = member.livery if member.livery else livery
            assert isinstance(unit.livery_id, str)
            unit.livery_id = unit.livery_id.lower()

    def _is_modex_squadron(self) -> bool:
        return self.flight.unit_type.dcs_unit_type.id in MODEX_AIRCRAFT_IDS

    def _meaningful_board_number(self, onboard_num: str) -> Optional[int]:
        """The jet's modex, stamped before painting; None off the Navy set."""
        if not self._is_modex_squadron():
            return None
        try:
            return int(onboard_num)
        except (TypeError, ValueError):
            return None


class AircraftPainterJtac:
    def __init__(
        self, faction: Faction, unit_type: AircraftType, group: FlyingGroup[Any]
    ) -> None:
        self.faction = faction
        self.unit_type = unit_type
        self.group = group

    def livery_from_unit_type(self) -> Optional[str]:
        return self.unit_type.default_livery

    def livery_from_faction(self) -> Optional[str]:
        faction = self.faction

        if (choices := faction.liveries_overrides.get(self.unit_type)) is not None:
            return random.choice(choices)
        return None

    def determine_livery(self) -> Optional[str]:
        if (livery := self.livery_from_faction()) is not None:
            return livery
        if (livery := self.livery_from_unit_type()) is not None:
            return livery
        return None

    def apply_livery(self) -> None:
        livery = self.determine_livery()
        if livery is None:
            return
        for unit in self.group.units:
            unit.livery_id = livery
