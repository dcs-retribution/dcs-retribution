from unittest.mock import MagicMock
from uuid import uuid4

from game.ground_forces.combat_stance import CombatStance
from game.theater.controlpoint import Airfield, Player


def _bare_airfield() -> Airfield:
    # Bypass __init__ (which needs a real Airport/theater); these methods only
    # touch self.stances, so a constructed instance with a stances dict suffices.
    cp = Airfield.__new__(Airfield)
    cp.stances = {uuid4(): CombatStance.DEFENSIVE, uuid4(): CombatStance.RETREAT}
    return cp


def _mock_game(automate: bool, stance: CombatStance) -> MagicMock:
    game = MagicMock()
    game.settings.automate_front_line_stance = automate
    game.settings.default_front_line_stance = stance
    return game


def test_seed_front_line_stances_overwrites_every_entry() -> None:
    cp = _bare_airfield()
    cp.seed_front_line_stances(CombatStance.AGGRESSIVE)
    assert set(cp.stances.values()) == {CombatStance.AGGRESSIVE}


def test_capture_seeds_for_blue_with_auto_off() -> None:
    cp = _bare_airfield()
    game = _mock_game(automate=False, stance=CombatStance.AGGRESSIVE)
    cp.apply_default_stance_on_capture(game, Player.BLUE)
    assert set(cp.stances.values()) == {CombatStance.AGGRESSIVE}


def test_capture_does_not_seed_when_auto_on() -> None:
    cp = _bare_airfield()
    before = dict(cp.stances)
    game = _mock_game(automate=True, stance=CombatStance.AGGRESSIVE)
    cp.apply_default_stance_on_capture(game, Player.BLUE)
    assert cp.stances == before


def test_capture_does_not_seed_for_red() -> None:
    cp = _bare_airfield()
    before = dict(cp.stances)
    game = _mock_game(automate=False, stance=CombatStance.AGGRESSIVE)
    cp.apply_default_stance_on_capture(game, Player.RED)
    assert cp.stances == before
