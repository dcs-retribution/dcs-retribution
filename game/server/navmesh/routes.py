from fastapi import APIRouter, Depends

from game import Game
from game.server import GameContext
from game.theater.player import Player
from .models import NavMeshJs, NavMeshSelectionUpdateJs

router: APIRouter = APIRouter(prefix="/navmesh")


@router.get("/", operation_id="get_navmesh", response_model=NavMeshJs)
def get(for_player: Player, game: Game = Depends(GameContext.require)) -> NavMeshJs:
    mesh = game.coalition_for(for_player).nav_mesh
    return NavMeshJs.from_navmesh(mesh, game)


@router.put("/selection", operation_id="set_navmesh_selection", status_code=204)
def set_selection(
    selection: NavMeshSelectionUpdateJs,
    for_player: Player,
    game: Game = Depends(GameContext.require),
) -> None:
    coalition = game.coalition_for(for_player)
    coalition.set_area_of_operations(selection.poly_ids)
