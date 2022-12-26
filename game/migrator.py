from __future__ import annotations

from typing import TYPE_CHECKING

from game.ato.packagewaypoints import PackageWaypoints
from game.data.doctrine import MODERN_DOCTRINE, COLDWAR_DOCTRINE, WWII_DOCTRINE

if TYPE_CHECKING:
    from game import Game


class Migrator:
    def __init__(self, game: Game):
        self.game = game
        self._migrate_game()

    def _migrate_game(self) -> None:
        self._update_doctrine()
        self._update_packagewaypoints()

    def _update_doctrine(self) -> None:
        doctrines = [
            MODERN_DOCTRINE,
            COLDWAR_DOCTRINE,
            WWII_DOCTRINE,
        ]
        for c in self.game.coalitions:
            if c.faction.doctrine.__dict__ in [d.__dict__ for d in doctrines]:
                continue
            found = False
            for d in doctrines:
                if c.faction.doctrine.rendezvous_altitude == d.rendezvous_altitude:
                    c.faction.doctrine = d
                    found = True
                    break
            if not found:
                c.faction.doctrine = MODERN_DOCTRINE

    def _update_packagewaypoints(self) -> None:
        for c in self.game.coalitions:
            for p in c.ato.packages:
                if not hasattr(p.waypoints, "initial"):
                    p.waypoints = PackageWaypoints.create(p, c)
