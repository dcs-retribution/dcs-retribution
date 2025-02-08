from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSlider, QSpinBox, QComboBox
from dcs.weather import CloudPreset

from game.weather.clouds import Clouds


class DcsCloudThicknessSelector(QHBoxLayout):
    M2FT_FACTOR = 3.2808399

    def __init__(self, clouds: Optional[Clouds]) -> None:
        super().__init__()
        self.unit_changing = False

        self.label = QLabel("Thickness : ")
        self.addWidget(self.label)

        self.thickness = QSlider(Qt.Orientation.Horizontal)
        self.thickness.setRange(200, 2000)
        if clouds:
            self.thickness.setValue(clouds.thickness)
        self.thickness.valueChanged.connect(self.on_slider_change)
        self.addWidget(self.thickness, 1)

        self.thickness_spinner = QSpinBox()
        self.thickness_spinner.setValue(self.thickness.value())
        self.thickness_spinner.setFixedWidth(75)
        self.thickness_spinner.setSingleStep(100)
        self.thickness_spinner.valueChanged.connect(self.update_slider)
        self.addWidget(self.thickness_spinner, 1)

        self.unit = QComboBox()
        self.unit.insertItems(0, ["m", "ft"])
        self.unit.currentIndexChanged.connect(self.on_unit_change)
        self.unit.setCurrentIndex(1)
        self.addWidget(self.unit)

    def update_ui(self, preset: Optional[CloudPreset]) -> None:
        self.label.setVisible(preset is None)
        self.thickness.setVisible(preset is None)
        self.thickness_spinner.setVisible(preset is None)
        self.unit.setVisible(preset is None)

        if preset:
            self.thickness.setValue(0)

    def on_slider_change(self, value: int) -> None:
        if self.unit.currentIndex() == 0:
            self.thickness_spinner.setValue(value)
        elif self.unit.currentIndex() == 1 and not self.unit_changing:
            self.thickness_spinner.setValue(self.m2ft(value))

    def update_slider(self, value: int) -> None:
        if self.unit_changing:
            return
        if self.unit.currentIndex() == 0:
            self.thickness.setValue(value)
        elif self.unit.currentIndex() == 1:
            self.unit_changing = True
            self.thickness.setValue(self.ft2m(value))
            self.unit_changing = False

    def on_unit_change(self, index: int) -> None:
        self.unit_changing = True
        mini = (
            self.thickness.minimum()
            if index == 0
            else self.m2ft(self.thickness.minimum())
        )
        maxi = (
            self.thickness.maximum()
            if index == 0
            else self.m2ft(self.thickness.maximum())
        )
        value = (
            self.thickness.value() if index == 0 else self.m2ft(self.thickness.value())
        )
        self.thickness_spinner.setRange(mini, maxi)
        self.thickness_spinner.setValue(value)
        self.unit_changing = False

    def m2ft(self, value: int) -> int:
        return round(value * self.M2FT_FACTOR)

    def ft2m(self, value: int) -> int:
        return round(value / self.M2FT_FACTOR)
