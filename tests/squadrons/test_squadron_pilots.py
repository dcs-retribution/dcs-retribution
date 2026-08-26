from __future__ import annotations

from types import SimpleNamespace
from typing import cast

from game.settings import Settings
from game.squadrons.pilot import Pilot, PilotStatus
from game.squadrons.squadron import Squadron


def _squadron(available: list[Pilot], invulnerable_players: bool = False) -> Squadron:
    squadron = Squadron.__new__(Squadron)
    squadron.available_pilots = available
    squadron.settings = cast(
        Settings, SimpleNamespace(invulnerable_player_pilots=invulnerable_players)
    )
    return squadron


def _dead(pilots: list[Pilot]) -> int:
    return sum(p.status is PilotStatus.Dead for p in pilots)


def test_lose_pilots_kills_the_requested_count() -> None:
    pilots = [Pilot(f"AI {i}") for i in range(4)]
    _squadron(list(pilots)).lose_pilots(2)
    assert _dead(pilots) == 2


def test_lose_pilots_only_touches_untasked_pilots() -> None:
    # A pilot tasked to another flight has been claimed (removed from
    # available_pilots) and must not be killed by a QRA loss.
    tasked = Pilot("Tasked")
    idle = Pilot("Idle")
    _squadron([idle]).lose_pilots(2)
    assert idle.status is PilotStatus.Dead
    assert tasked.status is PilotStatus.Active


def test_lose_pilots_prefers_ai_over_players() -> None:
    player = Pilot("Ace", player=True)
    ai = Pilot("Wingman", player=False)
    _squadron([player, ai]).lose_pilots(1)
    assert ai.status is PilotStatus.Dead
    assert player.status is PilotStatus.Active


def test_lose_pilots_spares_players_when_invulnerable() -> None:
    player = Pilot("Ace", player=True)
    _squadron([player], invulnerable_players=True).lose_pilots(1)
    assert player.status is PilotStatus.Active


def test_lose_pilots_kills_players_when_no_ai_and_vulnerable() -> None:
    player = Pilot("Ace", player=True)
    _squadron([player]).lose_pilots(1)
    assert player.status is PilotStatus.Dead


def test_lose_pilots_removes_dead_pilots_from_available() -> None:
    pilots = [Pilot("AI 1"), Pilot("AI 2")]
    squadron = _squadron(pilots)
    squadron.lose_pilots(1)
    assert len(squadron.available_pilots) == 1
    assert squadron.available_pilots[0].name == "AI 2"


def test_lose_pilots_caps_at_available_pilots() -> None:
    pilots = [Pilot("AI 1"), Pilot("AI 2")]
    _squadron(list(pilots)).lose_pilots(5)
    assert _dead(pilots) == 2
