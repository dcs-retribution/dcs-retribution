import logging
from typing import Callable, Dict, TypeVar

from PySide6.QtGui import QIcon, QPixmap, QCloseEvent
from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from game.debriefing import Debriefing
from game.theater import Player
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal

T = TypeVar("T")


class LossGrid(QGridLayout):
    def __init__(self, debriefing: Debriefing, player: Player) -> None:
        super().__init__()

        self.add_loss_rows(
            debriefing.air_losses.by_type(player), lambda u: u.display_name
        )
        self.add_loss_rows(
            debriefing.front_line_losses_by_type(player), lambda u: str(u)
        )
        self.add_loss_rows(
            debriefing.convoy_losses_by_type(player), lambda u: f"{u} from convoy"
        )
        self.add_loss_rows(
            debriefing.cargo_ship_losses_by_type(player),
            lambda u: f"{u} from cargo ship",
        )
        self.add_loss_rows(
            debriefing.airlift_losses_by_type(player), lambda u: f"{u} from airlift"
        )
        self.add_loss_rows(debriefing.ground_object_losses_by_type(player), lambda u: u)
        self.add_loss_rows(debriefing.scenery_losses_by_type(player), lambda u: u)

        # TODO: Display dead ground object units and runways.

    def add_loss_rows(self, losses: Dict[T, int], make_name: Callable[[T], str]):
        for unit_type, count in losses.items():
            row = self.rowCount()
            try:
                name = make_name(unit_type)
            except AttributeError:
                logging.exception(f"Could not make unit name for {unit_type}")
                name = unit_type.id
            self.addWidget(QLabel(name), row, 0)
            self.addWidget(QLabel(str(count)), row, 1)


class ScrollingCasualtyReportContainer(QGroupBox):
    def __init__(self, debriefing: Debriefing, player: Player) -> None:
        country = (
            debriefing.player_country if player.is_blue else debriefing.enemy_country
        )
        super().__init__(f"{country}'s lost units:")
        scroll_content = QWidget()
        scroll_content.setLayout(LossGrid(debriefing, player))
        scroll_area = QScrollArea()
        scroll_area.setWidget(scroll_content)
        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)


class MissionImpactGrid(QGridLayout):
    def __init__(self, debriefing: Debriefing) -> None:
        super().__init__()
        for row, (label, value) in enumerate(self._rows_for(debriefing)):
            self.addWidget(QLabel(f"<b>{label}</b>"), row, 0)
            self.addWidget(QLabel(value), row, 1)

    @staticmethod
    def _rows_for(debriefing: Debriefing) -> list[tuple[str, str]]:
        blue_losses = debriefing.loss_counts(Player.BLUE)
        red_losses = debriefing.loss_counts(Player.RED)
        captured = [
            capture.control_point.name
            for capture in debriefing.base_captures
            if capture.captured_by_player.is_blue
        ]
        lost = [
            capture.control_point.name
            for capture in debriefing.base_captures
            if capture.captured_by_player.is_red
        ]
        runways = [airfield.name for airfield in debriefing.damaged_runways]

        rows = [
            (
                "Mission status",
                (
                    "Mission ended normally"
                    if debriefing.state_data.mission_ended
                    else "Mission ended early or state data was incomplete"
                ),
            ),
            (
                "Bases captured",
                ", ".join(captured) if captured else "None",
            ),
            (
                "Bases lost",
                ", ".join(lost) if lost else "None",
            ),
            (
                "Runways damaged",
                ", ".join(runways) if runways else "None",
            ),
            (
                f"{debriefing.player_country} losses",
                f"{blue_losses.aircraft} aircraft, {blue_losses.front_line} front-line "
                f"units, {blue_losses.ground_objects} site units, {blue_losses.bases_lost} bases",
            ),
            (
                f"{debriefing.enemy_country} losses",
                f"{red_losses.aircraft} aircraft, {red_losses.front_line} front-line "
                f"units, {red_losses.ground_objects} site units, {red_losses.bases_lost} bases",
            ),
        ]
        return rows


class MissionImpactContainer(QGroupBox):
    def __init__(self, debriefing: Debriefing) -> None:
        super().__init__("Mission Impact")
        layout = QVBoxLayout()
        layout.addLayout(MissionImpactGrid(debriefing))
        self.setLayout(layout)


class QDebriefingWindow(QDialog):
    def __init__(self, debriefing: Debriefing):
        super(QDebriefingWindow, self).__init__()
        self.debriefing = debriefing

        self.setModal(True)
        self.setWindowTitle("Debriefing")
        self.setMinimumSize(300, 200)
        self.setWindowIcon(QIcon("./resources/icon.png"))

        layout = QVBoxLayout()
        self.setLayout(layout)

        header = QLabel(self)
        header.setGeometry(0, 0, 655, 106)
        pixmap = QPixmap("./resources/ui/debriefing.png")
        header.setPixmap(pixmap)
        layout.addWidget(header)

        title = QLabel("<b>Casualty report</b>")
        layout.addWidget(title)

        impact = MissionImpactContainer(debriefing)
        layout.addWidget(impact)

        player_lost_units = ScrollingCasualtyReportContainer(
            debriefing, player=Player.BLUE
        )
        layout.addWidget(player_lost_units)

        enemy_lost_units = ScrollingCasualtyReportContainer(
            debriefing, player=Player.RED
        )
        layout.addWidget(enemy_lost_units, 1)

        okay = QPushButton("Okay")
        okay.clicked.connect(self.close)
        layout.addWidget(okay)

    def closeEvent(self, event: QCloseEvent) -> None:
        super().closeEvent(event)
        state = self.debriefing.game.check_win_loss()
        GameUpdateSignal.get_instance().gameStateChanged(state)
