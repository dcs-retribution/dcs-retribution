from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSlider, QSpinBox
from dcs.weather import CloudPreset

from game.weather.clouds import Clouds


class DcsCloudDensitySelector(QHBoxLayout):
    def __init__(self, clouds: Optional[Clouds]) -> None:
        super().__init__()
        self.unit_changing = False

        self.label = QLabel("Density : ")
        self.addWidget(self.label)

        self.density = QSlider(Qt.Orientation.Horizontal)
        self.density.setRange(0, 10)
        if clouds:
            self.density.setValue(clouds.density)
        self.density.valueChanged.connect(self.on_slider_change)
        self.addWidget(self.density, 1)

        self.density_spinner = QSpinBox()
        self.density_spinner.setValue(self.density.value())
        self.density_spinner.setFixedWidth(75)
        self.density_spinner.valueChanged.connect(self.update_slider)
        self.addWidget(self.density_spinner, 1)

    def on_slider_change(self, value: int) -> None:
        self.density_spinner.setValue(value)

    def update_slider(self, value: int) -> None:
        self.density.setValue(value)

    def update_ui(self, preset: Optional[CloudPreset]) -> None:
        self.label.setVisible(preset is None)
        self.density.setVisible(preset is None)
        self.density_spinner.setVisible(preset is None)

        if preset:
            self.density.setValue(0)
