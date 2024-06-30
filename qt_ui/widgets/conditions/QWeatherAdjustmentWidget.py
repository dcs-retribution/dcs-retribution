from PySide6.QtWidgets import QLabel, QHBoxLayout, QComboBox, QWidget, QVBoxLayout
from dcs.cloud_presets import CLOUD_PRESETS

from game.weather.weather import ClearSkies, Cloudy, Raining, Thunderstorm
from qt_ui.widgets.conditions.DcsCloudBaseSelector import DcsCloudBaseSelector
from qt_ui.widgets.conditions.DcsCloudDensitySelector import DcsCloudDensitySelector
from qt_ui.widgets.conditions.DcsCloudThicknessSelector import DcsCloudThicknessSelector
from qt_ui.widgets.conditions.DcsPrecipitationSelector import DcsPrecipitationSelector
from qt_ui.widgets.conditions.QWeatherWidget import QWeatherWidget


class QWeatherAdjustmentWidget(QWidget):
    def __init__(self, weather: QWeatherWidget) -> None:
        super().__init__()
        self.weather = weather
        self.init_ui()

    def init_ui(self) -> None:
        weather = self.weather.conditions.weather

        vbox = QVBoxLayout()
        label = QLabel("<h2><b>Weather:</b></h2>")
        label.setMaximumHeight(75)
        vbox.addWidget(label)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Type"))
        self.type_selector = QComboBox()
        for text, w_type in [
            ("Clear", ClearSkies),
            ("Clouds", Cloudy),
            ("Rain", Raining),
            ("Thunderstorm", Thunderstorm),
        ]:
            self.type_selector.addItem(text, w_type)
            if isinstance(weather, w_type):
                self.type_selector.setCurrentText(text)
        self.type_selector.currentIndexChanged.connect(self.update_ui_for_type)
        hbox.addWidget(self.type_selector)
        vbox.addLayout(hbox)

        label = QLabel("<h3><b>Clouds:</b></h3>")
        label.setMaximumHeight(50)
        vbox.addWidget(label)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Preset"))
        self.preset_selector = QComboBox()
        for _, preset in CLOUD_PRESETS.items():
            self.preset_selector.addItem(preset.value.ui_name, preset.value)
        self.preset_selector.addItem("Custom", None)
        self.preset_selector.setCurrentText(
            weather.clouds.preset.ui_name
            if weather.clouds and weather.clouds.preset
            else "Custom"
        )
        self.preset_selector.currentIndexChanged.connect(self.update_ui)
        hbox.addWidget(self.preset_selector)
        vbox.addLayout(hbox)

        self.cloud_base = DcsCloudBaseSelector(self.preset_selector.currentData())
        vbox.addLayout(self.cloud_base)

        clouds = self.weather.conditions.weather.clouds

        self.cloud_thickness = DcsCloudThicknessSelector(clouds)
        vbox.addLayout(self.cloud_thickness)

        self.cloud_density = DcsCloudDensitySelector(clouds)
        vbox.addLayout(self.cloud_density)

        self.precipitation = DcsPrecipitationSelector(clouds)
        vbox.addLayout(self.precipitation)

        self.setLayout(vbox)

        self.update_ui_for_type()

    def update_ui_for_type(self) -> None:
        if self.type_selector.currentData() in [ClearSkies, Thunderstorm]:
            self.preset_selector.setCurrentText("Custom")
            self.preset_selector.setDisabled(True)
        else:
            self.preset_selector.setDisabled(False)

        self.update_ui()

    def update_ui(self) -> None:
        preset = self.preset_selector.currentData()
        self.cloud_base.preset = preset
        self.cloud_base.update_bounds()
        self.cloud_thickness.update_ui(preset)
        self.cloud_density.update_ui(preset)
        self.precipitation.update_ui(preset)
