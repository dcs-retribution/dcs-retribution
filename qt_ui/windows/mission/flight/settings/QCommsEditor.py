from PySide6.QtWidgets import QGroupBox, QVBoxLayout

from game.ato import Flight, FlightType
from qt_ui.models import GameModel
from qt_ui.widgets.QFrequencyWidget import QFrequencyWidget
from qt_ui.widgets.QTacanWidget import QTacanWidget


class QCommsEditor(QGroupBox):
    def __init__(self, flight: Flight, game: GameModel):
        title = "Intra-Flight Frequency"

        layout = QVBoxLayout()

        is_refuel = flight.flight_type == FlightType.REFUELING
        has_tacan = flight.unit_type.dcs_unit_type.tacan

        layout.addWidget(QFrequencyWidget(flight, game))
        if is_refuel and has_tacan:
            layout.addWidget(QTacanWidget(flight, game))
            title = title + " / TACAN"
        super(QCommsEditor, self).__init__(title)
        self.flight = flight

        self.setLayout(layout)
