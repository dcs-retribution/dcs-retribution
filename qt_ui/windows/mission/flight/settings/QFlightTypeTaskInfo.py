from PySide6.QtWidgets import QLabel, QGroupBox, QGridLayout

from qt_ui.uiconstants import AIRCRAFT_ICONS


class QFlightTypeTaskInfo(QGroupBox):
    def __init__(self, flight):
        super(QFlightTypeTaskInfo, self).__init__("Flight")
        self.flight = flight

        layout = QGridLayout()

        self.aircraft_icon = QLabel()
        # Replace slashes with underscores because slashes are not allowed in filenames
        if self.flight.unit_type.dcs_id.replace("/", "_") in AIRCRAFT_ICONS:
            self.aircraft_icon.setPixmap(
                AIRCRAFT_ICONS[self.flight.unit_type.dcs_id.replace("/", "_")]
            )

        self.task = QLabel("Task:")
        self.task_type = QLabel(str(flight.flight_type))
        self.task_type.setProperty("style", flight.flight_type.name)

        layout.addWidget(self.aircraft_icon, 0, 0)

        layout.addWidget(self.task, 1, 0)
        layout.addWidget(self.task_type, 1, 1)

        self.setLayout(layout)
