"""Campaign-date gating for era-specific aircraft *properties* (mission options).

This mirrors weapon date-gating (``game.data.weapons.Weapon.available_on``) but for
the DCS unit "properties" exposed in the payload editor — the per-airframe mission
options such as the pilot's helmet-mounted cueing system. Weapons carry an
introduction year in their data; properties do not, so each aircraft's own data file
supplies one: the ``date_gated_properties`` block in
``resources/units/aircraft/<type>.yaml`` maps a property identifier to
``{value label: introduction year}`` and loads into
``AircraftType.property_date_gate``, so lookup is a direct attribute access on the
airframe being configured — no shared table, no cross-airframe iteration.

The block is keyed by the property value *label* (e.g. ``"JHMCS"``), not the numeric
id. That is deliberate: the label pins the gate to what the option actually *is* — if
a DCS/pydcs update renumbers or renames a value, a label key degrades to "not gated"
instead of gating the wrong option (and a test pins the labels against pydcs so that
degradation is caught rather than shipped).

Only genuinely era-defining cueing systems belong in the data; the baseline options
(``Not installed``, ``Visor Only``, ``NVG``) are intentionally absent so they stay
available in every era. The whole layer is a no-op unless the campaign's
``restrict_props_by_date`` setting is on — independent of the weapons toggle so users
can enforce either or both.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Any, Iterator, Mapping, Optional, Union

from dcs.unitpropertydescription import UnitPropertyDescription

#: The id type pydcs uses for ``UnitPropertyDescription.values`` keys.
PropertyValueId = Union[str, int, float, None]


@dataclass(frozen=True)
class PropertyDateGate:
    """Date gate for one airframe's era-specific property values.

    Built by :meth:`from_data` from the aircraft data file's
    ``date_gated_properties`` block. An empty gate (the default for the many
    airframes that declare no block) is falsy and gates nothing, so every method is
    safe to call unconditionally.
    """

    #: Property identifier -> value label -> real-world introduction year.
    introduction_years: Mapping[str, Mapping[str, int]] = field(default_factory=dict)

    @classmethod
    def from_data(cls, data: Optional[Mapping[str, Any]]) -> PropertyDateGate:
        """Build a gate from a yaml ``date_gated_properties`` block (or None)."""
        if not data:
            return cls()
        return cls(
            {
                str(identifier): {
                    str(label): int(year) for label, year in labels.items()
                }
                for identifier, labels in data.items()
            }
        )

    def __bool__(self) -> bool:
        return bool(self.introduction_years)

    def _introduction_year(
        self, prop: UnitPropertyDescription, value_id: PropertyValueId
    ) -> Optional[int]:
        """The introduction year for a property value, or None if not gated."""
        labels = self.introduction_years.get(prop.identifier)
        if labels is None or prop.values is None:
            return None
        label = prop.values.get(value_id)
        if label is None:
            return None
        return labels.get(label)

    def value_available_on(
        self,
        prop: UnitPropertyDescription,
        value_id: PropertyValueId,
        date: datetime.date,
    ) -> bool:
        """Whether a single property value is available at the campaign ``date``.

        Returns True for any value that is not date-gated (the common case), so
        callers can treat every non-gated property — and every era-appropriate
        gated option — as always available.
        """
        year = self._introduction_year(prop, value_id)
        if year is None:
            return True
        return date >= datetime.date(year, 1, 1)

    def available_value_ids(
        self, prop: UnitPropertyDescription, date: datetime.date
    ) -> list[PropertyValueId]:
        """The value ids of ``prop`` available at ``date``, in declared order."""
        if prop.values is None:
            return []
        return [
            value_id
            for value_id in prop.values
            if self.value_available_on(prop, value_id, date)
        ]

    def period_correct_value(
        self,
        prop: UnitPropertyDescription,
        current: PropertyValueId,
        date: datetime.date,
    ) -> PropertyValueId:
        """Clamp ``current`` to a value that is period-correct for ``prop`` at ``date``.

        Returns ``current`` unchanged when it is already available. Otherwise returns
        the first still-available value, which on every affected airframe is the
        baseline "no modern cueing" option (``Not installed`` / ``Visor Only``).
        Falls back to ``current`` if nothing is available (not expected for the
        curated data).
        """
        if self.value_available_on(prop, current, date):
            return current
        allowed = self.available_value_ids(prop, date)
        if not allowed:
            return current
        return allowed[0]

    def gated_props(
        self, properties: Mapping[str, UnitPropertyDescription]
    ) -> Iterator[UnitPropertyDescription]:
        """The subset of an airframe's ``properties`` this gate has data for.

        Iterates only the gated identifiers (not every property of the airframe), so
        a consumer clamping generated missions touches exactly the curated options.
        """
        for identifier in self.introduction_years:
            prop = properties.get(identifier)
            if prop is not None:
                yield prop
