from collections import defaultdict

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QGroupBox,
    QLabel,
    QVBoxLayout,
    QScrollArea,
    QWidget,
)

from game.theater import ControlPoint, ParkingType


class QIntelInfo(QFrame):
    def __init__(self, cp: ControlPoint):
        super(QIntelInfo, self).__init__()
        self.cp = cp

        layout = QVBoxLayout()
        scroll_content = QWidget()
        intel_layout = QVBoxLayout()

        units_by_task: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        parking_type = ParkingType(
            fixed_wing=True, fixed_wing_stol=True, rotary_wing=True
        )
        for unit_type, count in self.cp.allocated_aircraft(
            parking_type
        ).present.items():
            if count:
                task_type = unit_type.dcs_unit_type.task_default.name
                units_by_task[task_type][unit_type.display_name] += count

        units_by_task = {
            task: units_by_task[task] for task in sorted(units_by_task.keys())
        }

        front_line_units = defaultdict(int)
        for unit_type, count in self.cp.base.armor.items():
            if count:
                front_line_units[unit_type.display_name] += count

        units_by_task["Front line units"] = front_line_units
        for task, unit_types in units_by_task.items():
            task_group = QGroupBox(task)
            task_layout = QGridLayout()
            task_group.setLayout(task_layout)

            for row, (name, count) in enumerate(unit_types.items()):
                task_layout.addWidget(QLabel(f"<b>{name}</b>"), row, 0)
                task_layout.addWidget(QLabel(str(count)), row, 1)

            intel_layout.addWidget(task_group)

        scroll_content.setLayout(intel_layout)
        scroll = QScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_content)

        layout.addWidget(scroll)

        self.setLayout(layout)
