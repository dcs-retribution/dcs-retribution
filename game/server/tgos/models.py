from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from pydantic import BaseModel

from game.dcs.groundunittype import GroundUnitType
from game.ground_forces.ai_ground_planner import reserve_armor_for
from game.missiongenerator.motorpoolpopulator import (
    MotorpoolPopulator,
    motorpools_at,
    select_capped,
)
from game.server.leaflet import LeafletPoint
from game.theater.theatergroundobject import MotorpoolGroundObject, ShipGroundObject

if TYPE_CHECKING:
    from game import Game
    from game.theater import TheaterGroundObject


class AggregateGroundUnitEntry(BaseModel):
    unit_type: str
    display_name: str
    count: int


class TgoJs(BaseModel):
    id: UUID
    name: str
    control_point_name: str
    category: str
    blue: bool
    position: LeafletPoint
    units: list[str]  # TODO: Event stream
    reserve_units: list[str]
    expected_inventory: list[AggregateGroundUnitEntry]
    unrendered_reserve: list[AggregateGroundUnitEntry]
    in_transit_units: list[AggregateGroundUnitEntry]
    threat_ranges: list[float]  # TODO: Event stream
    detection_ranges: list[float]  # TODO: Event stream
    dead: bool  # TODO: Event stream
    sidc: str  # TODO: Event stream
    task: Optional[tuple[str, str]]
    mobile: bool
    destination: Optional[LeafletPoint]

    class Config:
        title = "Tgo"

    @staticmethod
    def _aggregate_entries(
        counts: dict[GroundUnitType, int],
    ) -> list[AggregateGroundUnitEntry]:
        return [
            AggregateGroundUnitEntry(
                unit_type=unit_type.variant_id,
                display_name=unit_type.display_name,
                count=count,
            )
            for unit_type, count in sorted(
                counts.items(), key=lambda item: item[0].variant_id
            )
            if count > 0
        ]

    @staticmethod
    def for_tgo(tgo: TheaterGroundObject) -> TgoJs:
        threat_ranges = [group.max_threat_range().meters for group in tgo.groups]
        detection_ranges = [group.max_detection_range().meters for group in tgo.groups]
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
        reserve_units: list[str] = []
        expected_inventory: list[AggregateGroundUnitEntry] = []
        unrendered_reserve: list[AggregateGroundUnitEntry] = []
        in_transit_units: list[AggregateGroundUnitEntry] = []
        if isinstance(tgo, MotorpoolGroundObject):
            MotorpoolPopulator(
                tgo.control_point.coalition.game
            ).populate_control_points([tgo.control_point])
            reserve_units = [unit.display_name for unit in tgo.units]
            motorpools = motorpools_at(tgo.control_point)
            if motorpools and motorpools[0] is tgo:
                reserve = reserve_armor_for(tgo.control_point)
                pending_orders = tgo.control_point.ground_unit_orders.units
                current_inventory = {
                    unit_type: tgo.control_point.base.total_units_of_type(unit_type)
                    for unit_type in set(tgo.control_point.base.armor)
                    | set(pending_orders)
                }
                expected_inventory = TgoJs._aggregate_entries(
                    {
                        unit_type: count
                        + tgo.control_point.ground_unit_orders.pending_orders(unit_type)
                        for unit_type, count in current_inventory.items()
                    }
                )
                settings = tgo.control_point.coalition.game.settings
                selected = (
                    select_capped(reserve, settings.motorpool_spawn_cap)
                    if settings.motorpool_enabled
                    else {}
                )
                unrendered_reserve = TgoJs._aggregate_entries(
                    {
                        unit_type: count - selected.get(unit_type, 0)
                        for unit_type, count in reserve.items()
                    }
                )
                transit: defaultdict[GroundUnitType, int] = defaultdict(int)
                for coalition in tgo.control_point.coalition.game.coalitions:
                    for transfer in coalition.transfers:
                        if transfer.origin != tgo.control_point:
                            continue
                        for unit_type, count in transfer.units.items():
                            transit[unit_type] += count
                in_transit_units = TgoJs._aggregate_entries(dict(transit))
        return TgoJs(
            id=tgo.id,
            name=tgo.name,
            control_point_name=tgo.control_point.name,
            category=tgo.category,
            blue=blue,
            position=tgo.position.latlng(),
            units=[unit.display_name for unit in tgo.units],
            reserve_units=reserve_units,
            expected_inventory=expected_inventory,
            unrendered_reserve=unrendered_reserve,
            in_transit_units=in_transit_units,
            threat_ranges=threat_ranges,
            detection_ranges=detection_ranges,
            dead=tgo.is_dead,
            sidc=str(tgo.sidc()),
            task=(
                (
                    tgo.groups[0].ground_object.task.description,
                    tgo.groups[0].ground_object.task.role.value,
                )
                if tgo.groups and tgo.groups[0].ground_object.task is not None
                else None
            ),
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
