from copy import deepcopy
from datetime import datetime, timedelta

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton

from game.sim import GameUpdateEvents
from game.weather.clouds import Clouds
from qt_ui.widgets.conditions.QTimeAdjustmentWidget import QTimeAdjustmentWidget
from qt_ui.widgets.conditions.QTimeTurnWidget import QTimeTurnWidget
from qt_ui.widgets.conditions.QWeatherAdjustmentWidget import QWeatherAdjustmentWidget
from qt_ui.widgets.conditions.QWeatherWidget import QWeatherWidget


class QConditionsDialog(QDialog):
    def __init__(self, time_turn: QTimeTurnWidget, weather: QWeatherWidget):
        super().__init__()
        self.time_turn = time_turn
        self.weather = weather
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Time & Weather Conditions")
        self.setMinimumSize(360, 380)

        vbox = QVBoxLayout()

        self.time_adjuster = QTimeAdjustmentWidget(self.time_turn)
        vbox.addWidget(self.time_adjuster, 1)
        self.weather_adjuster = QWeatherAdjustmentWidget(self.weather)
        vbox.addWidget(self.weather_adjuster, 8)

        hbox = QHBoxLayout()
        reject_btn = QPushButton("REJECT")
        reject_btn.setProperty("style", "btn-danger")
        reject_btn.clicked.connect(self.close)
        hbox.addWidget(reject_btn)
        accept_btn = QPushButton("ACCEPT")
        accept_btn.setProperty("style", "btn-success")
        accept_btn.clicked.connect(self.apply_conditions)
        hbox.addWidget(accept_btn)
        vbox.addLayout(hbox, 1)

        self.setLayout(vbox)

    def apply_conditions(self) -> None:
        qdt: datetime = self.time_adjuster.datetime_edit.dateTime().toPython()

        sim = self.time_turn.sim_controller
        current_time = sim.current_time_in_sim_if_game_loaded
        if current_time:
            current_time = deepcopy(current_time)
        sim.game_loop.sim.time = qdt

        game = sim.game_loop.game
        game.date = qdt.date() - timedelta(days=game.turn // 4)
        game.conditions.start_time = qdt
        self.time_turn.set_current_turn(game.turn, game.conditions)

        # TODO: create new weather object

        new_weather_type = self.weather_adjuster.type_selector.currentData()
        new_weather = new_weather_type(
            seasonal_conditions=game.theater.seasonal_conditions,
            day=qdt.date(),
            time_of_day=game.current_turn_time_of_day,
        )

        # self.weather.conditions.weather = WeatherType()
        preset = self.weather_adjuster.preset_selector.currentData()
        new_weather.clouds = Clouds(
            base=self.weather_adjuster.cloud_base.base.value(),
            density=self.weather_adjuster.cloud_density.density.value(),
            thickness=self.weather_adjuster.cloud_thickness.thickness.value(),
            precipitation=self.weather_adjuster.precipitation.selector.currentData(),
            preset=preset,
        )

        self.weather.conditions.weather = new_weather

        self.weather.update_forecast()
        if game.turn > 0 and current_time != qdt:
            events = GameUpdateEvents()
            game.initialize_turn(events, for_blue=True, for_red=True)
            sim.sim_update.emit(events)
        self.accept()
