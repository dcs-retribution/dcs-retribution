"""Dialog window for editing flights."""

import logging

from PySide6.QtWidgets import (
    QDialog,
    QMessageBox,
    QVBoxLayout,
)

from game.ato.flight import Flight
from game.ato.flightplans.planningerror import PlanningError
from game.server import EventStream
from game.sim import GameUpdateEvents
from qt_ui.models import GameModel, PackageModel
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.windows.mission.flight.QFlightPlanner import QFlightPlanner


class QEditFlightDialog(QDialog):
    """Dialog window for editing flight plans and loadouts."""

    def __init__(
        self,
        game_model: GameModel,
        package_model: PackageModel,
        flight: Flight,
        parent=None,
    ) -> None:
        super().__init__(parent=parent)

        self.game_model = game_model
        self.flight = flight
        self.package_model = package_model
        self.events = GameUpdateEvents()

        self.setWindowTitle("Edit flight")
        self.setWindowIcon(EVENT_ICONS["strike"])
        self.setModal(True)

        layout = QVBoxLayout()

        self.flight_planner = QFlightPlanner(package_model, flight, game_model)
        self.flight_planner.squadron_changed.connect(self.on_squadron_change)
        layout.addWidget(self.flight_planner)

        self.setLayout(layout)
        self.finished.connect(self.on_close)

    def on_squadron_change(self, flight: Flight):
        self.events = GameUpdateEvents().delete_flight(self.flight)
        self.events = self.events.new_flight(flight)
        self.game_model.ato_model.client_slots_changed.emit()
        self.flight = flight
        self.reject()
        new_dialog = QEditFlightDialog(
            self.game_model, self.package_model, flight, self.parent()
        )
        new_dialog.show()

    def on_close(self, _result) -> None:
        self._recreate_package_if_standoff_changed()
        self.events = self.events.update_flight(self.flight)
        EventStream.put_nowait(self.events)
        self.game_model.ato_model.client_slots_changed.emit()

    def _recreate_package_if_standoff_changed(self) -> None:
        """Move the ingress point when the package's stand-off range changed.

        Editing the payload does not rebuild the flight plan, so the ingress point can
        be left at a distance that no longer matches the loadout (e.g. a Kh-22 was
        added or removed). The package waypoints remember the stand-off range they were
        built with, so if it now differs we offer to regenerate the package's flight
        plans (which resets their routes).
        """
        package = self.flight.package
        waypoints = package.waypoints
        if waypoints is None:
            return
        if waypoints.standoff_range == package.max_standoff_range():
            return

        result = QMessageBox.question(
            self,
            "Update flight plan?",
            (
                "The stand-off weapons in this package changed, so the ingress point "
                "should move to match the new launch range. This will regenerate the "
                "flight plan(s) for the package and reset any manual route changes. "
                "Continue?"
            ),
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )
        if result != QMessageBox.StandardButton.Yes:
            return

        package.waypoints = None
        for flight in package.flights:
            try:
                flight.recreate_flight_plan()
                self.events = self.events.update_flight(flight)
            except PlanningError:
                logging.exception(
                    "Could not regenerate flight plan after stand-off change"
                )
