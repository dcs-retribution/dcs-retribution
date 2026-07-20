"""Regression tests for front-line battle scoring around base capture.

Background (the bug these pin): a front-line unit's death is attributed to its
origin control point by ``Debriefing.casualty_count`` with no check of which
side the unit was on. A base's defenders have ``origin`` == that base. If a base
is captured *before* the front-line win/loss is scored, those dead enemy
defenders get counted as the new owner's (allied) casualties on the front line
leading out of the just-captured base -- producing a phantom "massive losses /
defeat" at a base the player actually took. Scoring must therefore run before
ownership flips.
"""

import inspect
from types import SimpleNamespace
from typing import Any, Callable, cast
from unittest.mock import MagicMock

from game.debriefing import Debriefing, GroundLosses
from game.sim.missionresultsprocessor import MissionResultsProcessor
from game.theater import ControlPoint

#: The complete set of sub-steps ``MissionResultsProcessor.commit`` invokes, in
#: no particular order. ``_record_steps`` stubs *every* processor method, so this
#: set is checked exactly: adding or removing a commit sub-step without updating
#: this list fails ``test_battle_impact_scored_before_captures_flip_ownership``.
COMMIT_STEPS = [
    "commit_air_losses",
    "commit_pilot_experience",
    "commit_front_line_losses",
    "commit_motorpool_losses",
    "commit_convoy_losses",
    "commit_cargo_ship_losses",
    "commit_airlift_losses",
    "commit_ground_losses",
    "commit_damaged_runways",
    "commit_captures",
    "commit_front_line_battle_impact",
    "record_carcasses",
]


def _record_steps(processor: MissionResultsProcessor, calls: list[str]) -> None:
    """Replace every processor method (except ``commit``) with a stub that
    records when it ran.

    Stubbing the full method set -- rather than only ``COMMIT_STEPS`` -- means a
    newly added sub-step is still recorded, so ``set(calls) == COMMIT_STEPS``
    fails until ``COMMIT_STEPS`` is updated to match ``commit``.
    """

    def recorder(name: str) -> Callable[..., None]:
        def _inner(*args: Any, **kwargs: Any) -> None:
            calls.append(name)

        return _inner

    for name, _ in inspect.getmembers(type(processor), inspect.isfunction):
        if name == "commit" or name.startswith("__"):
            continue
        setattr(processor, name, recorder(name))


def test_casualty_count_is_side_agnostic() -> None:
    """casualty_count matches on origin CP only -- it does not check side.

    This is *why* scoring must precede captures: after a base flips owner, its
    enemy defenders' deaths (origin == that base) would be miscounted for the
    new owner.
    """
    cp = cast(ControlPoint, MagicMock())
    other = cast(ControlPoint, MagicMock())
    debriefing = Debriefing.__new__(Debriefing)
    debriefing.ground_losses = GroundLosses(
        player_front_line=[cast(Any, SimpleNamespace(origin=cp))],
        enemy_front_line=[
            cast(Any, SimpleNamespace(origin=cp)),
            cast(Any, SimpleNamespace(origin=other)),
        ],
    )

    # Both the allied unit and the enemy defender whose origin is `cp` count.
    assert debriefing.casualty_count(cp) == 2
    assert debriefing.casualty_count(other) == 1


def test_battle_impact_scored_before_captures_flip_ownership() -> None:
    """commit() must score the front line before flipping captured bases.

    Running commit_captures first would relabel a captured base as friendly, so
    its dead defenders would be tallied as allied casualties (see
    test_casualty_count_is_side_agnostic), inverting a victory into a defeat.
    """
    processor = MissionResultsProcessor(cast(Any, MagicMock()))
    calls: list[str] = []
    _record_steps(processor, calls)

    processor.commit(cast(Any, MagicMock()), cast(Any, MagicMock()))

    assert set(calls) == set(COMMIT_STEPS), "every commit sub-step should run"
    assert calls.index("commit_front_line_battle_impact") < calls.index(
        "commit_captures"
    ), "front-line scoring must run before bases are captured"
