"""Regression tests for QRA attrition reconciliation in
``MissionResultsProcessor.commit_intercept_losses``.

The dispatcher is only seeded with the *fielded* count
(``qra_resource_count`` = reserve capped by owned airframes and untasked
pilots), and the Lua bounds reported survivors by that fielded count. The loss
baseline must therefore be the fielded count, not the raw ``intercept_reserve``
-- otherwise an under-strength squadron loses airframes (and pilots) that never
flew, and does so every turn, spiralling to zero with no combat.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, cast
from uuid import uuid4

from game.debriefing import Debriefing
from game.settings import Settings
from game.sim.missionresultsprocessor import MissionResultsProcessor
from game.squadrons.pilot import Pilot
from game.squadrons.squadron import Squadron


def _squadron(*, reserve: int, owned: int, pilots: int, pilot_limits: bool) -> Squadron:
    squadron = Squadron.__new__(Squadron)
    squadron.id = uuid4()
    squadron.name = "Test Squadron"
    squadron.nickname = None
    squadron.intercept_reserve = reserve
    squadron.owned_aircraft = owned
    squadron.available_pilots = [Pilot(f"AI {i}") for i in range(pilots)]
    squadron.settings = cast(
        Settings,
        SimpleNamespace(
            invulnerable_player_pilots=False,
            enable_squadron_pilot_limits=pilot_limits,
        ),
    )
    return squadron


def _processor(squadrons: list[Squadron]) -> MissionResultsProcessor:
    return _processor_split(squadrons, [])


def _processor_split(
    blue: list[Squadron], red: list[Squadron]
) -> MissionResultsProcessor:
    game = SimpleNamespace(
        blue=SimpleNamespace(air_wing=SimpleNamespace(iter_squadrons=lambda: blue)),
        red=SimpleNamespace(air_wing=SimpleNamespace(iter_squadrons=lambda: red)),
    )
    return MissionResultsProcessor(cast(Any, game))


def _debrief(survivors: dict[str, int]) -> Debriefing:
    return cast(
        Debriefing,
        SimpleNamespace(state_data=SimpleNamespace(intercept_survivors=survivors)),
    )


def test_understrength_squadron_takes_no_phantom_loss() -> None:
    # reserve 6 but only 4 owned -> fields 4; all 4 survive -> zero real losses.
    squadron = _squadron(reserve=6, owned=4, pilots=4, pilot_limits=False)
    processor = _processor([squadron])
    processor.commit_intercept_losses(_debrief({str(squadron.id): 4}))
    assert squadron.owned_aircraft == 4
    assert len(squadron.available_pilots) == 4


def test_pilot_capped_squadron_takes_no_phantom_loss() -> None:
    # reserve 6, 10 owned, but only 3 untasked pilots -> fields 3; all survive.
    squadron = _squadron(reserve=6, owned=10, pilots=3, pilot_limits=True)
    processor = _processor([squadron])
    processor.commit_intercept_losses(_debrief({str(squadron.id): 3}))
    assert squadron.owned_aircraft == 10
    assert len(squadron.available_pilots) == 3


def test_genuine_losses_still_applied() -> None:
    # reserve 6, 10 owned, pilots ample -> fields 6; only 2 survive -> 4 lost.
    squadron = _squadron(reserve=6, owned=10, pilots=8, pilot_limits=False)
    processor = _processor([squadron])
    processor.commit_intercept_losses(_debrief({str(squadron.id): 2}))
    assert squadron.owned_aircraft == 6
    assert len(squadron.available_pilots) == 4


def test_pilot_limits_enabled_owned_is_binding_no_phantom_loss() -> None:
    # pilot limits on, but owned (2) binds below both reserve (6) and pilots (10)
    # -> fields 2; both survive -> no loss, no pilot deaths.
    squadron = _squadron(reserve=6, owned=2, pilots=10, pilot_limits=True)
    processor = _processor([squadron])
    processor.commit_intercept_losses(_debrief({str(squadron.id): 2}))
    assert squadron.owned_aircraft == 2
    assert len(squadron.available_pilots) == 10


def test_pilot_limited_squadron_genuine_losses() -> None:
    # pilot limits on, pilots (4) bind -> fields 4; 1 survives -> 3 lost, 3 pilots
    # killed (AI), owned drops 10 -> 7.
    squadron = _squadron(reserve=6, owned=10, pilots=4, pilot_limits=True)
    processor = _processor([squadron])
    processor.commit_intercept_losses(_debrief({str(squadron.id): 1}))
    assert squadron.owned_aircraft == 7
    assert len(squadron.available_pilots) == 1


def test_red_coalition_losses_committed() -> None:
    # A squadron in only the red wing is processed identically; guards against a
    # refactor silently dropping red from the iteration.
    squadron = _squadron(reserve=4, owned=10, pilots=8, pilot_limits=False)
    processor = _processor_split([], [squadron])
    processor.commit_intercept_losses(_debrief({str(squadron.id): 1}))
    assert squadron.owned_aircraft == 7
    assert len(squadron.available_pilots) == 5


def test_multiple_squadrons_mixed_outcomes() -> None:
    # One taking losses, one absent from the survivor map (no participation, no
    # loss), one fully surviving -- all in one commit.
    losing = _squadron(reserve=4, owned=10, pilots=8, pilot_limits=False)
    absent = _squadron(reserve=4, owned=10, pilots=8, pilot_limits=False)
    survived = _squadron(reserve=4, owned=10, pilots=8, pilot_limits=False)
    processor = _processor([losing, absent, survived])
    processor.commit_intercept_losses(
        _debrief({str(losing.id): 1, str(survived.id): 4})
    )
    assert losing.owned_aircraft == 7
    assert len(losing.available_pilots) == 5
    assert absent.owned_aircraft == 10
    assert len(absent.available_pilots) == 8
    assert survived.owned_aircraft == 10
    assert len(survived.available_pilots) == 8


def test_zero_reserve_squadron_skipped_even_if_in_survivors() -> None:
    # reserve 0 -> never fielded; a stale survivor entry must not touch it.
    squadron = _squadron(reserve=0, owned=10, pilots=8, pilot_limits=False)
    processor = _processor([squadron])
    processor.commit_intercept_losses(_debrief({str(squadron.id): 0}))
    assert squadron.owned_aircraft == 10
    assert len(squadron.available_pilots) == 8


def test_owned_zero_squadron_not_charged_even_if_in_survivors() -> None:
    # reserve 4 but nothing owned -> fields 0; a survivor entry is a no-op.
    squadron = _squadron(reserve=4, owned=0, pilots=8, pilot_limits=False)
    processor = _processor([squadron])
    processor.commit_intercept_losses(_debrief({str(squadron.id): 0}))
    assert squadron.owned_aircraft == 0
    assert len(squadron.available_pilots) == 8
