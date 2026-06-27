"""Campaign-date gating for era-specific aircraft *properties* (mission options).

This mirrors weapon date-gating (``game.data.weapons.Weapon.available_on``) but for the
DCS unit "properties" exposed in the payload editor — the per-airframe mission options
such as the pilot helmet-mounted device. Weapons carry an introduction year in their
data; properties do not, so this module supplies a small curated table.

The table is keyed by the property value *label* (e.g. ``"JHMCS"``), not the numeric id.
That is deliberate: across airframes the same id means different things — ``HelmetMounted-
Device`` id ``1`` is ``"JHMCS"`` on the F/A-18 and F-16 but ``"SURA Visor"`` (a 1980s
Soviet helmet sight) on the Su-30/Su-35 — so an id-based gate would wrongly restrict the
Soviet sight. The gate is further scoped to the helmet-device property identifiers so it
can never touch an unrelated option that happens to share a gated label.

Only genuinely era-defining cueing systems belong in the table; the baseline options
(Visor Only, Not installed, NVG, the Soviet SURA Visor) are intentionally absent so they
stay available in every era. The whole layer is a no-op unless the campaign's
``restrict_weapons_by_date`` setting is on — the same toggle that gates weapons.
"""

from __future__ import annotations

import datetime
from typing import Optional, Union

from dcs.unitpropertydescription import UnitPropertyDescription

#: The id type pydcs uses for ``UnitPropertyDescription.values`` keys.
PropertyValueId = Union[str, int, float, None]

#: Property identifiers that carry a helmet-mounted cueing selection. Scoping the gate to
#: these keeps it from touching any unrelated property that shares a gated value label.
HELMET_DEVICE_PROPERTY_IDS: frozenset[str] = frozenset(
    {"HelmetMountedDevice", "HelmetMountedDeviceWSO"}
)

#: Helmet-mounted cueing systems gated by their real-world fielding year, keyed by the
#: pydcs value label. JHMCS (Joint Helmet-Mounted Cueing System) reached operational
#: service on US fighters (F-15C, then F/A-18 and F-16) circa 2003. Extend this with
#: other era-defining systems (e.g. Scorpion HMCS) as the data is curated.
HELMET_CUEING_INTRODUCTION_YEARS: dict[str, int] = {
    "JHMCS": 2003,
}


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
