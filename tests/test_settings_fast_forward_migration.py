"""Save-compat migration for the pre-#684 fast-forward settings.

#684 replaced ``fast_forward_to_first_contact`` / ``player_mission_interrupts_sim_at``
/ ``auto_resolve_combat`` with the ``FastForwardStopCondition`` and
``CombatResolutionMethod`` enums. Loading an older save (or one holding the
legacy ``None``/``"none"`` "Never" sentinel) must not crash.
"""

from typing import Any

from game.ato.starttype import StartType
from game.settings.settings import (
    CombatResolutionMethod,
    FastForwardStopCondition,
    Settings,
)


def _deserialized(state: dict[str, Any]) -> dict[str, Any]:
    return Settings.deserialize_state_dict(dict(state))


def test_string_none_stop_condition_maps_to_disabled() -> None:
    out = _deserialized({"fast_forward_stop_condition": "none"})
    assert out["fast_forward_stop_condition"] is FastForwardStopCondition.DISABLED


def test_python_none_stop_condition_maps_to_disabled() -> None:
    out = _deserialized({"fast_forward_stop_condition": None})
    assert out["fast_forward_stop_condition"] is FastForwardStopCondition.DISABLED


def test_string_never_stop_condition_maps_to_disabled() -> None:
    out = _deserialized({"fast_forward_stop_condition": "Never"})
    assert out["fast_forward_stop_condition"] is FastForwardStopCondition.DISABLED


def test_valid_stop_condition_is_preserved() -> None:
    out = _deserialized(
        {"fast_forward_stop_condition": "FastForwardStopCondition.PLAYER_TAXI"}
    )
    assert out["fast_forward_stop_condition"] is FastForwardStopCondition.PLAYER_TAXI


def test_legacy_fields_disabled_maps_to_disabled() -> None:
    out = _deserialized(
        {
            "fast_forward_to_first_contact": False,
            "player_mission_interrupts_sim_at": StartType.COLD,
        }
    )
    assert out["fast_forward_stop_condition"] is FastForwardStopCondition.DISABLED
    # Legacy keys are consumed, not left as junk attributes.
    assert "fast_forward_to_first_contact" not in out
    assert "player_mission_interrupts_sim_at" not in out


def test_legacy_enabled_at_startup_maps_to_player_startup() -> None:
    out = _deserialized(
        {
            "fast_forward_to_first_contact": True,
            "player_mission_interrupts_sim_at": StartType.COLD,
        }
    )
    assert out["fast_forward_stop_condition"] is FastForwardStopCondition.PLAYER_STARTUP


def test_legacy_enabled_at_taxi_maps_to_player_taxi() -> None:
    out = _deserialized(
        {
            "fast_forward_to_first_contact": True,
            "player_mission_interrupts_sim_at": StartType.WARM,
        }
    )
    assert out["fast_forward_stop_condition"] is FastForwardStopCondition.PLAYER_TAXI


def test_legacy_enabled_at_takeoff_maps_to_player_takeoff() -> None:
    out = _deserialized(
        {
            "fast_forward_to_first_contact": True,
            "player_mission_interrupts_sim_at": StartType.RUNWAY,
        }
    )
    assert out["fast_forward_stop_condition"] is FastForwardStopCondition.PLAYER_TAKEOFF


def test_legacy_enabled_never_interrupt_maps_to_first_contact() -> None:
    out = _deserialized(
        {
            "fast_forward_to_first_contact": True,
            "player_mission_interrupts_sim_at": None,
        }
    )
    assert out["fast_forward_stop_condition"] is FastForwardStopCondition.FIRST_CONTACT


def test_legacy_start_type_stored_as_string_is_resolved() -> None:
    out = _deserialized(
        {
            "fast_forward_to_first_contact": True,
            "player_mission_interrupts_sim_at": "StartType.WARM",
        }
    )
    assert out["fast_forward_stop_condition"] is FastForwardStopCondition.PLAYER_TAXI


def test_legacy_auto_resolve_combat_maps_to_resolve() -> None:
    out = _deserialized({"auto_resolve_combat": True})
    assert out["combat_resolution_method"] is CombatResolutionMethod.RESOLVE
    assert "auto_resolve_combat" not in out


def test_legacy_auto_resolve_combat_off_maps_to_pause() -> None:
    out = _deserialized({"auto_resolve_combat": False})
    assert out["combat_resolution_method"] is CombatResolutionMethod.PAUSE


def test_setstate_yields_a_valid_member_for_legacy_none() -> None:
    # __setstate__ is the real load path; the field must end as a usable member.
    settings = Settings.__new__(Settings)
    settings.__setstate__({"fast_forward_stop_condition": "none"})
    assert isinstance(settings.fast_forward_stop_condition, FastForwardStopCondition)
    assert settings.fast_forward_stop_condition is FastForwardStopCondition.DISABLED


def test_python_none_combat_method_falls_back_to_default() -> None:
    out = _deserialized({"combat_resolution_method": None})
    assert out["combat_resolution_method"] is CombatResolutionMethod.PAUSE


def test_string_none_combat_method_falls_back_to_default() -> None:
    out = _deserialized({"combat_resolution_method": "none"})
    assert out["combat_resolution_method"] is CombatResolutionMethod.PAUSE


def test_legacy_bool_combat_method_falls_back_to_default() -> None:
    # A leftover bool from the pre-#684 auto_resolve_combat field stored under
    # the new key is not a member -> field default.
    out = _deserialized({"combat_resolution_method": True})
    assert out["combat_resolution_method"] is CombatResolutionMethod.PAUSE


def test_valid_combat_method_is_preserved() -> None:
    out = _deserialized({"combat_resolution_method": "CombatResolutionMethod.SKIP"})
    assert out["combat_resolution_method"] is CombatResolutionMethod.SKIP


def test_json_encoded_enum_is_restored() -> None:
    out = _deserialized(
        {"fast_forward_stop_condition": {"Enum": "FastForwardStopCondition.MANUAL"}}
    )
    assert out["fast_forward_stop_condition"] is FastForwardStopCondition.MANUAL


def test_json_encoded_stale_enum_falls_back_to_default() -> None:
    out = _deserialized(
        {"fast_forward_stop_condition": {"Enum": "FastForwardStopCondition.NEVER"}}
    )
    assert out["fast_forward_stop_condition"] is FastForwardStopCondition.PLAYER_STARTUP


def test_already_resolved_enum_member_is_kept() -> None:
    out = _deserialized({"combat_resolution_method": CombatResolutionMethod.RESOLVE})
    assert out["combat_resolution_method"] is CombatResolutionMethod.RESOLVE
