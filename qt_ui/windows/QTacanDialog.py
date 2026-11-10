from typing import Iterable, Optional

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
from game.radio.tacan import TacanBand, TacanChannel
from qt_ui.uiconstants import EVENT_ICONS


class QTacanDialog(QDialog):
    def __init__(
        self,
        parent=None,
        container: Optional[TacanContainer] = None,
        unavailable_channels: Iterable[TacanChannel] = (),
    ) -> None:
        super().__init__(parent=parent)
        self.container = container
        self.unavailable_channels = set(unavailable_channels)
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

        self.warning_label = QLabel()
        self.warning_label.setStyleSheet("color: orange")
        layout.addWidget(self.warning_label)
        layout.addStretch()

        self.create_button = QPushButton("Save")
        self.create_button.clicked.connect(self.accept)
        layout.addWidget(self.create_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)

        self.tacan_input.valueChanged.connect(self.update_availability_warning)
        self.band_input.currentTextChanged.connect(self.update_availability_warning)

        if container is not None:
            if container.tcn_name is not None:
                self.callsign_input.setText(container.tcn_name)
            if container.tacan is not None:
                self.tacan_input.setValue(container.tacan.number)
                self.band_input.setCurrentText(container.tacan.band.value)

        self.update_availability_warning()

    def selected_channel(self) -> TacanChannel:
        band = TacanBand.X if self.band_input.currentText() == "X" else TacanBand.Y
        return TacanChannel(self.tacan_input.value(), band)

    def update_availability_warning(self) -> None:
        if self.selected_channel() in self.unavailable_channels:
            self.warning_label.setText("Already in use!")
            self.warning_label.setToolTip(
                "This TACAN channel is already used by a map beacon, another "
                "carrier/airfield, or a flight. Verify that this is intentional."
            )
        else:
            self.warning_label.setText("")
            self.warning_label.setToolTip(None)
