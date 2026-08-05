from uuid import UUID

from dcs import Point
from dcs.mapping import LatLng
from fastapi import APIRouter, Body, Depends, HTTPException, status
from starlette.responses import Response

from game import Game
from .models import TgoJs
from ..dependencies import GameContext
from ..leaflet import LeafletPoint
from game.theater.theatergroundobject import ShipGroundObject

router: APIRouter = APIRouter(prefix="/tgos")


@router.get("/", operation_id="list_tgos", response_model=list[TgoJs])
def list_tgos(game: Game = Depends(GameContext.require)) -> list[TgoJs]:
    return TgoJs.all_in_game(game)


@router.get("/{tgo_id}", operation_id="get_tgo_by_id", response_model=TgoJs)
def get_tgo(tgo_id: UUID, game: Game = Depends(GameContext.require)) -> TgoJs:
    return TgoJs.for_tgo(game.db.tgos.get(tgo_id))


@router.get(
    "/{tgo_id}/destination-in-range",
    operation_id="tgo_destination_in_range",
    response_model=bool,
)
def tgo_destination_in_range(
    tgo_id: UUID, lat: float, lng: float, game: Game = Depends(GameContext.require)
) -> bool:
    tgo = game.db.tgos.get(tgo_id)
    if not isinstance(tgo, ShipGroundObject):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail=f"{tgo} is not a movable ship"
        )
    if not tgo.control_point.captured.is_blue:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail=f"{tgo} is not owned by the player"
        )
    point = Point.from_latlng(LatLng(lat, lng), game.theater.terrain)
    return tgo.destination_in_range(point)


@router.put(
    "/{tgo_id}/destination",
    operation_id="set_tgo_destination",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def set_tgo_destination(
    tgo_id: UUID,
    destination: LeafletPoint = Body(..., title="destination"),
    game: Game = Depends(GameContext.require),
) -> None:
    tgo = game.db.tgos.get(tgo_id)
    if not isinstance(tgo, ShipGroundObject):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail=f"{tgo} is not a movable ship"
        )
    if not tgo.control_point.captured.is_blue:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail=f"{tgo} is not owned by the player"
        )
    point = Point.from_latlng(
        LatLng(destination.lat, destination.lng), game.theater.terrain
    )
    if not tgo.destination_in_range(point):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot move {tgo} more than "
            f"{tgo.max_move_distance.nautical_miles}nm.",
        )
    # Only enforce the sea/land constraint when the theater has a landmap;
    # without one is_in_sea() returns False for every point, which would reject
    # all moves (carriers face the same gap and likewise skip the check).
    if game.theater.landmap and (
        not game.theater.is_in_sea(point)
        or game.theater.landmap.land_inbetween(tgo.position, point)
    ):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot move {tgo} over land or out of the sea.",
        )
    tgo.target_position = point
    from .. import EventStream

    with EventStream.event_context() as events:
        events.update_tgo(tgo)


@router.put(
    "/{tgo_id}/cancel-travel",
    operation_id="clear_tgo_destination",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def clear_tgo_destination(
    tgo_id: UUID, game: Game = Depends(GameContext.require)
) -> None:
    tgo = game.db.tgos.get(tgo_id)
    if not isinstance(tgo, ShipGroundObject):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail=f"{tgo} is not a movable ship"
        )
    if not tgo.control_point.captured.is_blue:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail=f"{tgo} is not owned by the player"
        )
    tgo.target_position = None
    from .. import EventStream

    with EventStream.event_context() as events:
        events.update_tgo(tgo)
