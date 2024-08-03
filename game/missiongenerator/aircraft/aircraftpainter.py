from __future__ import annotations

import random
from typing import Any, Optional

from dcs.unitgroup import FlyingGroup

from game.ato import Flight


class AircraftPainter:
    def __init__(self, flight: Flight, group: FlyingGroup[Any]) -> None:
        self.flight = flight
        self.group = group

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

    def livery_from_squadron_set(self, member_uses_livery_set: bool) -> Optional[str]:
        if not (
            self.flight.squadron.livery_set
            and (self.flight.squadron.use_livery_set or member_uses_livery_set)
        ):
            return None
        return random.choice(self.flight.squadron.livery_set)

    def determine_livery(self, member_uses_livery_set: bool) -> Optional[str]:
        livery = self.livery_from_squadron_set(member_uses_livery_set)
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
            livery = self.determine_livery(member.use_livery_set)
            if not (livery or member.livery):
                continue
            unit.livery_id = member.livery if member.livery else livery
            assert isinstance(unit.livery_id, str)
            unit.livery_id = unit.livery_id.lower()
