from __future__ import annotations

from game.settings.settings import Settings


def test_motorpool_enabled_defaults_true() -> None:
    assert Settings().motorpool_enabled is True


def test_motorpool_spawn_cap_defaults_to_ten() -> None:
    assert Settings().motorpool_spawn_cap == 10


def test_motorpool_settings_are_user_visible() -> None:
    names = {
        name
        for page in Settings.pages()
        for section in Settings.sections(page)
        for name, _description in Settings.fields(page, section)
    }
    assert "motorpool_enabled" in names
    assert "motorpool_spawn_cap" in names
