from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel

from game.server.leaflet import LeafletPoint

if TYPE_CHECKING:
    from game import Game
    from game.squadrons.downedpilot import DownedPilot


class DownedPilotJs(BaseModel):
    id: UUID
    name: str
    squadron: str
    aircraft: str
    blue: bool
    position: LeafletPoint
    turns_remaining: int
    sidc: str

    class Config:
        title = "DownedPilot"

    @staticmethod
    def for_pilot(downed: DownedPilot) -> DownedPilotJs:
        return DownedPilotJs(
            id=downed.id,
            name=downed.pilot.name,
            squadron=str(downed.squadron),
            aircraft=downed.aircraft_name,
            blue=downed.player.is_blue,
            position=downed.position.latlng(),
            turns_remaining=downed.turns_remaining,
            sidc=str(downed.sidc()),
        )

    @staticmethod
    def all_in_game(game: Game) -> list[DownedPilotJs]:
        # Both coalitions are exposed. The map already shows enemy flights and
        # ground objects, so hiding red downed pilots would be inconsistent, and
        # seeing opfor rescues in progress is useful. The `blue` flag drives the
        # icon colour on the map.
        return [
            DownedPilotJs.for_pilot(downed)
            for coalition in (game.blue, game.red)
            for downed in coalition.downed_pilots
        ]
