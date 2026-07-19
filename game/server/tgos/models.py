from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from uuid import UUID

from pydantic import BaseModel

from game.data.groups import GroupTask
from game.server.leaflet import LeafletPoint
from game.theater.player import Player
from game.theater.theatergroundobject import ShipGroundObject

if TYPE_CHECKING:
    from game import Game
    from game.theater import TheaterGroundObject


class TgoJs(BaseModel):
    id: UUID
    name: str
    control_point_name: str
    category: str
    blue: bool
    position: LeafletPoint
    units: list[str]  # TODO: Event stream
    threat_ranges: list[float]  # TODO: Event stream
    detection_ranges: list[float]  # TODO: Event stream
    dead: bool  # TODO: Event stream
    sidc: str  # TODO: Event stream
    task: Optional[GroupTask]
    mobile: bool
    destination: Optional[LeafletPoint]

    class Config:
        title = "Tgo"

    @staticmethod
    def for_tgo(tgo: TheaterGroundObject) -> TgoJs:
        threat_ranges: list[float]
        detection_ranges: list[float]
        units: list[str]
        if tgo.known_for(Player.BLUE):
            threat_ranges = [group.max_threat_range().meters for group in tgo.groups]
            detection_ranges = [
                group.max_detection_range().meters for group in tgo.groups
            ]
            units = [unit.display_name for unit in tgo.units]
            dead = tgo.is_dead
        else:
            # Recon intel-fog: the site stays on the map and remains targetable
            # (position, category, allegiance), but its actual composition and
            # threat/detection rings are hidden until it is attacked, scouted, or
            # has a unit destroyed.
            threat_ranges = []
            detection_ranges = []
            units = []
            dead = False
        if tgo.control_point.captured.is_blue:
            blue = True
        else:
            blue = False
        mobile = isinstance(tgo, ShipGroundObject) and blue
        destination: Optional[LeafletPoint] = None
        if (
            isinstance(tgo, ShipGroundObject)
            and blue
            and tgo.target_position is not None
        ):
            destination = LeafletPoint.from_latlng(tgo.target_position.latlng())
        return TgoJs(
            id=tgo.id,
            name=tgo.name,
            control_point_name=tgo.control_point.name,
            category=tgo.category,
            blue=blue,
            position=tgo.position.latlng(),
            units=units,
            threat_ranges=threat_ranges,
            detection_ranges=detection_ranges,
            dead=dead,
            sidc=str(tgo.sidc()),
            task=tgo.groups[0].ground_object.task if tgo.groups else None,
            mobile=mobile,
            destination=destination,
        )

    @staticmethod
    def all_in_game(game: Game) -> list[TgoJs]:
        tgos = []
        for control_point in game.theater.controlpoints:
            for tgo in control_point.connected_objectives:
                if not tgo.is_control_point:
                    tgos.append(TgoJs.for_tgo(tgo))
        return tgos
