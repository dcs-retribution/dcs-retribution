from PySide2.QtCore import Signal
from PySide2.QtWidgets import QFrame, QGridLayout, QVBoxLayout

from game.ato.flight import Flight
from qt_ui.models import PackageModel, GameModel
from qt_ui.windows.mission.flight.settings.FlightPlanPropertiesGroup import (
    FlightPlanPropertiesGroup,
)
from qt_ui.windows.mission.flight.settings.QCommsEditor import QCommsEditor
from qt_ui.windows.mission.flight.settings.QCustomName import QFlightCustomName
from qt_ui.windows.mission.flight.settings.QFlightSlotEditor import QFlightSlotEditor
from qt_ui.windows.mission.flight.settings.QFlightStartType import QFlightStartType
from qt_ui.windows.mission.flight.settings.QFlightTypeTaskInfo import (
    QFlightTypeTaskInfo,
)
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointList import (
    QFlightWaypointList,
)


class QGeneralFlightSettingsTab(QFrame):
    flight_size_changed = Signal()

    def __init__(
        self,
        game: GameModel,
        package_model: PackageModel,
        flight: Flight,
        flight_wpt_list: QFlightWaypointList,
    ):
        super().__init__()

        self.flight_slot_editor = QFlightSlotEditor(package_model, flight, game.game)
        self.flight_slot_editor.flight_resized.connect(self.flight_size_changed)

        widgets = [
            QFlightTypeTaskInfo(flight),
            QCommsEditor(flight, game),
            FlightPlanPropertiesGroup(
                game.game, package_model, flight, flight_wpt_list
            ),
            self.flight_slot_editor,
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
