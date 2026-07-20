"""Sensible per-airframe country choices (#627 surfacing).

DCS's own per-country unit rosters (pydcs ``Country.planes``/``.helicopters``)
are authoritative for AI-only types, but every player-flyable module is listed
under ALL countries -- that is ED's data (you may fly any module under any
nation in the ME), which makes the roster useless for choosing a *sensible*
squadron nation: the F/A-18C offers the Third Reich. Resolution order:

1. A curated family-operator row, for the flyable modules whose roster is
   non-discriminating (real-world operator families, DCS country names only,
   validated by test).
2. The type's own roster, when it discriminates (all AI-only types).
3. A same-family AI sibling's roster -- the AI type carries ED's real operator
   data for the family (e.g. the AI F-15E for the F-15E Strike Eagle module).
4. No data: empty -- the caller should offer the full country list (mods and
   the types without a row keep the unfiltered behavior).
"""

from __future__ import annotations

from typing import Optional, Type

from dcs.countries import country_dict
from dcs.country import Country
from dcs.helicopters import helicopter_map
from dcs.planes import plane_map
from dcs.unittype import FlyingType

from game.dcs.countries import country_with_name

#: Real-world operator families for flyable modules whose DCS roster admits
#: every country (see module docstring). Family-level: any nation that flew a
#: close variant of the module's family is listed. Keys are pydcs unit ids;
#: AI stand-ins of the same family alias the same row.
_HORNET = (
    "USA",
    "USAF Aggressors",
    "Canada",
    "Australia",
    "Spain",
    "Finland",
    "Switzerland",
    "Kuwait",
    "Malaysia",
)
_A10 = ("USA",)
_HARRIER = ("USA", "Spain", "Italy")
_F4E = (
    "USA",
    "USAF Aggressors",
    "Germany",
    "Greece",
    "Turkey",
    "Israel",
    "Iran",
    "Egypt",
    "South Korea",
    "Japan",
)
_F5E = (
    "USA",
    "USAF Aggressors",
    "Switzerland",
    "Norway",
    "Greece",
    "Turkey",
    "Iran",
    "South Korea",
    "Brazil",
    "Mexico",
    "Chile",
    "Honduras",
    "Jordan",
    "Morocco",
    "Tunisia",
    "Thailand",
    "Vietnam",
    "Saudi Arabia",
)
_MIG21 = (
    "USSR",
    "Russia",
    "GDR",
    "Poland",
    "Czech Republic",
    "Slovakia",
    "Hungary",
    "Bulgaria",
    "Romania",
    "Yugoslavia",
    "Serbia",
    "Croatia",
    "Finland",
    "India",
    "Vietnam",
    "North Korea",
    "China",
    "Cuba",
    "Egypt",
    "Syria",
    "Iraq",
    "Libya",
    "Algeria",
    "Sudan",
    "Yemen",
    "Ethiopia",
    "Afghanistan",
)
_JF17 = ("Pakistan", "China", "Nigeria")
_KA50 = ("Russia",)
_GAZELLE = (
    "France",
    "UK",
    "Egypt",
    "Lebanon",
    "Syria",
    "Qatar",
    "Kuwait",
    "United Arab Emirates",
    "Morocco",
    "Tunisia",
    "Cyprus",
    "Yugoslavia",
    "Serbia",
)

CURATED_OPERATORS: dict[str, tuple[str, ...]] = {
    "FA-18C_hornet": _HORNET,
    "F/A-18C": _HORNET,
    "A-10C": _A10,
    "A-10C_2": _A10,
    "A-10A": _A10,
    "AV8BNA": _HARRIER,
    "F-4E-45MC": _F4E,
    "F-4E": _F4E,
    "F-5E-3": _F5E,
    "F-5E": _F5E,
    "MiG-21Bis": _MIG21,
    "JF-17": _JF17,
    "Ka-50": _KA50,
    "Ka-50_3": _KA50,
    "SA342M": _GAZELLE,
    "SA342L": _GAZELLE,
    "SA342Mistral": _GAZELLE,
    "SA342Minigun": _GAZELLE,
}

#: Flyable module -> AI type of the same family whose roster carries ED's real
#: per-nation operator data. Only listed where the module's own roster is
#: non-discriminating and the sibling's is (verified against pydcs).
AI_SIBLING_IDS: dict[str, str] = {
    "F-16C_50": "F-16C bl.50",
    "F-15ESE": "F-15E",
    "M-2000C": "Mirage 2000-5",
    "AH-64D_BLK_II": "AH-64D",
    "CH-47Fbl1": "CH-47D",
    "Mi-24P": "Mi-24V",
}


def _roster(unit_type: Type[FlyingType]) -> list[Country]:
    return [
        country_type()
        for country_type in country_dict.values()
        if unit_type in country_type.planes or unit_type in country_type.helicopters
    ]


def _type_by_id(unit_id: str) -> Optional[Type[FlyingType]]:
    return plane_map.get(unit_id) or helicopter_map.get(unit_id)


def operator_countries(unit_type: Type[FlyingType]) -> list[Country]:
    """Countries that sensibly operate the airframe, or [] when there is no data.

    An empty result means "no operator data" (a mod, or a type without a
    curated row) -- the caller should fall back to the full country list, not
    to an empty choice.
    """
    curated = CURATED_OPERATORS.get(unit_type.id)
    if curated is not None:
        return [country_with_name(name) for name in curated]

    roster = _roster(unit_type)
    if 0 < len(roster) < len(country_dict):
        return roster

    sibling_id = AI_SIBLING_IDS.get(unit_type.id)
    if sibling_id is not None:
        sibling = _type_by_id(sibling_id)
        if sibling is not None:
            sibling_roster = _roster(sibling)
            if 0 < len(sibling_roster) < len(country_dict):
                return sibling_roster

    return []
