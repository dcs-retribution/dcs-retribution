from uuid import UUID

from fastapi import APIRouter, Depends

from game import Game
from game.server import GameContext
from game.server.flights.models import FlightJs, TacticalOverlayJs

router: APIRouter = APIRouter(prefix="/flights")


@router.get("/", operation_id="list_flights", response_model=list[FlightJs])
def list_flights(
    with_waypoints: bool = False, game: Game = Depends(GameContext.require)
) -> list[FlightJs]:
    return FlightJs.all_in_game(game, with_waypoints)


@router.get("/{flight_id}", operation_id="get_flight_by_id", response_model=FlightJs)
def get_flight(
    flight_id: UUID,
    with_waypoints: bool = False,
    game: Game = Depends(GameContext.require),
) -> FlightJs:
    flight = game.db.flights.get(flight_id)
    return FlightJs.for_flight(flight, with_waypoints)


@router.get(
    "/{flight_id}/tactical-overlay",
    operation_id="get_tactical_overlay_for_flight",
    response_model=TacticalOverlayJs,
)
def tactical_overlay(
    flight_id: UUID, game: Game = Depends(GameContext.require)
) -> TacticalOverlayJs:
    flight = game.db.flights.get(flight_id)
    return TacticalOverlayJs.for_flight(flight, game)
