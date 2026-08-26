from __future__ import annotations

from types import SimpleNamespace
from typing import cast

from game.coalition import Coalition
from game.game import Game
from game.settings import Settings


def test_coordinator_maps_ownfor_to_blue_and_opfor_to_red() -> None:
    recorded: list[tuple[str, int, int]] = []

    def _wing(tag: str) -> SimpleNamespace:
        return SimpleNamespace(
            repropagate_qra_reserve=(
                lambda old, new, _tag=tag: recorded.append((_tag, old, new))
            )
        )

    game = Game.__new__(Game)
    game.blue = cast(Coalition, SimpleNamespace(air_wing=_wing("blue")))
    game.red = cast(Coalition, SimpleNamespace(air_wing=_wing("red")))
    game.settings = cast(
        Settings,
        SimpleNamespace(ownfor_default_qra_reserve=4, opfor_default_qra_reserve=3),
    )

    game.repropagate_qra_reserves(old_ownfor=0, old_opfor=1)

    # New values come from settings; blue<-OWNFOR, red<-OPFOR, not swapped.
    assert recorded == [("blue", 0, 4), ("red", 1, 3)]
