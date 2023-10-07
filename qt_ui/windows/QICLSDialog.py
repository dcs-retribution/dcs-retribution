from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QSpinBox,
    QLineEdit,
)

from game.radio.ICLSContainer import ICLSContainer
from qt_ui.uiconstants import EVENT_ICONS


class QICLSDialog(QDialog):
    def __init__(self, parent=None, container: Optional[ICLSContainer] = None) -> None:
        super().__init__(parent=parent)
        self.container = container
        self.setMinimumWidth(400)

        # Make dialog modal to prevent background windows to close unexpectedly.
        self.setModal(True)

        self.setWindowTitle("Assign ICLS")
        self.setWindowIcon(EVENT_ICONS["strike"])

        layout = QHBoxLayout()

        self.icls_label = QLabel("ICLS:")
        self.icls_input = QSpinBox()
        self.icls_input.setRange(1, 20)
        self.icls_input.setSingleStep(1)
        layout.addWidget(self.icls_label)
        layout.addStretch()
        layout.addWidget(self.icls_input)
        self.callsign_input = QLineEdit()
        self.callsign_input.setMaxLength(3)
        self.callsign_input.setMaximumWidth(50)
        layout.addWidget(self.callsign_input)
        layout.addStretch()

        self.create_button = QPushButton("Save")
        self.create_button.clicked.connect(self.accept)
        layout.addWidget(self.create_button, alignment=Qt.AlignRight)

        self.setLayout(layout)

        if container is not None:
            if container.icls_name is not None:
                self.callsign_input.setText(container.icls_name)
            if container.icls_channel is not None:
                self.icls_input.setValue(container.icls_channel)
