"""Campaign-date gating for era-specific aircraft *properties* (mission options).

This mirrors weapon date-gating (``game.data.weapons.Weapon.available_on``) but for the
DCS unit "properties" exposed in the payload editor — the per-airframe mission options
such as the pilot helmet-mounted device. Weapons carry an introduction year in their
data; properties do not, so the dates live alongside them as YAML data.

Following the weapons model, each gated helmet-cueing system is one YAML file under
``resources/aircraftproperties/helmets/`` carrying its ``name``, ``introduction_year``
and the ``property_ids`` it applies to. The data is keyed by the property value *label*,
not the numeric id. That is essential: across airframes the same ``HelmetMountedDevice``
id ``1`` is a *different* era-defining system with a *different* fielding year —
``"JHMCS"`` on the F/A-18 and F-16 (~2003), ``"HMS"`` (the Soviet Shchel-3UM sight) on
the MiG-29 (~1985), ``"SURA Visor"`` on the Su-30 (~1996) and ``"HMCS"`` (Scorpion) on
the A-10C II (~2012). An id-based gate would have to apply one year to all of them; the
label key gives each its own. The gate is further scoped to each entry's ``property_ids``
so it can never touch an unrelated option that happens to share a gated label.

Only genuinely era-defining cueing systems belong in the data; the baseline options
(Visor Only, Not installed, plain NVG) are intentionally absent so they stay available in
every era. The whole layer is a no-op unless the campaign's ``restrict_weapons_by_date``
setting is on — the same toggle that gates weapons.
"""

from __future__ import annotations

import datetime
import logging
from pathlib import Path
from typing import Optional, Union

import yaml
from dcs.unitpropertydescription import UnitPropertyDescription

#: The id type pydcs uses for ``UnitPropertyDescription.values`` keys.
PropertyValueId = Union[str, int, float, None]

#: Directory holding one YAML file per date-gated helmet-cueing system.
_HELMET_DATA_DIR = Path("resources/aircraftproperties/helmets")

#: Property identifiers a helmet-cueing entry applies to when it omits ``property_ids``.
_DEFAULT_HELMET_PROPERTY_IDS = ("HelmetMountedDevice", "HelmetMountedDeviceWSO")


def _load_helmet_cueing_data() -> tuple[frozenset[str], dict[str, int]]:
    """Load the date-gated helmet-cueing data from the YAML files.

    Returns the set of helmet-device property identifiers the gate is scoped to (the
    union of every entry's ``property_ids``) and the label → introduction-year map.
    """
    property_ids: set[str] = set()
    introduction_years: dict[str, int] = {}
    for path in sorted(_HELMET_DATA_DIR.glob("*.yaml")):
        with path.open(encoding="utf8") as data_file:
            data = yaml.safe_load(data_file)
        name = data["name"]
        introduction_years[name] = int(data["introduction_year"])
        property_ids.update(data.get("property_ids", _DEFAULT_HELMET_PROPERTY_IDS))
    if not introduction_years:
        logging.warning("No helmet-cueing date data found in %s", _HELMET_DATA_DIR)
    return frozenset(property_ids), introduction_years


#: Property identifiers that carry a helmet-mounted cueing selection. Scoping the gate to
#: these keeps it from touching any unrelated property that shares a gated value label.
#: Helmet-mounted cueing systems gated by their real-world fielding year, keyed by the
#: pydcs value label (loaded from ``resources/aircraftproperties/helmets/*.yaml``).
HELMET_DEVICE_PROPERTY_IDS, HELMET_CUEING_INTRODUCTION_YEARS = (
    _load_helmet_cueing_data()
)


def _introduction_year(
    prop: UnitPropertyDescription, value_id: PropertyValueId
) -> Optional[int]:
    """The introduction year for a property value, or None if it is not date-gated."""
    if prop.identifier not in HELMET_DEVICE_PROPERTY_IDS:
        return None
    if prop.values is None:
        return None
    label = prop.values.get(value_id)
    if label is None:
        return None
    return HELMET_CUEING_INTRODUCTION_YEARS.get(label)


def property_value_available_on(
    prop: UnitPropertyDescription, value_id: PropertyValueId, date: datetime.date
) -> bool:
    """Whether a single property value is available at the campaign ``date``.

    Returns True for any value that is not date-gated (the common case), so callers can
    treat every non-helmet property — and every era-appropriate helmet option — as
    always available.
    """
    year = _introduction_year(prop, value_id)
    if year is None:
        return True
    return date >= datetime.date(year, 1, 1)


def available_value_ids(
    prop: UnitPropertyDescription, date: datetime.date
) -> list[PropertyValueId]:
    """The value ids of ``prop`` available at ``date``, in their declared order."""
    if prop.values is None:
        return []
    return [
        value_id
        for value_id in prop.values
        if property_value_available_on(prop, value_id, date)
    ]


def period_correct_value(
    prop: UnitPropertyDescription, current: PropertyValueId, date: datetime.date
) -> PropertyValueId:
    """Clamp ``current`` to a value that is period-correct for ``prop`` at ``date``.

    Returns ``current`` unchanged when it is already available. Otherwise returns the
    first still-available value, which on every affected airframe is the baseline
    "no modern cueing" option (``Not installed`` / ``Visor Only``). Falls back to
    ``current`` if nothing is available (not expected for the curated gate).
    """
    if property_value_available_on(prop, current, date):
        return current
    allowed = available_value_ids(prop, date)
    if not allowed:
        return current
    return allowed[0]
