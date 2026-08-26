from __future__ import annotations

from types import SimpleNamespace
from typing import cast

from game.settings import Settings
from game.squadrons.squadron import Squadron


def _bare_squadron(
    owned: int, reserve: int, intercept_enabled: bool = True
) -> Squadron:
    squadron = Squadron.__new__(Squadron)
    squadron.current_roster = []
    squadron.owned_aircraft = owned
    squadron.intercept_reserve = reserve
    squadron.settings = cast(
        Settings, SimpleNamespace(plugins={"intercept": intercept_enabled})
    )
    return squadron


def test_reset_holds_back_qra_reserve_from_plannable_inventory() -> None:
    squadron = _bare_squadron(owned=10, reserve=4)
    squadron.return_all_pilots_and_aircraft()
    assert squadron.untasked_aircraft == 6


def test_reset_with_zero_reserve_leaves_all_aircraft_plannable() -> None:
    squadron = _bare_squadron(owned=10, reserve=0)
    squadron.return_all_pilots_and_aircraft()
    assert squadron.untasked_aircraft == 10


def test_reset_clamps_plannable_inventory_at_zero() -> None:
    squadron = _bare_squadron(owned=3, reserve=5)
    squadron.return_all_pilots_and_aircraft()
    assert squadron.untasked_aircraft == 0


def test_reset_benches_reserve_regardless_of_plugin_flag() -> None:
    # The reserve (intercept_reserve > 0) is the single on/off switch for QRA:
    # emission and loss commit gate on it alone, so benching must too. The plugin
    # flag must NOT change benching, otherwise a reserve could be both
    # ATO-plannable and fielded as QRA.
    squadron = _bare_squadron(owned=10, reserve=4, intercept_enabled=False)
    squadron.return_all_pilots_and_aircraft()
    assert squadron.untasked_aircraft == 6


def test_set_intercept_reserve_releases_jets_into_pool_immediately() -> None:
    # Editing the reserve mid-turn must update the plannable pool at once, without
    # a full return_all_pilots_and_aircraft() (which would return tasked flights).
    squadron = _bare_squadron(owned=10, reserve=4)
    squadron.return_all_pilots_and_aircraft()
    assert squadron.untasked_aircraft == 6

    squadron.set_intercept_reserve(0)
    assert squadron.intercept_reserve == 0
    assert squadron.untasked_aircraft == 10


def test_set_intercept_reserve_benches_jets_immediately() -> None:
    squadron = _bare_squadron(owned=10, reserve=0)
    squadron.return_all_pilots_and_aircraft()
    assert squadron.untasked_aircraft == 10

    squadron.set_intercept_reserve(4)
    assert squadron.intercept_reserve == 4
    assert squadron.untasked_aircraft == 6
