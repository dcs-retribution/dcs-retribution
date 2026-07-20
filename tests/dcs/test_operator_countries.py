"""Sensible per-airframe country choices for the squadron country selector (#627).

Flyable modules are listed under every DCS country (ED's own data -- any module
may fly under any nation in the ME), so the country selector needs better
sources: curated family rows for those modules, the pydcs per-country roster
for AI types, an AI sibling's roster for modules like the F-15E, and an
explicit no-data signal (empty) for mods. The curated tables are typo-guarded
here so a pydcs unit or country rename fails CI instead of silently dropping a
nation from the picker.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, cast

from dcs.countries import country_dict
from dcs.helicopters import helicopter_map
from dcs.planes import plane_map

from game.dcs.countries import country_with_name
from game.dcs.operatorcountries import (
    AI_SIBLING_IDS,
    CURATED_OPERATORS,
    operator_countries,
)


def _names(unit_id: str) -> set[str]:
    unit = plane_map.get(unit_id) or helicopter_map[unit_id]
    return {country.name for country in operator_countries(unit)}


def test_curated_flyable_module_is_trimmed() -> None:
    # The motivating case: the flyable Hornet's DCS roster admits every country
    # (even the Third Reich), so its curated family row applies.
    names = _names("FA-18C_hornet")
    assert "USA" in names
    assert "Malaysia" in names
    assert "Third Reich" not in names
    assert len(names) < 20


def test_discriminating_roster_is_used_for_ai_types() -> None:
    names = _names("Tornado GR4")
    assert "UK" in names
    assert "USA" not in names
    assert len(names) < 10


def test_ai_sibling_roster_covers_flyable_modules() -> None:
    # The F-15E module's own roster admits everyone; the AI F-15E's is ED's
    # real operator list for the family.
    names = _names("F-15ESE")
    assert "Saudi Arabia" in names
    assert "Third Reich" not in names
    assert len(names) < 12


def test_no_operator_data_yields_empty() -> None:
    # A mod airframe pydcs knows nothing about: the caller falls back to the
    # full list, so the signal must be empty, never a partial guess.
    fake = cast(Any, SimpleNamespace(id="Not A Real Jet"))
    assert operator_countries(fake) == []


def test_curated_tables_resolve_against_pydcs() -> None:
    # A pydcs unit or country rename must fail CI, not silently drop a nation.
    for unit_id, names in CURATED_OPERATORS.items():
        assert plane_map.get(unit_id) or helicopter_map.get(unit_id), unit_id
        for name in names:
            country_with_name(name)  # raises KeyError on a bad name


def test_ai_siblings_resolve_and_discriminate() -> None:
    for module_id, sibling_id in AI_SIBLING_IDS.items():
        assert plane_map.get(module_id) or helicopter_map.get(module_id), module_id
        sibling = plane_map.get(sibling_id) or helicopter_map.get(sibling_id)
        assert sibling is not None, sibling_id
        roster_size = len(operator_countries(sibling))
        assert 0 < roster_size < len(country_dict), sibling_id
