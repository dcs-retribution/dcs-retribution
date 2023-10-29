from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QSpinBox,
    QComboBox,
    QLineEdit,
)

from game.radio.TacanContainer import TacanContainer
from qt_ui.uiconstants import EVENT_ICONS


class QTacanDialog(QDialog):
    def __init__(self, parent=None, container: Optional[TacanContainer] = None) -> None:
        super().__init__(parent=parent)
        self.container = container
        self.setMinimumWidth(400)

        # Make dialog modal to prevent background windows to close unexpectedly.
        self.setModal(True)

        self.setWindowTitle("Assign TACAN")
        self.setWindowIcon(EVENT_ICONS["strike"])

        layout = QHBoxLayout()

        self.tacan_label = QLabel("TACAN:")
        self.tacan_input = QSpinBox()
        self.tacan_input.setRange(1, 126)
        self.tacan_input.setSingleStep(1)
        layout.addWidget(self.tacan_label)
        layout.addStretch()
        layout.addWidget(self.tacan_input)
        self.band_input = QComboBox()
        self.band_input.addItems(["X", "Y"])
        layout.addWidget(self.band_input)
        self.callsign_input = QLineEdit()
        self.callsign_input.setMaxLength(3)
        self.callsign_input.setMaximumWidth(50)
        layout.addWidget(self.callsign_input)
        layout.addStretch()

        self.create_button = QPushButton("Save")
        self.create_button.clicked.connect(self.accept)
        layout.addWidget(self.create_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)

        if container is not None:
            if container.tcn_name is not None:
                self.callsign_input.setText(container.tcn_name)
            if container.tacan is not None:
                self.tacan_input.setValue(container.tacan.number)
                self.band_input.setCurrentText(container.tacan.band.value)
