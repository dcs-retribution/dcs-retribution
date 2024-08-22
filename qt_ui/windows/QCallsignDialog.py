from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QSpinBox,
    QComboBox,
)

from game.radio.CallsignContainer import CallsignContainer
from qt_ui.uiconstants import EVENT_ICONS


class QCallsignDialog(QDialog):
    def __init__(
        self, parent=None, container: Optional[CallsignContainer] = None
    ) -> None:
        super().__init__(parent=parent)
        self.container = container
        self.setMinimumWidth(400)

        # Make dialog modal to prevent background windows to close unexpectedly.
        self.setModal(True)

        self.setWindowTitle("Assign Callsign")
        self.setWindowIcon(EVENT_ICONS["strike"])

        layout = QHBoxLayout()

        self.callsign_label = QLabel("Callsign:")
        self.callsign_name_input = QComboBox()
        self.callsign_name_input.addItems(container.available_callsigns)
        self.callsign_nr_input = QSpinBox()
        self.callsign_nr_input.setRange(1, 9)
        self.callsign_nr_input.setSingleStep(1)
        self.callsign_nr_input.setMaximumWidth(50)
        layout.addWidget(self.callsign_label)
        layout.addStretch()
        layout.addWidget(self.callsign_name_input)
        layout.addStretch()
        layout.addWidget(self.callsign_nr_input)
        layout.addStretch()

        self.create_button = QPushButton("Save")
        self.create_button.clicked.connect(self.accept)
        layout.addWidget(self.create_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)

        if container is not None:
            if container.callsign is not None:
                self.callsign_name_input.setCurrentText(container.callsign.name)
                self.callsign_nr_input.setValue(container.callsign.nr)
