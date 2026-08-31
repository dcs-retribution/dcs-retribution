"""Campaign-pinned squadron DCS country (#627 surfacing).

Under a CJTF faction an airframe-name squadron pick is a random.choice across
every nation's presets, so a USAF-named F-16 squadron can roll an
Israeli-countried preset and fly with the wrong comms voice and pilot names
(found in a flown CJTF campaign). A campaign squadron config may now pin
``country:``: the pick
only accepts same-nation presets (falling through to the def generator
otherwise), and ``override_squadron_defaults`` stamps the pinned nation either
way. An unknown country name is an authoring error that aborts New Game.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, Optional, cast

import pytest
from dcs.countries import (
    Greece,
    USA,
)

from game.campaignloader.campaignairwingconfig import SquadronConfig
from game.campaignloader.defaultsquadronassigner import (
    DefaultSquadronAssigner,
    resolve_config_country,
)


def _config(country: Optional[str]) -> SquadronConfig:
    data: dict[str, Any] = {"primary": "BARCAP"}
    if country is not None:
        data["country"] = country
    return SquadronConfig.from_data(data)


def _squadron_def(country_id: int, name: str = "Preset") -> Any:
    return SimpleNamespace(
        name=name,
        nickname=None,
        country=SimpleNamespace(id=country_id),
        claimed=False,
        operates_from=lambda cp: True,
        capable_of=lambda task: True,
        livery="livery",
        livery_set=[],
    )


def _assigner(defs: dict[Any, list[Any]]) -> DefaultSquadronAssigner:
    assigner = DefaultSquadronAssigner.__new__(DefaultSquadronAssigner)
    assigner.air_wing = cast(Any, SimpleNamespace(squadron_defs=defs))
    return assigner


def test_config_parses_country() -> None:
    assert _config("USA").country == "USA"
    assert _config(None).country is None


def test_resolve_config_country() -> None:
    resolved = resolve_config_country(_config("USA"))
    assert resolved is not None and resolved.id == USA.id
    assert resolve_config_country(_config(None)) is None
    # An unknown country name is an authoring error: abort New Game loudly.
    with pytest.raises(ValueError):
        resolve_config_country(_config("Atlantis"))


def test_airframe_pick_prefers_pinned_nation() -> None:
    us = _squadron_def(USA.id, "US preset")
    greek = _squadron_def(Greece.id, "Greek preset")
    assigner = _assigner({"F-16": [greek, us]})
    pinned = cast(Any, SimpleNamespace(id=USA.id))
    # random.choice over a country-filtered pool: with one match the pick is
    # deterministic no matter the seed.
    for _ in range(10):
        picked = assigner.find_squadron_for_airframe(
            cast(Any, "F-16"), cast(Any, None), cast(Any, None), pinned
        )
        assert picked is us


def test_airframe_pick_without_pin_is_unchanged() -> None:
    greek = _squadron_def(Greece.id)
    assigner = _assigner({"F-16": [greek]})
    picked = assigner.find_squadron_for_airframe(
        cast(Any, "F-16"), cast(Any, None), cast(Any, None)
    )
    assert picked is greek


def test_airframe_pick_with_no_matching_nation_returns_none() -> None:
    # No same-nation preset: fall through to the def generator (whose def the
    # override stamps) instead of dragging a wrong-nation preset's livery and
    # authored roster along.
    greek = _squadron_def(Greece.id)
    assigner = _assigner({"F-16": [greek]})
    picked = assigner.find_squadron_for_airframe(
        cast(Any, "F-16"),
        cast(Any, None),
        cast(Any, None),
        cast(Any, SimpleNamespace(id=USA.id)),
    )
    assert picked is None


def test_task_fallback_respects_pin() -> None:
    greek = _squadron_def(Greece.id, "Greek preset")
    us = _squadron_def(USA.id, "US preset")
    assigner = _assigner({"F-16": [greek], "F-15": [us]})
    picked = assigner.find_squadron_for_task(
        cast(Any, None), cast(Any, None), cast(Any, SimpleNamespace(id=USA.id))
    )
    assert picked is us


def test_override_stamps_pinned_country() -> None:
    squadron_def = _squadron_def(Greece.id)
    result = DefaultSquadronAssigner.override_squadron_defaults(
        cast(Any, squadron_def), _config("USA")
    )
    assert result is squadron_def
    assert squadron_def.country.id == USA.id
    assert squadron_def.country.name == "USA"


def test_override_aborts_on_unknown_name() -> None:
    # An unknown pinned country name raises out of override_squadron_defaults
    # too, so New Game aborts wherever the config is first resolved.
    squadron_def = _squadron_def(Greece.id)
    with pytest.raises(ValueError):
        DefaultSquadronAssigner.override_squadron_defaults(
            cast(Any, squadron_def), _config("Atlantis")
        )


def test_override_without_pin_is_untouched() -> None:
    squadron_def = _squadron_def(Greece.id)
    DefaultSquadronAssigner.override_squadron_defaults(
        cast(Any, squadron_def), _config(None)
    )
    assert squadron_def.country.id == Greece.id


def test_pinned_country_restamps_a_named_preset_of_another_nation() -> None:
    # A named preset wins the airframe pick (the author asked for that unit), but
    # a different-nation pin re-stamps only the nation -- it never drags in a
    # wrong-nation preset. This is the pick-keeps-the-unit, pin-fixes-the-voice
    # contract.
    greek_named_preset = _squadron_def(Greece.id, "The 335th Squadron")
    DefaultSquadronAssigner.override_squadron_defaults(
        cast(Any, greek_named_preset), _config("USA")
    )
    assert greek_named_preset.country.id == USA.id
    # The preset object (its name/livery) is otherwise untouched.
    assert greek_named_preset.name == "The 335th Squadron"


def test_named_preset_pick_ignores_nation() -> None:
    # find_squadron_by_name matches on the author's name regardless of the
    # preset's nation -- that is why the pin has to re-stamp afterward.
    greek_named_preset = _squadron_def(Greece.id, "The 335th Squadron")
    greek_named_preset.aircraft = SimpleNamespace()
    assigner = _assigner({"F-16": [greek_named_preset]})
    control_point = cast(Any, SimpleNamespace(can_operate=lambda aircraft: True))
    picked = assigner.find_squadron_by_name(
        "The 335th Squadron", cast(Any, None), control_point
    )
    assert picked is greek_named_preset


def test_saved_country_round_trips() -> None:
    # Save Config (AirWingConfigurationDialog._build_air_wing) writes
    # "country": squadron.country.name for every squadron; reloading must
    # restore that nation instead of rerolling it. Assert the data contract of
    # that round-trip: an exported entry parses back to the same country.
    exported = {"primary": "BARCAP", "aircraft": ["F-16C"], "country": "USA"}
    reloaded = SquadronConfig.from_data(exported)
    assert reloaded.country == "USA"
    resolved = resolve_config_country(reloaded)
    assert resolved is not None and resolved.id == USA.id
