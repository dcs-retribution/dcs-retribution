from game.ground_forces.combat_stance import CombatStance
from game.settings.optiondescription import SETTING_DESCRIPTION_KEY
from game.settings.settings import Settings


def test_default_front_line_stance_defaults_to_aggressive() -> None:
    assert Settings().default_front_line_stance is CombatStance.AGGRESSIVE


def test_default_front_line_stance_choices_exclude_retreat() -> None:
    # The option's choices are what the settings window offers; RETREAT is not a
    # sensible standing default and must not be selectable.
    field = Settings.__dataclass_fields__["default_front_line_stance"]
    description = field.metadata[SETTING_DESCRIPTION_KEY]
    values = set(description.choices.values())
    assert CombatStance.RETREAT not in values
    assert values == {
        CombatStance.AGGRESSIVE,
        CombatStance.DEFENSIVE,
        CombatStance.AMBUSH,
        CombatStance.ELIMINATION,
        CombatStance.BREAKTHROUGH,
    }


def test_default_front_line_stance_is_user_visible() -> None:
    names = {
        name
        for page in Settings.pages()
        for section in Settings.sections(page)
        for name, _description in Settings.fields(page, section)
    }
    assert "default_front_line_stance" in names


def test_default_front_line_stance_backfills_on_old_save() -> None:
    # An old save lacks the field entirely; __setstate__ overlays saved state on a
    # fresh Settings(), so the field must resolve to the AGGRESSIVE default.
    settings = Settings.__new__(Settings)
    settings.__setstate__({})
    assert settings.default_front_line_stance is CombatStance.AGGRESSIVE


def test_default_front_line_stance_enum_round_trips() -> None:
    out = Settings.deserialize_state_dict(
        {"default_front_line_stance": "CombatStance.BREAKTHROUGH"}
    )
    assert out["default_front_line_stance"] is CombatStance.BREAKTHROUGH


def test_default_front_line_stance_stale_value_falls_back() -> None:
    out = Settings.deserialize_state_dict({"default_front_line_stance": "nonsense"})
    assert out["default_front_line_stance"] is CombatStance.AGGRESSIVE


def test_default_front_line_stance_corrupt_value_falls_back() -> None:
    # Empty/truncated saved strings raise SyntaxError in eval; must fall back,
    # not crash campaign load.
    out = Settings.deserialize_state_dict({"default_front_line_stance": ""})
    assert out["default_front_line_stance"] is CombatStance.AGGRESSIVE


def test_default_front_line_stance_non_enum_value_falls_back() -> None:
    # A saved string that evals to a non-member (e.g. a bare int) raises no
    # exception; it must still fall back to the default, not store a bad type.
    out = Settings.deserialize_state_dict({"default_front_line_stance": "42"})
    assert out["default_front_line_stance"] is CombatStance.AGGRESSIVE
