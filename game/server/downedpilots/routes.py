from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from game import Game
from .models import DownedPilotJs
from ..dependencies import GameContext

router: APIRouter = APIRouter(prefix="/downed-pilots")


@router.get("/", operation_id="list_downed_pilots", response_model=list[DownedPilotJs])
def list_downed_pilots(
    game: Game = Depends(GameContext.require),
) -> list[DownedPilotJs]:
    return DownedPilotJs.all_in_game(game)


@router.get(
    "/{pilot_id}",
    operation_id="get_downed_pilot_by_id",
    response_model=DownedPilotJs,
)
def get_downed_pilot(
    pilot_id: UUID, game: Game = Depends(GameContext.require)
) -> DownedPilotJs:
    try:
        downed = game.db.downed_pilots.get(pilot_id)
    except KeyError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Game has no downed pilot with ID {pilot_id}",
        )
    return DownedPilotJs.for_pilot(downed)
