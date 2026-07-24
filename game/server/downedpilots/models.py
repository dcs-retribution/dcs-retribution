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
        # Only the player coalition's downed pilots are exposed; enemy downed
        # pilots stay hidden from the map.
        return [DownedPilotJs.for_pilot(downed) for downed in game.blue.downed_pilots]
