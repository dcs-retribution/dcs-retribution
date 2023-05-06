from __future__ import annotations

from typing import TYPE_CHECKING, Any

from game.ato.packagewaypoints import PackageWaypoints
from game.data.doctrine import MODERN_DOCTRINE, COLDWAR_DOCTRINE, WWII_DOCTRINE

if TYPE_CHECKING:
    from game import Game


def try_set_attr(obj: Any, attr_name: str, val: Any = None) -> None:
    if not hasattr(obj, attr_name):
        setattr(obj, attr_name, val)


class Migrator:
    def __init__(self, game: Game):
        self.game = game
        self._migrate_game()

    def _migrate_game(self) -> None:
        self._update_doctrine()
        self._update_packagewaypoints()
        self._update_package_attributes()
        self._update_control_points()
        self._update_flights()
        self._release_untasked_flights()

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
                if p.waypoints:
                    try_set_attr(p.waypoints, "initial", None)

    def _update_package_attributes(self) -> None:
        for c in self.game.coalitions:
            for p in c.ato.packages:
                try_set_attr(p, "custom_name")
                try_set_attr(p, "frequency")

    def _update_control_points(self) -> None:
        for cp in self.game.theater.controlpoints:
            is_carrier = cp.is_carrier
            is_lha = cp.is_lha
            is_fob = cp.category == "fob"
            radio_configurable = is_carrier or is_lha or is_fob
            if radio_configurable:
                try_set_attr(cp, "frequency")
            if is_carrier or is_lha:
                try_set_attr(cp, "tacan")
                try_set_attr(cp, "tcn_name")
                try_set_attr(cp, "icls_channel")
                try_set_attr(cp, "icls_name")
                try_set_attr(cp, "link4")

    def _update_flights(self) -> None:
        for f in self.game.db.flights.objects.values():
            try_set_attr(f, "frequency")
            try_set_attr(f, "tacan")
            try_set_attr(f, "tcn_name")
            try_set_attr(f, "fuel", f.unit_type.max_fuel)

    def _release_untasked_flights(self) -> None:
        for cp in self.game.theater.controlpoints:
            for s in cp.squadrons:
                claimed = s.owned_aircraft - s.untasked_aircraft
                count = 0
                for f in s.flight_db.objects.values():
                    if f.squadron == s:
                        count += f.count
                s.claim_inventory(count - claimed)
