"""Front-line victory/loss resolution.

Pure, stateless model that turns a front line's force ratio, both sides'
stances, and the round's casualties into a strength-delta verdict. Extracted
from MissionResultsProcessor.commit_front_line_battle_impact so the decision
logic is unit-testable in isolation.

Design: docs/superpowers/front-line-victory/design_spec.md
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from game.ground_forces.combat_stance import CombatStance

# Influence magnitude tiers (match the historical missionresultsprocessor values).
STRONG_INFLUENCE = 0.5
DEFEAT_INFLUENCE = 0.3
MINOR_INFLUENCE = 0.1

# --- tunable constants ---
STRONG_RATIO = 4.0  # force ratio at which force_score saturates to +/-1
STALEMATE_THRESHOLD = 0.08  # |net| below this -> no movement
WEIGHT_FORCE = 0.40
WEIGHT_POSTURE = 0.30
WEIGHT_BATTLE = 0.30

STANCE_WEIGHT: dict[CombatStance, float] = {
    CombatStance.BREAKTHROUGH: 1.0,
    CombatStance.ELIMINATION: 0.75,
    CombatStance.AGGRESSIVE: 0.5,
    CombatStance.DEFENSIVE: 0.0,
    CombatStance.AMBUSH: 0.0,
    CombatStance.RETREAT: -1.0,
}
_PASSIVE_STANCES: tuple[CombatStance, ...] = (
    CombatStance.DEFENSIVE,
    CombatStance.AMBUSH,
)


@dataclass(frozen=True)
class FrontLineOutcome:
    """The verdict for one front line this turn.

    player_won: True if the allied force advances, False if it loses ground.
    delta:      magnitude tier applied via Base.affect_strength (0.0 = stalemate).
    summary:    short reason, folded into the player-facing report message.
    """

    player_won: bool
    delta: float
    summary: str


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def force_score(ally_alive: int, enemy_alive: int) -> float:
    if ally_alive <= 0:
        return -1.0
    if enemy_alive <= 0:
        return 1.0
    return _clamp(
        math.log2(ally_alive / enemy_alive) / math.log2(STRONG_RATIO), -1.0, 1.0
    )


def posture_score(player_stance: CombatStance, enemy_stance: CombatStance) -> float:
    return _clamp(
        (STANCE_WEIGHT[player_stance] - STANCE_WEIGHT[enemy_stance]) / 2.0, -1.0, 1.0
    )


def battle_score(ally_casualties: int, enemy_casualties: int) -> float:
    return _clamp(
        math.log2((1.0 + enemy_casualties) / (1.0 + ally_casualties))
        / math.log2(STRONG_RATIO),
        -1.0,
        1.0,
    )


def _tier(score: float) -> tuple[bool, float]:
    """Map a signed score in [-1, 1] to (player_won, magnitude)."""
    if abs(score) < STALEMATE_THRESHOLD:
        return True, 0.0
    if score > 0:
        magnitude = (
            STRONG_INFLUENCE
            if score >= 0.6
            else DEFEAT_INFLUENCE if score >= 0.3 else MINOR_INFLUENCE
        )
        return True, magnitude
    magnitude = (
        STRONG_INFLUENCE
        if score <= -0.6
        else DEFEAT_INFLUENCE if score <= -0.3 else MINOR_INFLUENCE
    )
    return False, magnitude


def resolve_front_line(
    ally_alive: int,
    enemy_alive: int,
    ally_casualties: int,
    enemy_casualties: int,
    player_stance: CombatStance,
    enemy_stance: CombatStance,
) -> FrontLineOutcome:
    # 1. Annihilation: a non-existent force can't hold ground.
    if ally_alive <= 0:
        return FrontLineOutcome(False, STRONG_INFLUENCE, "Allied force destroyed")
    if enemy_alive <= 0:
        return FrontLineOutcome(True, STRONG_INFLUENCE, "Enemy force destroyed")

    # 2. Mutual withdrawal: both sides retreating -> only rearguard skirmishing
    #    (raw battle_score; force/posture moot). Capped at minor.
    if player_stance == CombatStance.RETREAT and enemy_stance == CombatStance.RETREAT:
        bs = battle_score(ally_casualties, enemy_casualties)
        if abs(bs) < STALEMATE_THRESHOLD:
            return FrontLineOutcome(True, 0.0, "Both sides withdrew")
        return FrontLineOutcome(bs > 0, MINOR_INFLUENCE, "Mutual withdrawal skirmish")

    # 3. Player retreat order (enemy not retreating): respect the command.
    if player_stance == CombatStance.RETREAT:
        fs = force_score(ally_alive, enemy_alive)
        if fs <= -0.3:
            return FrontLineOutcome(
                False, STRONG_INFLUENCE, "Retreated while outmatched"
            )
        if fs <= 0.1:
            return FrontLineOutcome(False, DEFEAT_INFLUENCE, "Retreated")
        return FrontLineOutcome(False, MINOR_INFLUENCE, "Fighting withdrawal")

    # 4. Mutual dug-in standoff, no casualties: a defensive line holds.
    if (
        player_stance in _PASSIVE_STANCES
        and enemy_stance in _PASSIVE_STANCES
        and ally_casualties == 0
        and enemy_casualties == 0
    ):
        return FrontLineOutcome(True, 0.0, "Both sides held their lines")

    # 5. General net-pressure model.
    net = _clamp(
        WEIGHT_FORCE * force_score(ally_alive, enemy_alive)
        + WEIGHT_POSTURE * posture_score(player_stance, enemy_stance)
        + WEIGHT_BATTLE * battle_score(ally_casualties, enemy_casualties),
        -1.0,
        1.0,
    )
    won, magnitude = _tier(net)
    # Defensive cap: a dug-in force doesn't pursue, so cap any advance at minor.
    if won and magnitude > 0.0 and player_stance in _PASSIVE_STANCES:
        magnitude = MINOR_INFLUENCE

    if magnitude == 0.0:
        return FrontLineOutcome(True, 0.0, "Neither side gained ground")
    if won:
        return FrontLineOutcome(True, magnitude, "Allied forces advancing")
    return FrontLineOutcome(False, magnitude, "Allied forces falling back")
