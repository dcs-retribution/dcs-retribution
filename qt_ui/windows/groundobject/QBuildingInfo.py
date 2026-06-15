import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGroupBox, QLabel, QVBoxLayout

from game.config import REWARDS
from game.theater import TheaterUnit


class QBuildingInfo(QGroupBox):
    def __init__(self, building: TheaterUnit, ground_object):
        super(QBuildingInfo, self).__init__()
        self.building = building
        self.ground_object = ground_object
        self.init_ui()

    def init_ui(self):
        icon_path = os.path.join(
            "./resources/ui/units/buildings/" + self.building.icon + ".png"
        )
        has_real_icon = self.building.icon != "missing" and os.path.isfile(icon_path)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        if not self.building.alive:
            header = QLabel()
            header.setPixmap(QPixmap("./resources/ui/units/buildings/dead.png"))
            layout.addWidget(header)
        elif has_real_icon:
            header = QLabel()
            header.setPixmap(QPixmap(icon_path))
            layout.addWidget(header)

        name_label = QLabel(self.building.short_name)
        name_label.setProperty("style", "small")
        name_label.setWordWrap(True)
        layout.addWidget(name_label)

        if self.ground_object.category in REWARDS:
            income_text = "Value: " + str(REWARDS[self.ground_object.category]) + "M"
            if not self.building.alive:
                income_text = "<s>" + income_text + "</s>"
            layout.addWidget(QLabel(income_text))

        self.setLayout(layout)
