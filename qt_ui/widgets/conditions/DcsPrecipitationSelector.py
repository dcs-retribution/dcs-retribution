from typing import Optional

from PySide6.QtWidgets import QHBoxLayout, QLabel, QComboBox
from dcs.weather import Weather as PydcsWeather, CloudPreset

from game.weather.clouds import Clouds


class DcsPrecipitationSelector(QHBoxLayout):
    def __init__(self, clouds: Clouds) -> None:
        super().__init__()
        self.unit_changing = False

        self.label = QLabel("Precipitation : ")
        self.addWidget(self.label)

        self.selector = QComboBox()
        for p in PydcsWeather.Preceptions:
            self.selector.addItem(p.name.replace("_", ""), p)

        self.selector.setCurrentText(clouds.precipitation.name.replace("_", ""))
        self.addWidget(self.selector, 1)

    def update_ui(self, preset: Optional[CloudPreset]) -> None:
        self.selector.setEnabled(preset is None)

        if preset:
            self.selector.setCurrentText("None")
