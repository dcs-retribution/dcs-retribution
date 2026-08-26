from functools import partial
from typing import Set

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from game.ato.flighttype import FlightType
from game.dcs.aircrafttype import AircraftType
from game.purchaseadapter import AircraftPurchaseAdapter
from game.squadrons import Squadron
from game.squadrons.intercept_reserve import max_intercept_reserve
from game.theater import ControlPoint, ParkingType
from qt_ui.models import GameModel
from qt_ui.uiconstants import ICONS
from qt_ui.windows.basemenu.UnitTransactionFrame import UnitTransactionFrame


class QAircraftRecruitmentMenu(UnitTransactionFrame[Squadron]):
    def __init__(self, cp: ControlPoint, game_model: GameModel) -> None:
        super().__init__(game_model, AircraftPurchaseAdapter(cp))
        self.cp = cp
        self.game_model = game_model
        self.purchase_groups = {}
        self.bought_amount_labels = {}
        self.existing_units_labels = {}

        self.bought_amount_labels = {}
        self.existing_units_labels = {}

        self.hangar_status = QHangarStatus(game_model, self.cp)

        main_layout = QVBoxLayout()

        scroll_content = QWidget()
        task_box_layout = QGridLayout()
        row = 0

        unit_types: Set[AircraftType] = set()

        for squadron in cp.squadrons:
            unit_types.add(squadron.aircraft)

        sorted_squadrons = sorted(
            cp.squadrons, key=lambda s: (s.aircraft.display_name, s.name)
        )
        for row, squadron in enumerate(sorted_squadrons):
            self.add_purchase_row(squadron, task_box_layout, row)
            task_box_layout.addLayout(self._qra_control(squadron), row, 4)

        stretch = QVBoxLayout()
        stretch.addStretch()
        task_box_layout.addLayout(stretch, row, 0)

        scroll_content.setLayout(task_box_layout)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_content)
        main_layout.addLayout(self.hangar_status)
        main_layout.addWidget(scroll)

        incoming = sorted(
            (s for s in cp.coalition.air_wing.iter_squadrons() if s.destination == cp),
            key=lambda s: (s.aircraft.display_name, s.name),
        )
        if incoming:
            transfer_box = QGroupBox("Units transferring here in the next turn")
            transfer_layout = QVBoxLayout()
            for s in incoming:
                transfer_layout.addWidget(
                    QLabel(
                        f"{s.name} ({s.aircraft.display_name}) - "
                        f"{s.owned_aircraft} aircraft from {s.location.name}"
                    )
                )
            transfer_box.setLayout(transfer_layout)
            main_layout.addWidget(transfer_box)

        self.setLayout(main_layout)

    def _qra_control(self, squadron: Squadron) -> QVBoxLayout:
        layout = QVBoxLayout()
        label = QLabel("QRA")
        label.setToolTip(
            "Aircraft held on quick-reaction alert; scramble airborne to intercept."
        )
        layout.addWidget(label)
        spinner = QSpinBox()
        spinner.lineEdit().setEnabled(False)
        spinner.setMinimum(0)
        # Cap at unplanned airframes (owned - tasked = untasked + reserve); aircraft
        # already tasked to flights this turn cannot be pulled onto QRA.
        spinner.setMaximum(
            max_intercept_reserve(
                squadron.untasked_aircraft,
                squadron.intercept_reserve,
                squadron.max_size,
            )
        )
        spinner.setValue(squadron.intercept_reserve)
        # Carry the descriptive tooltip on the spinner too (matching the other QRA
        # dialogs); the non-BARCAP branch below overrides it with its own.
        spinner.setToolTip(
            "Aircraft held on quick-reaction alert; scramble airborne to intercept."
        )
        if not squadron.capable_of(FlightType.BARCAP):
            spinner.setEnabled(False)
            spinner.setToolTip(
                "QRA is only available for fixed-wing squadrons capable of BARCAP."
            )
        spinner.valueChanged.connect(partial(self._set_reserve, squadron))
        layout.addWidget(spinner)
        return layout

    @staticmethod
    def _set_reserve(squadron: Squadron, value: int) -> None:
        # Route through set_intercept_reserve so untasked_aircraft (the planner's
        # pool) updates immediately, instead of going stale until turn advance.
        squadron.set_intercept_reserve(value)

    def sell_tooltip(self, is_enabled: bool) -> str:
        if is_enabled:
            return "Sell unit. Use Shift or Ctrl key to sell multiple units at once."
        else:
            return (
                "Can not be sold because either no aircraft are available or are "
                "already assigned to a mission."
            )

    def post_transaction_update(self) -> None:
        super().post_transaction_update()
        self.hangar_status.update_label()


class QHangarStatus(QHBoxLayout):
    def __init__(self, game_model: GameModel, control_point: ControlPoint) -> None:
        super().__init__()
        self.game_model = game_model
        self.control_point = control_point

        self.icon = QLabel()
        self.icon.setPixmap(ICONS["Hangar"])
        self.text = QLabel("")

        self.update_label()
        self.addWidget(self.icon, Qt.AlignmentFlag.AlignLeft)
        self.addWidget(self.text, Qt.AlignmentFlag.AlignLeft)
        self.addStretch(50)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def update_label(self) -> None:
        parking_type = ParkingType(
            fixed_wing=True, fixed_wing_stol=True, rotary_wing=True
        )

        next_turn = self.control_point.allocated_aircraft(parking_type)
        max_amount = self.control_point.total_aircraft_parking(parking_type)

        components = [f"{next_turn.total_present} present"]
        if next_turn.total_ordered > 0:
            components.append(f"{next_turn.total_ordered} purchased")
        elif next_turn.total_ordered < 0:
            components.append(f"{-next_turn.total_ordered} sold")

        transferring = next_turn.total_transferring
        if transferring > 0:
            components.append(f"{transferring} transferring in")
        if transferring < 0:
            components.append(f"{-transferring} transferring out")

        details = ", ".join(components)
        self.text.setText(
            f"<strong>{next_turn.total}/{max_amount}</strong> ({details})"
        )
