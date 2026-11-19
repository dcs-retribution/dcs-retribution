import json
from pathlib import Path

from game.plugins.luaplugin import LuaPluginDefinition


def test_mooseautolase_defines_six_tier_spinboxes() -> None:
    definition = LuaPluginDefinition.from_json(
        "MooseAutolase", Path("resources/plugins/MooseAutolase/plugin.json")
    )
    by_id = {opt.identifier: opt for opt in definition.options}
    expected = {
        "MooseAutolase.TierSamThreats": 1,
        "MooseAutolase.TierGuidedAaa": 2,
        "MooseAutolase.TierArtillery": 3,
        "MooseAutolase.TierUnguidedAaa": 3,
        "MooseAutolase.TierArmorLaunchers": 4,
        "MooseAutolase.TierOther": 5,
    }
    for identifier, default in expected.items():
        assert identifier in by_id, f"missing {identifier}"
        opt = by_id[identifier]
        assert opt.get_value == default
        assert opt.min == 0
        assert opt.max == 6


def test_mooseautolase_has_global_jtac_options_not_per_jtac() -> None:
    data = json.loads(
        Path("resources/plugins/MooseAutolase/plugin.json").read_text(encoding="utf-8")
    )
    mnemonics = {o["mnemonic"] for o in data["specificOptions"]}
    assert {"JtacSmoke", "JtacsPerFrontline", "JtacRadiusNM"} <= mnemonics
    assert "JtacTargetsMax" not in mnemonics
    assert not any(
        m.startswith("JtacAlpha") or m.startswith("JtacBravo") for m in mnemonics
    )


def test_jtacs_per_frontline_consumer_key_matches_registered_identifier() -> None:
    # The mission generators look up the option by literal key; a casing mismatch
    # makes settings.plugins.get() miss and every front line silently falls back to
    # a single JTAC. Guard the consumer constant against the registered identifier.
    from game.missiongenerator.flotgenerator import JTACS_PER_FRONTLINE_OPTION

    definition = LuaPluginDefinition.from_json(
        "MooseAutolase", Path("resources/plugins/MooseAutolase/plugin.json")
    )
    registered = {opt.identifier for opt in definition.options}
    assert JTACS_PER_FRONTLINE_OPTION in registered


def test_mooseautolase_jtacs_per_frontline_option() -> None:
    definition = LuaPluginDefinition.from_json(
        "MooseAutolase", Path("resources/plugins/MooseAutolase/plugin.json")
    )
    by_id = {opt.identifier: opt for opt in definition.options}
    opt = by_id["MooseAutolase.JtacsPerFrontline"]
    assert opt.get_value == 1
    assert opt.min == 1
    assert opt.max == 4
