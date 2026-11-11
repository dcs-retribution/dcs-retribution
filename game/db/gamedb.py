from typing import Any, TYPE_CHECKING

from .database import Database

if TYPE_CHECKING:
    from game.ato import Flight
    from game.squadrons.downedpilot import DownedPilot
    from game.theater import FrontLine, TheaterGroundObject


class GameDb:
    def __init__(self) -> None:
        self.flights: Database[Flight] = Database()
        self.front_lines: Database[FrontLine] = Database()
        self.tgos: Database[TheaterGroundObject] = Database()
        self.downed_pilots: Database[DownedPilot] = Database()

    def __setstate__(self, state: dict[str, Any]) -> None:
        # CSAR postdates the oldest saves.
        if "downed_pilots" not in state:
            state["downed_pilots"] = Database()
        self.__dict__.update(state)
