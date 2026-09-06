"""Shared pytest fixtures for the whole suite.

Loading aircraft via ``AircraftType.iter_all()`` / ``priority_list_for_task()``
(and therefore the squadron/aircraft tests) reaches ``_user_weapon_injections()``,
which asserts ``persistency._dcs_saved_game_folder`` is set. Point it at a temp
dir for the test session so those lookups don't abort without a real DCS install.
"""

import pytest

import game.persistency as persistency


@pytest.fixture(autouse=True, scope="session")
def stub_dcs_saved_game_folder(tmp_path_factory: pytest.TempPathFactory) -> None:
    """Point persistency at a temp dir so weapon-injection lookups don't abort."""
    tmp = tmp_path_factory.mktemp("dcs_saved_game")
    persistency._dcs_saved_game_folder = str(tmp)
