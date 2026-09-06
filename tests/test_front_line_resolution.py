"""Unit tests for the front-line resolution model.

Each test pins one behavior of resolve_front_line. Outcomes are asserted as
(player_won, delta); delta is an influence magnitude tier or 0.0 (stalemate).
"""

from __future__ import annotations

import pytest

from game.ground_forces.combat_stance import CombatStance
from game.sim.front_line_resolution import (
    DEFEAT_INFLUENCE,
    MINOR_INFLUENCE,
    STRONG_INFLUENCE,
    FrontLineOutcome,
    battle_score,
    force_score,
    posture_score,
    resolve_front_line,
)

DEF = CombatStance.DEFENSIVE
AMB = CombatStance.AMBUSH
AGG = CombatStance.AGGRESSIVE
ELIM = CombatStance.ELIMINATION
BT = CombatStance.BREAKTHROUGH
RET = CombatStance.RETREAT


def _won_delta(outcome: FrontLineOutcome) -> tuple[bool, float]:
    return outcome.player_won, outcome.delta


# --- score helpers ---


def test_force_score_saturates_and_is_symmetric() -> None:
    assert force_score(10, 10) == pytest.approx(0.0)
    assert force_score(40, 10) == pytest.approx(1.0)  # 4:1 saturates at +1
    assert force_score(10, 40) == pytest.approx(-1.0)  # 1:4 saturates at -1
    assert force_score(0, 10) == -1.0  # allied force wiped
    assert force_score(10, 0) == 1.0  # enemy force wiped


def test_posture_score_uses_stance_weights() -> None:
    assert posture_score(DEF, DEF) == pytest.approx(0.0)
    assert posture_score(BT, RET) == pytest.approx(1.0)  # (1 - (-1)) / 2
    assert posture_score(RET, BT) == pytest.approx(-1.0)
    assert posture_score(AGG, DEF) == pytest.approx(0.25)


def test_battle_score_is_casualty_differential() -> None:
    assert battle_score(0, 0) == pytest.approx(0.0)
    assert battle_score(0, 3) == pytest.approx(1.0)  # enemy bloodied hard
    assert battle_score(3, 0) == pytest.approx(-1.0)
    assert battle_score(2, 2) == pytest.approx(0.0)  # even grind


# --- resolve_front_line behaviors ---


def test_reported_case_overwhelming_force_advances() -> None:
    # 30:1, aggressive, enemy retreating, zero casualties -> strong win.
    assert _won_delta(resolve_front_line(30, 1, 0, 0, AGG, RET)) == (
        True,
        STRONG_INFLUENCE,
    )


def test_mutual_dug_in_no_losses_is_stalemate() -> None:
    assert _won_delta(resolve_front_line(30, 1, 0, 0, DEF, DEF)) == (True, 0.0)
    assert _won_delta(resolve_front_line(10, 10, 0, 0, AMB, DEF)) == (True, 0.0)


def test_mutual_retreat_no_losses_is_stalemate() -> None:
    assert _won_delta(resolve_front_line(30, 1, 0, 0, RET, RET)) == (True, 0.0)


def test_mutual_retreat_resolves_on_casualties_only() -> None:
    # 0:3 -> minor win (capped); 5:6 -> minor win (just above threshold).
    assert _won_delta(resolve_front_line(10, 10, 0, 3, RET, RET)) == (
        True,
        MINOR_INFLUENCE,
    )
    assert _won_delta(resolve_front_line(10, 10, 5, 6, RET, RET)) == (
        True,
        MINOR_INFLUENCE,
    )
    # 3:0 -> minor loss.
    assert _won_delta(resolve_front_line(10, 10, 3, 0, RET, RET)) == (
        False,
        MINOR_INFLUENCE,
    )


def test_mutual_dug_in_with_casualties_resolves() -> None:
    # 30:1 both defensive, enemy bloodied 0:3 -> minor win (defensive cap).
    assert _won_delta(resolve_front_line(30, 1, 0, 3, DEF, DEF)) == (
        True,
        MINOR_INFLUENCE,
    )


def test_parity_passive_is_stalemate() -> None:
    assert _won_delta(resolve_front_line(10, 10, 0, 0, DEF, DEF)) == (True, 0.0)


def test_parity_aggressive_vs_defensive_is_stalemate() -> None:
    # net = 0.075, just under the 0.08 stalemate threshold.
    assert _won_delta(resolve_front_line(10, 10, 0, 0, AGG, DEF)) == (True, 0.0)


def test_parity_elimination_vs_defensive_is_minor_win() -> None:
    assert _won_delta(resolve_front_line(10, 10, 0, 0, ELIM, DEF)) == (
        True,
        MINOR_INFLUENCE,
    )


def test_taking_more_losses_than_enemy_is_a_defeat() -> None:
    assert _won_delta(resolve_front_line(10, 10, 3, 0, AGG, DEF)) == (
        False,
        MINOR_INFLUENCE,
    )


def test_player_retreat_scales_with_force_ratio() -> None:
    assert _won_delta(resolve_front_line(2, 10, 0, 0, RET, DEF)) == (
        False,
        STRONG_INFLUENCE,
    )
    assert _won_delta(resolve_front_line(10, 10, 0, 0, RET, DEF)) == (
        False,
        DEFEAT_INFLUENCE,
    )
    assert _won_delta(resolve_front_line(30, 10, 0, 0, RET, DEF)) == (
        False,
        MINOR_INFLUENCE,
    )


def test_annihilation_is_unconditional() -> None:
    assert _won_delta(resolve_front_line(0, 10, 0, 0, AGG, DEF)) == (
        False,
        STRONG_INFLUENCE,
    )
    assert _won_delta(resolve_front_line(10, 0, 0, 0, DEF, AGG)) == (
        True,
        STRONG_INFLUENCE,
    )


def test_enemy_breakthrough_vs_defense_at_parity_loses_ground() -> None:
    # A determined push overruns a dug-in defense at parity.
    assert _won_delta(resolve_front_line(10, 10, 0, 0, DEF, BT)) == (
        False,
        MINOR_INFLUENCE,
    )


def test_defensive_stance_caps_advance_at_minor() -> None:
    # 30:1 defensive vs retreating enemy -> would be a win, capped to minor.
    assert _won_delta(resolve_front_line(30, 1, 0, 0, DEF, RET)) == (
        True,
        MINOR_INFLUENCE,
    )


def test_stance_ordering_is_monotonic() -> None:
    # For a fixed scenario, a more aggressive OWNFOR stance is never worse.
    ranks: dict[tuple[bool, float], int] = {
        (False, STRONG_INFLUENCE): -3,
        (False, DEFEAT_INFLUENCE): -2,
        (False, MINOR_INFLUENCE): -1,
        (True, 0.0): 0,
        (True, MINOR_INFLUENCE): 1,
        (True, DEFEAT_INFLUENCE): 2,
        (True, STRONG_INFLUENCE): 3,
    }
    prev: int | None = None
    for stance in (RET, DEF, AMB, AGG, ELIM, BT):
        outcome = resolve_front_line(30, 10, 0, 0, stance, RET)
        rank = ranks[_won_delta(outcome)]
        assert (
            prev is None or rank >= prev
        ), f"{stance} ({rank}) worse than previous ({prev})"
        prev = rank
