"""Regression tests for save-game migration (game.migrator.Migrator)."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import MagicMock
from uuid import uuid4

from game.migrator import Migrator
from game.squadrons.squadron import Squadron


def _qra_squadron(owned: int, reserve: int) -> Squadron:
    """A minimal squadron holding a QRA reserve, with no pilot roster.

    Built without __init__ -- the migrator path under test only touches
    inventory counts, the (empty) roster, and claim_available_pilot (mocked).
    """
    squadron = Squadron.__new__(Squadron)
    squadron.id = uuid4()
    squadron.name = "010"
    squadron.owned_aircraft = owned
    squadron.intercept_reserve = reserve
    squadron.current_roster = []
    squadron.available_pilots = []
    return squadron


def test_release_untasked_flights_respects_qra_reserve() -> None:
    """An old save whose flights were planned against the full owned count must
    still load once the squadron holds a QRA reserve.

    return_all_pilots_and_aircraft() benches the reserve (untasked = owned -
    intercept_reserve), so _release_untasked_flights must claim against
    untasked_aircraft, not owned_aircraft -- otherwise claim_inventory raises
    "Cannot remove 14 from Squadron 010. Only have 10." and the app reports the
    save as incompatible.
    """
    squadron = _qra_squadron(owned=14, reserve=4)  # untasked == 10
    # Flights task all 14 airframes -- more than the 10 untasked after reserve.
    flights = [SimpleNamespace(squadron=squadron, count=7) for _ in range(2)]
    squadron.flight_db = cast(
        Any, SimpleNamespace(objects={i: f for i, f in enumerate(flights)})
    )
    squadron.claim_available_pilot = MagicMock()  # type: ignore[method-assign]

    cp = SimpleNamespace(squadrons=[squadron])
    game = cast(Any, SimpleNamespace(theater=SimpleNamespace(controlpoints=[cp])))

    migrator = Migrator.__new__(Migrator)
    migrator.game = game

    migrator._release_untasked_flights()  # must not raise

    assert squadron.untasked_aircraft == 0  # all 10 untasked claimed by flights
    assert squadron.owned_aircraft == 14  # owned unchanged; 4 still on reserve
    assert squadron.claim_available_pilot.call_count == 10


def test_release_untasked_flights_zero_reserve_unchanged() -> None:
    """With no QRA reserve, untasked == owned, so behaviour is the pre-fix one:
    flights claim min(count, owned)."""
    squadron = _qra_squadron(owned=10, reserve=0)
    flights = [SimpleNamespace(squadron=squadron, count=3)]
    squadron.flight_db = cast(Any, SimpleNamespace(objects={0: flights[0]}))
    squadron.claim_available_pilot = MagicMock()  # type: ignore[method-assign]

    cp = SimpleNamespace(squadrons=[squadron])
    game = cast(Any, SimpleNamespace(theater=SimpleNamespace(controlpoints=[cp])))

    migrator = Migrator.__new__(Migrator)
    migrator.game = game
    migrator._release_untasked_flights()

    assert squadron.untasked_aircraft == 7  # 10 owned - 3 claimed
    assert squadron.claim_available_pilot.call_count == 3
