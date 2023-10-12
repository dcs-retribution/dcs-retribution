from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QObject, Signal

from game import Game
from game.debriefing import Debriefing
from game.game import TurnState


class GameUpdateSignal(QObject):
    instance = None
    gameupdated = Signal(Game)
    budgetupdated = Signal(Game)
    game_state_changed = Signal(TurnState)
    debriefingReceived = Signal(Debriefing)

    game_loaded = Signal(Game)

    def __init__(self):
        super(GameUpdateSignal, self).__init__()
        GameUpdateSignal.instance = self

        self.game_loaded.connect(self.updateGame)

    def updateGame(self, game: Optional[Game]):
        # noinspection PyUnresolvedReferences
        self.gameupdated.emit(game)

    def updateBudget(self, game: Game):
        # noinspection PyUnresolvedReferences
        self.budgetupdated.emit(game)

    def sendDebriefing(self, debriefing: Debriefing) -> None:
        # noinspection PyUnresolvedReferences
        self.debriefingReceived.emit(debriefing)

    def gameStateChanged(self, state: TurnState):
        if state in (TurnState.WIN, TurnState.LOSS):
            # noinspection PyUnresolvedReferences
            self.game_state_changed.emit(state)

    @staticmethod
    def get_instance() -> GameUpdateSignal:
        return GameUpdateSignal.instance
