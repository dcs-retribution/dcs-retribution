from unittest.mock import MagicMock

from game.ground_forces.combat_stance import CombatStance
from game.settings.settings import Settings
from game.theater.player import Player
from game.theater.start_generator import apply_default_player_stances


def _settings(auto: bool) -> Settings:
    settings = Settings()
    settings.automate_front_line_stance = auto
    return settings


def _cp(captured: Player) -> MagicMock:
    cp = MagicMock()
    cp.captured = captured
    return cp


def test_generation_seeds_player_points_when_auto_off() -> None:
    # Delegates coalition filtering to player_points() and seeds each result.
    blue = _cp(Player.BLUE)
    theater = MagicMock()
    theater.player_points.return_value = [blue]

    apply_default_player_stances(theater, _settings(auto=False))

    theater.player_points.assert_called_once()
    blue.seed_front_line_stances.assert_called_once_with(CombatStance.AGGRESSIVE)


def test_generation_seeds_nothing_when_auto_on() -> None:
    blue = _cp(Player.BLUE)
    theater = MagicMock()
    theater.player_points.return_value = [blue]

    apply_default_player_stances(theater, _settings(auto=True))

    blue.seed_front_line_stances.assert_not_called()
