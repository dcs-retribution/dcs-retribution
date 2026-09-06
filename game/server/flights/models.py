from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel
from shapely.geometry import LineString, Point as ShapelyPoint

from game.ato.flightplans.tacticaloverlay import TacticalOverlay, TacticalOverlayDisplay
from game.ato.flightplans.uizonedisplay import UiZone, UiZoneDisplay
from game.ato.flightstate import InFlight
from game.ato.flightstate.killed import Killed
from game.server.leaflet import LeafletLine, LeafletPoint, LeafletPoly, ShapelyUtil
from game.server.waypoints.models import FlightWaypointJs
from game.server.waypoints.routes import waypoints_for_flight

if TYPE_CHECKING:
    from game import Game
    from game.ato import Flight
    from game.theater import ConflictTheater


class TacticalReachJs(BaseModel):
    polygon: LeafletPoly
    filled: bool

    class Config:
        title = "TacticalReach"


class TacticalTargetJs(BaseModel):
    position: LeafletPoint

    class Config:
        title = "TacticalTarget"


class TacticalOverlayJs(BaseModel):
    reach: list[TacticalReachJs]
    actual_path: LeafletLine | None = None
    targets: list[TacticalTargetJs]

    class Config:
        title = "TacticalOverlay"

    @staticmethod
    def from_overlay(
        overlay: TacticalOverlay, theater: ConflictTheater
    ) -> TacticalOverlayJs:
        reach = [
            TacticalReachJs(
                polygon=ShapelyUtil.poly_to_leaflet(shape.geometry, theater),
                filled=shape.filled,
            )
            for shape in overlay.reach
        ]
        actual_path: LeafletLine | None = None
        if overlay.actual_path:
            line = LineString([(p.x, p.y) for p in overlay.actual_path])
            actual_path = ShapelyUtil.line_to_leaflet(line, theater)
        targets = [
            TacticalTargetJs(position=LeafletPoint.from_latlng(t.position.latlng()))
            for t in overlay.targets
        ]
        return TacticalOverlayJs(reach=reach, actual_path=actual_path, targets=targets)

    @staticmethod
    def from_ui_zone(zone: UiZone, theater: ConflictTheater) -> TacticalOverlayJs:
        # Preserve the legacy commit-boundary look (a thin outline) for flights that only
        # expose ui_zone: players, support flights, and AI types without a bespoke overlay.
        if len(zone.points) == 1:
            center: ShapelyPoint | LineString = ShapelyPoint(
                zone.points[0].x, zone.points[0].y
            )
        else:
            center = LineString([(p.x, p.y) for p in zone.points])
        poly = center.buffer(zone.radius.meters)
        return TacticalOverlayJs(
            reach=[
                TacticalReachJs(
                    polygon=ShapelyUtil.poly_to_leaflet(poly, theater), filled=False
                )
            ],
            actual_path=None,
            targets=[],
        )

    @staticmethod
    def for_flight(flight: Flight, game: Game) -> TacticalOverlayJs:
        empty = TacticalOverlayJs(reach=[], actual_path=None, targets=[])
        plan = flight.flight_plan
        if flight.client_count == 0 and isinstance(plan, TacticalOverlayDisplay):
            return TacticalOverlayJs.from_overlay(plan.tactical_overlay(), game.theater)
        if isinstance(plan, UiZoneDisplay):
            return TacticalOverlayJs.from_ui_zone(plan.ui_zone(), game.theater)
        return empty


class FlightJs(BaseModel):
    id: UUID
    blue: bool
    position: LeafletPoint | None
    sidc: str
    waypoints: list[FlightWaypointJs] | None

    class Config:
        title = "Flight"

    @staticmethod
    def for_flight(flight: Flight, with_waypoints: bool) -> FlightJs:
        # Don't provide a location for aircraft that aren't in the air. Later we can
        # expand the model to include the state data for the UI so that it can make its
        # own decisions about whether to draw the aircraft, but for now we'll filter
        # here.
        #
        # We also draw dead aircraft so the player has some feedback about what's being
        # lost.
        position = None
        if isinstance(flight.state, InFlight) or isinstance(flight.state, Killed):
            position = flight.position().latlng()
        waypoints = None
        if with_waypoints:
            waypoints = waypoints_for_flight(flight)
        if flight.blue.is_blue:
            blue = True
        else:
            blue = False
        return FlightJs(
            id=flight.id,
            blue=blue,
            position=position,
            sidc=str(flight.sidc()),
            waypoints=waypoints,
        )

    @staticmethod
    def all_in_game(game: Game, with_waypoints: bool) -> list[FlightJs]:
        flights = []
        for coalition in game.coalitions:
            for package in coalition.ato.packages:
                for flight in package.flights:
                    flights.append(FlightJs.for_flight(flight, with_waypoints))
        return flights
