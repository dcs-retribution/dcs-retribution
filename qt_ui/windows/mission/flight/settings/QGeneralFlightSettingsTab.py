from PySide2.QtCore import Signal
from PySide2.QtWidgets import QFrame, QGridLayout, QVBoxLayout

from game import Game
from game.ato.flight import Flight
from qt_ui.models import PackageModel, GameModel
from qt_ui.windows.mission.flight.settings.FlightAirfieldDisplay import (
    FlightAirfieldDisplay,
)
from qt_ui.windows.mission.flight.settings.QCommsEditor import QCommsEditor
from qt_ui.windows.mission.flight.settings.QCustomName import QFlightCustomName
from qt_ui.windows.mission.flight.settings.QFlightSlotEditor import QFlightSlotEditor
from qt_ui.windows.mission.flight.settings.QFlightStartType import QFlightStartType
from qt_ui.windows.mission.flight.settings.QFlightTypeTaskInfo import (
    QFlightTypeTaskInfo,
)


class QGeneralFlightSettingsTab(QFrame):
    on_flight_settings_changed = Signal()

    def __init__(self, game: GameModel, package_model: PackageModel, flight: Flight):
        super().__init__()

        widgets = [
            QFlightTypeTaskInfo(flight),
            QCommsEditor(flight, game),
            FlightAirfieldDisplay(game.game, package_model, flight),
            QFlightSlotEditor(package_model, flight, game.game),
            QFlightStartType(package_model, flight),
            QFlightCustomName(flight),
        ]
        layout = QGridLayout()
        row = 0
        for w in widgets:
            layout.addWidget(w, row, 0)
            row += 1
        vstretch = QVBoxLayout()
        vstretch.addStretch()
        layout.addLayout(vstretch, row, 0)
        self.setLayout(layout)
