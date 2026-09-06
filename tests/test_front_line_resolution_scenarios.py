"""Scenario table for front-line resolution.

Read the CASES table for the full picture at a glance: each row is one
realistic front-line situation with its expected verdict. Covers the cases most
likely to occur in the wild plus the ones the old resolver got most wrong.

Outcome legend (by strength of ground exchanged):
  Strong Win / Win / Minor Win  -> allies advance (0.5 / 0.3 / 0.1 strength)
  Stalemate                     -> no movement
  Minor Loss / Loss / Strong Loss -> allies lose ground
"""

from __future__ import annotations

import pytest

from game.ground_forces.combat_stance import CombatStance
from game.sim.front_line_resolution import (
    DEFEAT_INFLUENCE,
    MINOR_INFLUENCE,
    STRONG_INFLUENCE,
    resolve_front_line,
)

# Short aliases keep the CASES rows compact and column-aligned.
DEF, AMB, AGG, ELIM, BT, RET = (
    CombatStance.DEFENSIVE,
    CombatStance.AMBUSH,
    CombatStance.AGGRESSIVE,
    CombatStance.ELIMINATION,
    CombatStance.BREAKTHROUGH,
    CombatStance.RETREAT,
)

# Verdict label -> (player_won, strength delta).
_LABEL = {
    "Strong Win": (True, STRONG_INFLUENCE),
    "Win": (True, DEFEAT_INFLUENCE),
    "Minor Win": (True, MINOR_INFLUENCE),
    "Stalemate": (True, 0.0),
    "Minor Loss": (False, MINOR_INFLUENCE),
    "Loss": (False, DEFEAT_INFLUENCE),
    "Strong Loss": (False, STRONG_INFLUENCE),
}

# Each row: (id, ally_alive, enemy_alive, ally_losses, enemy_losses,
#            player_stance, enemy_stance, expected_verdict)
CASES = [
    # --- Previously the MOST WRONG (these are the regressions) ---
    ("overwhelming_retreat", 30, 1, 0, 0, AGG, RET, "Strong Win"),
    ("overwhelming_breakthrough", 30, 1, 0, 0, BT, RET, "Strong Win"),
    ("rewarded_while_overrun", 2, 10, 0, 0, DEF, BT, "Loss"),
    ("advantaged_but_bled", 20, 10, 3, 0, AGG, DEF, "Stalemate"),
    # --- Common & important in the wild ---
    ("parity_dug_in_standoff", 10, 10, 0, 0, DEF, DEF, "Stalemate"),
    ("parity_push_vs_hold", 10, 10, 0, 0, AGG, DEF, "Stalemate"),
    ("advantage_2to1_agg", 20, 10, 0, 0, AGG, DEF, "Minor Win"),
    ("advantage_2to1_elim", 20, 10, 0, 0, ELIM, DEF, "Win"),
    ("parity_won_firefight", 10, 10, 0, 3, AGG, DEF, "Win"),
    ("parity_lost_firefight", 10, 10, 3, 0, AGG, DEF, "Minor Loss"),
    ("enemy_retreats_3to1", 30, 10, 0, 0, AGG, RET, "Win"),
    ("retreat_from_strength", 30, 10, 0, 0, RET, DEF, "Minor Loss"),
    ("retreat_while_outmatched", 10, 30, 0, 0, RET, AGG, "Strong Loss"),
    ("defensive_cap_5to1", 25, 5, 0, 0, DEF, RET, "Minor Win"),
    # --- Edges & special cases ---
    ("mutual_retreat", 30, 10, 0, 0, RET, RET, "Stalemate"),
    ("mutual_retreat_skirmish", 10, 10, 0, 3, RET, RET, "Minor Win"),
    ("enemy_annihilated", 10, 0, 0, 5, AGG, DEF, "Strong Win"),
    ("you_annihilated", 0, 10, 5, 0, AGG, DEF, "Strong Loss"),
    ("enemy_breakthrough_overrun", 10, 10, 0, 0, DEF, BT, "Minor Loss"),
    ("dug_in_with_casualties", 30, 1, 0, 3, DEF, DEF, "Minor Win"),
]

# Prose for each id, shown in the failure message so a failure reads like a bug
# report rather than a bare tuple mismatch.
_DESC = {
    "overwhelming_retreat": "30:1, enemy retreats, no contact (the reported bug)",
    "overwhelming_breakthrough": "30:1, you breakthrough vs a retreating enemy",
    "rewarded_while_overrun": "1:5 overrun while defending (was falsely a 'win')",
    "advantaged_but_bled": "2:1 & aggressive but you took all the losses",
    "parity_dug_in_standoff": "equal forces, both defending, nobody fights",
    "parity_push_vs_hold": "equal forces; you push (AGG), they hold (DEF)",
    "advantage_2to1_agg": "2:1 advantage, aggressive vs their defense",
    "advantage_2to1_elim": "2:1 advantage, committed to elimination",
    "parity_won_firefight": "equal forces; you bloodied them 0:3",
    "parity_lost_firefight": "equal forces; you bled 3:0",
    "enemy_retreats_3to1": "3:1 advantage; enemy retreats",
    "retreat_from_strength": "3:1 advantage but YOU order retreat",
    "retreat_while_outmatched": "1:3 outmatched and you retreat",
    "defensive_cap_5to1": "5:1 but defending caps the advance at minor",
    "mutual_retreat": "both sides withdraw, no contact",
    "mutual_retreat_skirmish": "both withdraw but you bloodied them",
    "enemy_annihilated": "enemy front-line force wiped out",
    "you_annihilated": "your front-line force wiped out",
    "enemy_breakthrough_overrun": "enemy breaks through your defense at parity",
    "dug_in_with_casualties": "30:1 both defending but you bloodied them 0:3",
}


@pytest.mark.parametrize(
    "case",
    CASES,
    ids=[c[0] for c in CASES],
)
def test_front_line_scenario(
    case: tuple[str, int, int, int, int, CombatStance, CombatStance, str],
) -> None:
    _id, ally, enemy, ally_cas, enemy_cas, p_stance, e_stance, expected = case
    outcome = resolve_front_line(ally, enemy, ally_cas, enemy_cas, p_stance, e_stance)
    assert (outcome.player_won, outcome.delta) == _LABEL[expected], (
        f"{_id}: {_DESC[_id]}\n"
        f"  inputs: ally={ally} enemy={enemy} losses={ally_cas}:{enemy_cas} "
        f"stances={p_stance.name}/{e_stance.name}\n"
        f"  expected {expected} {_LABEL[expected]}, "
        f"got player_won={outcome.player_won} delta={outcome.delta}"
    )
