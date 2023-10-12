from typing import Optional

from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QLineEdit, QLabel, QMessageBox

from game.ato.flight import Flight


class QFlightCustomName(QGroupBox):
    def __init__(self, flight: Flight):
        super(QFlightCustomName, self).__init__()

        self.flight = flight

        self.layout = QHBoxLayout()
        self.custom_name_label = QLabel(f"Custom Name:")
        self.custom_name_input = QLineEdit(flight.custom_name)
        self.custom_name_input.textChanged.connect(self.on_change)
        self.layout.addWidget(self.custom_name_label)
        self.layout.addWidget(self.custom_name_input)
        self.setLayout(self.layout)

    def on_change(self) -> None:
        error = self.verify_form()
        if error is not None:
            QMessageBox.critical(self, "Could not edit flight", error)
            return
        self.flight.custom_name = self.custom_name_input.text()

    def verify_form(self) -> Optional[str]:
        if "|" in self.custom_name_input.text():
            return f"Cannot include | in flight name"
        return None
