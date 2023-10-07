import logging
from copy import deepcopy
from typing import Callable, Iterator, Optional, Type

from PySide6.QtCore import QItemSelection, QItemSelectionModel, QModelIndex, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QListView,
    QPushButton,
    QVBoxLayout,
    QInputDialog,
    QLineEdit,
    QMessageBox,
)
from dcs.unittype import FlyingType

from game.ato.flightplans.custom import CustomFlightPlan
from game.ato.flighttype import FlightType
from game.ato.flightwaypointtype import FlightWaypointType
from game.dcs.aircrafttype import AircraftType
from game.server import EventStream
from game.sim import GameUpdateEvents
from game.squadrons import Pilot, Squadron
from game.theater import ConflictTheater, ControlPoint, ParkingType
from qt_ui.delegates import TwoColumnRowDelegate
from qt_ui.errorreporter import report_errors
from qt_ui.models import AtoModel, SquadronModel
from qt_ui.simcontroller import SimController
from qt_ui.widgets.combos.QSquadronLiverySelector import SquadronLiverySelector
from qt_ui.widgets.combos.primarytaskselector import PrimaryTaskSelector


class PilotDelegate(TwoColumnRowDelegate):
    def __init__(self, squadron_model: SquadronModel) -> None:
        super().__init__(rows=2, columns=2, font_size=12)
        self.squadron_model = squadron_model

    @staticmethod
    def pilot(index: QModelIndex) -> Pilot:
        return index.data(SquadronModel.PilotRole)

    def text_for(self, index: QModelIndex, row: int, column: int) -> str:
        pilot = self.pilot(index)
        if (row, column) == (0, 0):
            return self.squadron_model.data(index, Qt.DisplayRole)
        elif (row, column) == (0, 1):
            flown = pilot.record.missions_flown
            missions = "missions" if flown != 1 else "mission"
            return f"{flown} {missions} flown"
        elif (row, column) == (1, 0):
            return "Player" if pilot.player else "AI"
        elif (row, column) == (1, 1):
            return pilot.status.value
        return ""


class PilotList(QListView):
    """List view for displaying a squadron's pilots."""

    def __init__(self, squadron_model: SquadronModel) -> None:
        super().__init__()
        self.squadron_model = squadron_model

        self.setItemDelegate(PilotDelegate(self.squadron_model))
        self.setModel(self.squadron_model)
        self.selectionModel().setCurrentIndex(
            self.squadron_model.index(0, 0, QModelIndex()), QItemSelectionModel.Select
        )

        # self.setIconSize(QSize(91, 24))
        self.setSelectionBehavior(QAbstractItemView.SelectItems)


class AutoAssignedTaskControls(QVBoxLayout):
    def __init__(self, squadron_model: SquadronModel) -> None:
        super().__init__()
        self.squadron_model = squadron_model

        self.addWidget(QLabel("Auto-assignable mission types"))

        def make_callback(toggled_task: FlightType) -> Callable[[bool], None]:
            def callback(checked: bool) -> None:
                self.on_toggled(toggled_task, checked)

            return callback

        for task in FlightType:
            if self.squadron_model.squadron.capable_of(task):
                checkbox = QCheckBox(text=task.value)
                checkbox.setChecked(squadron_model.is_auto_assignable(task))
                checkbox.toggled.connect(make_callback(task))
                self.addWidget(checkbox)

        self.addStretch()

    def on_toggled(self, task: FlightType, checked: bool) -> None:
        self.squadron_model.set_auto_assignable(task, checked)


class SquadronDestinationComboBox(QComboBox):
    def __init__(self, squadron: Squadron, theater: ConflictTheater) -> None:
        super().__init__()
        self.squadron = squadron
        self.theater = theater

        parking_type = ParkingType().from_squadron(squadron)
        room = squadron.location.unclaimed_parking(parking_type)
        self.addItem(
            f"Remain at {squadron.location} (room for {room} more aircraft)",
            squadron.location,
        )
        selected_index: Optional[int] = None
        for idx, destination in enumerate(sorted(self.iter_destinations(), key=str), 1):
            if destination == squadron.destination:
                selected_index = idx
            room = self.calculate_parking_slots(
                destination, squadron.aircraft.dcs_unit_type
            )
            self.addItem(
                f"Transfer to {destination} (room for {room} more aircraft)",
                destination,
            )
            if room < squadron.owned_aircraft or room == 0:
                diff = squadron.owned_aircraft - room
                text = (
                    f"Transfer to {destination} not possible "
                    f"({diff} additional slots required)"
                )
                if squadron.owned_aircraft == 0 and room == 0:
                    text = (
                        f"Transfer to {destination} not possible "
                        f"(no fitting slots found)"
                    )
                self.setItemText(idx, text)
                self.model().item(idx).setEnabled(False)

        if squadron.destination is None:
            selected_index = 0

        if selected_index is not None:
            self.setCurrentIndex(selected_index)

    def iter_destinations(self) -> Iterator[ControlPoint]:
        size = self.squadron.expected_size_next_turn
        parking_type = ParkingType().from_squadron(self.squadron)
        for control_point in self.theater.control_points_for(self.squadron.player):
            if control_point == self.squadron.location:
                continue
            if not control_point.can_operate(self.squadron.aircraft):
                continue
            ac_type = self.squadron.aircraft.dcs_unit_type
            if (
                self.squadron.destination is not control_point
                and control_point.unclaimed_parking(parking_type) < size
                and self.calculate_parking_slots(control_point, ac_type) < size
            ):
                continue
            yield control_point

    @staticmethod
    def calculate_parking_slots(
        cp: ControlPoint, dcs_unit_type: Type[FlyingType]
    ) -> int:
        if cp.dcs_airport:
            ap = deepcopy(cp.dcs_airport)
            overflow = []

            parking_type = ParkingType(
                fixed_wing=False, fixed_wing_stol=False, rotary_wing=True
            )
            free_helicopter_slots = cp.total_aircraft_parking(parking_type)

            parking_type = ParkingType(
                fixed_wing=False, fixed_wing_stol=True, rotary_wing=False
            )
            free_ground_spawns = cp.total_aircraft_parking(parking_type)

            for s in cp.squadrons:
                for count in range(s.owned_aircraft):
                    is_heli = s.aircraft.helicopter
                    is_vtol = not is_heli and s.aircraft.lha_capable
                    count_ground_spawns = (
                        s.aircraft.flyable
                        or cp.coalition.game.settings.ground_start_ai_planes
                    )

                    if free_helicopter_slots > 0 and (is_heli or is_vtol):
                        free_helicopter_slots = -1
                    elif free_ground_spawns > 0 and (
                        is_heli or is_vtol or count_ground_spawns
                    ):
                        free_ground_spawns = -1
                    else:
                        slot = ap.free_parking_slot(s.aircraft.dcs_unit_type)
                        if slot:
                            slot.unit_id = id(s) + count
                        else:
                            overflow.append(s)
                            break
            if overflow:
                overflow_msg = ""
                for s in overflow:
                    overflow_msg += f"{s.name} - {s.aircraft.variant_id}<br/>"
                QMessageBox.warning(
                    None,
                    "Insufficient parking space detected!",
                    f"Insufficient parking space was detected at {cp.name}:<br/><br/>"
                    f"{overflow_msg}<br/>"
                    f"Consider moving these squadrons to different airfield "
                    "to avoid possible air-starts.",
                )
            return len(ap.free_parking_slots(dcs_unit_type))
        else:
            parking_type = ParkingType().from_aircraft(
                next(AircraftType.for_dcs_type(dcs_unit_type)),
                cp.coalition.game.settings.ground_start_ai_planes,
            )
            return cp.unclaimed_parking(parking_type)


class SquadronDialog(QDialog):
    """Dialog window showing a squadron."""

    def __init__(
        self,
        ato_model: AtoModel,
        squadron_model: SquadronModel,
        theater: ConflictTheater,
        sim_controller: SimController,
        parent,
    ) -> None:
        super().__init__(parent)
        self.ato_model = ato_model
        self.squadron_model = squadron_model
        self.sim_controller = sim_controller

        self.setMinimumSize(1000, 440)
        self.setWindowTitle(str(squadron_model.squadron))
        # TODO: self.setWindowIcon()

        layout = QVBoxLayout()
        self.setLayout(layout)

        columns = QHBoxLayout()
        layout.addLayout(columns)

        left_column = QVBoxLayout()
        columns.addLayout(left_column)

        left_column.addWidget(QLabel("Primary task"))
        self.primary_task_selector = PrimaryTaskSelector.for_squadron(
            self.squadron_model.squadron
        )
        self.primary_task_selector.currentIndexChanged.connect(
            self.on_task_index_changed
        )
        left_column.addWidget(self.primary_task_selector)

        left_column.addWidget(QLabel("Livery"))
        self.livery_selector = SquadronLiverySelector(self.squadron_model.squadron)
        self.livery_selector.currentIndexChanged.connect(self.on_livery_changed)
        left_column.addWidget(self.livery_selector)

        auto_assigned_tasks = AutoAssignedTaskControls(squadron_model)
        left_column.addLayout(auto_assigned_tasks)

        self.pilot_list = PilotList(squadron_model)
        self.pilot_list.selectionModel().selectionChanged.connect(
            self.on_selection_changed
        )
        columns.addWidget(self.pilot_list)

        button_panel = QHBoxLayout()

        self.transfer_destination = SquadronDestinationComboBox(
            squadron_model.squadron, theater
        )
        self.transfer_destination.currentIndexChanged.connect(
            self.on_destination_changed
        )
        button_panel.addWidget(self.transfer_destination)

        button_panel.addStretch()
        layout.addLayout(button_panel)

        self.rename_button = QPushButton("Rename pilot")
        self.rename_button.setProperty("style", "start-button")
        self.rename_button.clicked.connect(self.rename_pilot)
        button_panel.addWidget(self.rename_button, alignment=Qt.AlignRight)

        self.toggle_ai_button = QPushButton()
        self.reset_ai_toggle_state(self.pilot_list.currentIndex())
        self.toggle_ai_button.setProperty("style", "start-button")
        self.toggle_ai_button.clicked.connect(self.toggle_ai)
        button_panel.addWidget(self.toggle_ai_button, alignment=Qt.AlignRight)

        self.toggle_leave_button = QPushButton()
        self.reset_leave_toggle_state(self.pilot_list.currentIndex())
        self.toggle_leave_button.setProperty("style", "start-button")
        self.toggle_leave_button.clicked.connect(self.toggle_leave)
        button_panel.addWidget(self.toggle_leave_button, alignment=Qt.AlignRight)

    @property
    def squadron(self) -> Squadron:
        return self.squadron_model.squadron

    def _instant_relocate(self, destination: ControlPoint) -> None:
        self.squadron.relocate_to(destination)
        for _, f in self.squadron.flight_db.objects.items():
            if f.squadron == self.squadron:
                if isinstance(f.flight_plan, CustomFlightPlan):
                    for wpt in f.flight_plan.waypoints:
                        if wpt.waypoint_type == FlightWaypointType.LANDING_POINT:
                            wpt.control_point = destination
                            wpt.position = wpt.control_point.position
                            break
                f.recreate_flight_plan()
                EventStream.put_nowait(GameUpdateEvents().update_flight(f))

    def on_destination_changed(self, index: int) -> None:
        with report_errors("Could not change squadron destination", self):
            destination = self.transfer_destination.itemData(index)
            if destination is self.squadron.location:
                self.squadron.cancel_relocation()
            elif self.ato_model.game.settings.enable_transfer_cheat:
                self._instant_relocate(destination)
            else:
                self.squadron.plan_relocation(
                    destination, self.sim_controller.current_time_in_sim
                )
            self.ato_model.replace_from_game(player=True)

    def check_disabled_button_states(
        self, button: QPushButton, index: QModelIndex
    ) -> bool:
        if not index.isValid():
            button.setText("No pilot selected")
            button.setDisabled(True)
            return True
        pilot = self.squadron_model.pilot_at_index(index)
        if not pilot.alive:
            button.setText("Pilot is dead")
            button.setDisabled(True)
            return True
        return False

    def rename_pilot(self) -> None:
        index = self.pilot_list.currentIndex()
        if not index.isValid():
            logging.error("Cannot toggle player/AI: no pilot is selected")
            return
        p = self.squadron_model.pilot_at_index(index)
        text, ok = QInputDialog.getText(
            self, "Rename pilot", "New name: ", QLineEdit.EchoMode.Normal
        )
        if ok:
            p.name = text

    def toggle_ai(self) -> None:
        index = self.pilot_list.currentIndex()
        if not index.isValid():
            logging.error("Cannot toggle player/AI: no pilot is selected")
            return
        self.squadron_model.toggle_ai_state(index)

    def reset_ai_toggle_state(self, index: QModelIndex) -> None:
        if self.check_disabled_button_states(self.toggle_ai_button, index):
            return
        if not self.squadron_model.squadron.aircraft.flyable:
            self.toggle_ai_button.setText("Not flyable")
            self.toggle_ai_button.setDisabled(True)
            return
        self.toggle_ai_button.setEnabled(True)
        pilot = self.squadron_model.pilot_at_index(index)
        self.toggle_ai_button.setText(
            "Convert to AI" if pilot.player else "Convert to player"
        )

    def toggle_leave(self) -> None:
        index = self.pilot_list.currentIndex()
        if not index.isValid():
            logging.error("Cannot toggle on leave state: no pilot is selected")
            return
        self.squadron_model.toggle_leave_state(index)

    def reset_leave_toggle_state(self, index: QModelIndex) -> None:
        if self.check_disabled_button_states(self.toggle_leave_button, index):
            return
        pilot = self.squadron_model.pilot_at_index(index)
        self.toggle_leave_button.setEnabled(
            not pilot.on_leave or self.squadron_model.squadron.has_unfilled_pilot_slots
        )
        self.toggle_leave_button.setText(
            "Return from leave" if pilot.on_leave else "Send on leave"
        )

    def on_selection_changed(
        self, selected: QItemSelection, _deselected: QItemSelection
    ) -> None:
        index = selected.indexes()[0]
        self.reset_ai_toggle_state(index)
        self.reset_leave_toggle_state(index)

    def on_task_index_changed(self, index: int) -> None:
        task = self.primary_task_selector.itemData(index)
        if task is None:
            raise RuntimeError("Selected task cannot be None")
        self.squadron.primary_task = task

    def on_livery_changed(self) -> None:
        self.squadron.livery = self.livery_selector.currentData()
