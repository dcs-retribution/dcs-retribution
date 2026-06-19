"""Combo box for selecting squadrons."""

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox

from game.ato.flighttype import FlightType
from game.dcs.aircrafttype import AircraftType
from game.squadrons.airwing import AirWing
from game.squadrons.squadron import Squadron
from game.theater import MissionTarget
from game.utils import Distance


class SquadronSelector(QComboBox):
    """Combo box for selecting squadrons compatible with the given requirements."""

    def __init__(
        self,
        air_wing: AirWing,
        task: Optional[FlightType],
        aircraft: Optional[AircraftType],
        mission_target: Optional[MissionTarget] = None,
    ) -> None:
        super().__init__()
        self.air_wing = air_wing
        self.mission_target = mission_target

        self.model().sort(0)
        self.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.currentIndexChanged.connect(lambda _index: self._update_current_tooltip())
        self.update_items(task, aircraft)

    @property
    def aircraft_available(self) -> int:
        squadron = self.currentData()
        if squadron is None:
            return 0
        return squadron.untasked_aircraft

    def update_items(
        self, task: Optional[FlightType], aircraft: Optional[AircraftType]
    ) -> None:
        current_squadron = self.currentData()
        self.blockSignals(True)
        try:
            self.clear()
        finally:
            self.blockSignals(False)
        if task is None:
            self.addItem("No task selected", None)
            self.setToolTip("Select a mission task to see compatible squadrons.")
            return
        if aircraft is None:
            self.addItem("No aircraft selected", None)
            self.setToolTip(
                "Select an aircraft type to see squadrons that can fly the chosen task."
            )
            return

        for squadron in self.air_wing.squadrons_for(aircraft):
            valid_task = squadron.capable_of(task)
            runway_operational = squadron.location.runway_is_operational()
            if valid_task and squadron.untasked_aircraft and runway_operational:
                self.addItem(f"{squadron.location}: {squadron}", squadron)
                self.setItemData(
                    self.count() - 1,
                    self._tooltip_for_squadron(squadron, task),
                    Qt.ItemDataRole.ToolTipRole,
                )

        if self.count() == 0:
            self.addItem("No capable aircraft available", None)
            self.setToolTip(
                "No squadron with this aircraft currently has the selected task, a "
                "working runway, and spare untasked aircraft."
            )
            return

        if current_squadron is not None:
            self.setCurrentText(f"{current_squadron.location}: {current_squadron}")
        self._update_current_tooltip()

    def _tooltip_for_squadron(self, squadron: Squadron, task: FlightType) -> str:
        details = [
            f"Primary role: {squadron.primary_task.value}",
            f"Auto-assignable for this task: {'Yes' if squadron.can_auto_assign(task) else 'No'}",
            f"Untasked aircraft: {squadron.untasked_aircraft}",
            f"Departure base: {squadron.location.name}",
        ]
        if self.mission_target is not None:
            distance = Distance.from_meters(
                squadron.location.distance_to(self.mission_target)
            ).nautical_miles
            details.append(f"Distance to target: {distance:.0f} NM")
        return "\n".join(details)

    def _update_current_tooltip(self) -> None:
        index = self.currentIndex()
        tooltip = self.itemData(index, Qt.ItemDataRole.ToolTipRole)
        if tooltip:
            self.setToolTip(tooltip)
