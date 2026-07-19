from fastapi import APIRouter, status
from starlette.responses import Response

from game.theater.fogofwar import fog_revealed, set_fog_revealed

router: APIRouter = APIRouter(prefix="/fog-of-war")


@router.get("/reveal", operation_id="get_fog_of_war_reveal", response_model=bool)
def get_reveal() -> bool:
    """Whether the fog-of-war overview is currently on."""
    return fog_revealed()


@router.put(
    "/reveal",
    operation_id="set_fog_of_war_reveal",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def set_reveal(revealed: bool) -> None:
    """Toggle the fog-of-war overview ("show the real picture").

    Runtime-only view state; never persisted. After flipping this the client
    re-pulls full game state, so the map redraws with (or without) the fogged
    enemy composition, threat/detection rings, and hidden command posts. The
    flag short-circuits the three fog leaves (``alive_for`` / ``known_for`` /
    ``hidden_on_player_map``) to ground truth for any viewer; AI/planner/threat
    math pass ``viewer=None`` and are unaffected.
    """
    set_fog_revealed(revealed)
