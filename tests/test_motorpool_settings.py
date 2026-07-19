from __future__ import annotations

from game.settings.boundedintoption import BoundedIntOption
from game.settings.optiondescription import SETTING_DESCRIPTION_KEY
from game.settings.settings import Settings


def test_motorpool_enabled_defaults_true() -> None:
    assert Settings().motorpool_enabled is True


def test_motorpool_spawn_cap_defaults_to_ten() -> None:
    assert Settings().motorpool_spawn_cap == 10


def test_motorpool_spawn_cap_spinner_is_capped_at_twenty_five() -> None:
    # druss: 25 is a hard ceiling — the spinner must not allow more.
    field_info = Settings.__dataclass_fields__["motorpool_spawn_cap"]
    option = field_info.metadata[SETTING_DESCRIPTION_KEY]
    assert isinstance(option, BoundedIntOption)
    assert option.max == 25


def test_motorpool_settings_are_user_visible() -> None:
    names = {
        name
        for page in Settings.pages()
        for section in Settings.sections(page)
        for name, _description in Settings.fields(page, section)
    }
    assert "motorpool_enabled" in names
    assert "motorpool_spawn_cap" in names
