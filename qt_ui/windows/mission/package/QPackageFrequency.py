from typing import Optional, Type

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QDialog,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QDoubleSpinBox,
)

from game import Game
from game.ato.package import Package
from game.radio.radios import RadioRegistry
from qt_ui.uiconstants import EVENT_ICONS


class QPackageFrequency(QDialog):
    def __init__(self, game: Game, package: Package, parent=None) -> None:
        super().__init__(parent=parent)
        self.setMinimumWidth(400)

        self.game = game
        self.package = package

        # Make dialog modal to prevent background windows to close unexpectedly.
        self.setModal(True)

        self.setWindowTitle("Assign frequency")
        self.setWindowIcon(EVENT_ICONS["strike"])

        layout = QHBoxLayout()

        self.frequency_label = QLabel("FREQ (Mhz):")
        self.frequency_input = QDoubleSpinBox()
        self.frequency_input.setRange(225, 399.975)
        self.frequency_input.setSingleStep(0.025)
        self.frequency_input.setDecimals(3)
        layout.addWidget(self.frequency_label)
        layout.addWidget(self.frequency_input)

        self.create_button = QPushButton("Save")
        self.create_button.clicked.connect(self.accept)
        layout.addWidget(self.create_button, alignment=Qt.AlignRight)

        self.setLayout(layout)
