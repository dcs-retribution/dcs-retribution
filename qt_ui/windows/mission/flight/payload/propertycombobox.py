from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QComboBox
from dcs.unitpropertydescription import UnitPropertyDescription

from game.ato.flightmember import FlightMember
from game.dcs.aircrafttype import AircraftType
from .missingpropertydataerror import MissingPropertyDataError

if TYPE_CHECKING:
    from game import Game


class PropertyComboBox(QComboBox):
    def __init__(
        self,
        flight_member: FlightMember,
        prop: UnitPropertyDescription,
        aircraft: AircraftType,
        game: Game,
    ) -> None:
        super().__init__()
        self.flight_member = flight_member
        self.prop = prop
        self.gate = aircraft.property_date_gate
        self.game = game

        if prop.values is None:
            raise MissingPropertyDataError("values cannot be None")
        if prop.default is None:
            raise MissingPropertyDataError("default cannot be None")

        current_value = self.flight_member.properties.get(
            self.prop.identifier, self.prop.default
        )

        if self.game.settings.restrict_props_by_date:
            value_ids = self.gate.available_value_ids(prop, self.game.date)
            # If the stored/default selection is gated out for the campaign date, show a
            # period-correct value instead. Storage is left untouched (mirroring weapon
            # degrade) — the mission generator applies the same clamp at generation.
            current_value = self.gate.period_correct_value(
                prop, current_value, self.game.date
            )
        else:
            value_ids = list(prop.values)

        for ident in value_ids:
            text = prop.values[ident]
            self.addItem(text, ident)
            if ident == current_value:
                self.setCurrentText(text)

        self.currentIndexChanged.connect(self.on_selection_changed)

    def on_selection_changed(self, _index: int) -> None:
        self.flight_member.properties[self.prop.identifier] = self.currentData()

    def set_flight_member(self, flight_member: FlightMember) -> None:
        self.flight_member = flight_member
        if self.prop.values is None or self.prop.default is None:
            return
        current_value = flight_member.properties.get(
            self.prop.identifier, self.prop.default
        )
        if self.game.settings.restrict_props_by_date:
            current_value = self.gate.period_correct_value(
                self.prop, current_value, self.game.date
            )
        text = self.prop.values.get(current_value)
        if text is not None:
            self.setCurrentText(text)
