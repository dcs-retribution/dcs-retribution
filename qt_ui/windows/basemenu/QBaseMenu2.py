from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QGridLayout,
)

from game import Game
from game.ato.flighttype import FlightType
from game.config import RUNWAY_REPAIR_COST
from game.radio.ICLSContainer import ICLSContainer
from game.radio.RadioFrequencyContainer import RadioFrequencyContainer
from game.radio.TacanContainer import TacanContainer
from game.server import EventStream
from game.sim import GameUpdateEvents
from game.theater import (
    AMMO_DEPOT_FRONTLINE_UNIT_CONTRIBUTION,
    ControlPoint,
    ControlPointType,
    FREE_FRONTLINE_UNIT_SUPPLY,
    NavalControlPoint,
    ParkingType,
)
from qt_ui.dialogs import Dialog
from qt_ui.models import GameModel
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.widgets.QFrequencyWidget import QFrequencyWidget
from qt_ui.widgets.QICLSWidget import QICLSWidget
from qt_ui.widgets.QLink4Widget import QLink4Widget
from qt_ui.widgets.QTacanWidget import QTacanWidget
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.basemenu.NewUnitTransferDialog import NewUnitTransferDialog
from qt_ui.windows.basemenu.QBaseMenuTabs import QBaseMenuTabs
from qt_ui.windows.basemenu.UnitTransactionFrame import UnitTransactionFrame


class QBaseMenu2(QDialog):
    def __init__(self, parent, cp: ControlPoint, game_model: GameModel):
        super(QBaseMenu2, self).__init__(parent)

        # Attrs
        self.cp = cp
        self.game_model = game_model
        self.objectName = "menuDialogue"

        if self.cp.captured:
            self.deliveryEvent = None

        self.setWindowIcon(EVENT_ICONS["capture"])

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setMinimumSize(300, 200)
        self.setMinimumWidth(1024)
        self.setMaximumWidth(1024)
        self.setModal(True)

        self.setWindowTitle(self.cp.name)

        base_menu_header = QWidget()
        top_layout = QHBoxLayout()

        header = QLabel(self)
        header.setGeometry(0, 0, 655, 106)
        pixmap = QPixmap(self.get_base_image())
        header.setPixmap(pixmap)

        cp_settings = QGridLayout()
        top_layout.addLayout(cp_settings)

        title = QLabel("<b>" + self.cp.name + "</b>")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        title.setProperty("style", "base-title")
        cp_settings.addWidget(title, 0, 0, 1, 2)
        cp_settings.setHorizontalSpacing(20)

        counter = 2

        self.freq_widget = None
        self.link4_widget = None

        is_friendly = cp.is_friendly(True)
        if is_friendly and isinstance(cp, RadioFrequencyContainer):
            self.freq_widget = QFrequencyWidget(cp, self.game_model)
            cp_settings.addWidget(self.freq_widget, counter // 2, counter % 2)
            counter += 1

        if is_friendly and isinstance(cp, TacanContainer):
            self.tacan_widget = QTacanWidget(cp, self.game_model)
            cp_settings.addWidget(self.tacan_widget, counter // 2, counter % 2)
            counter += 1

        if is_friendly and isinstance(cp, ICLSContainer):
            self.icls_widget = QICLSWidget(cp, self.game_model)
            cp_settings.addWidget(self.icls_widget, counter // 2, counter % 2)
            counter += 1

        if is_friendly and isinstance(cp, NavalControlPoint):
            self.link4_widget = QLink4Widget(cp, self.game_model)
            cp_settings.addWidget(self.link4_widget, counter // 2, counter % 2)
            counter += 1

        if self.freq_widget and self.link4_widget:
            # link them so on change they check freq
            self.freq_widget.freq_changed.connect(self.link4_widget.check_freq)
            self.link4_widget.freq_changed.connect(self.freq_widget.check_freq)

        self.intel_summary = QLabel()
        self.intel_summary.setToolTip(self.generate_intel_tooltip())
        self.update_intel_summary()
        top_layout.addWidget(self.intel_summary)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        runway_buttons_layout = QVBoxLayout()
        top_layout.addLayout(runway_buttons_layout)

        if (
            self.cp.runway_is_destroyable
            and self.game_model.game.settings.enable_runway_state_cheat
        ):
            self.cheat_runway_state = QPushButton()
            self.update_cheat_runway_state_text()
            self.cheat_runway_state.clicked.connect(self.on_cheat_runway_state)
            runway_buttons_layout.addWidget(self.cheat_runway_state)

        self.repair_button = QPushButton()
        self.repair_button.clicked.connect(self.begin_runway_repair)
        self.update_repair_button()
        runway_buttons_layout.addWidget(self.repair_button)
        runway_buttons_layout.addStretch()

        base_menu_header.setProperty("style", "baseMenuHeader")
        base_menu_header.setLayout(top_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(header)
        main_layout.addWidget(base_menu_header)
        main_layout.addWidget(QBaseMenuTabs(cp, self.game_model))
        bottom_row = QHBoxLayout()
        main_layout.addLayout(bottom_row)

        if FlightType.OCA_RUNWAY in self.cp.mission_types(for_player=True):
            runway_attack_button = QPushButton("Attack airfield")
            bottom_row.addWidget(runway_attack_button)

            runway_attack_button.setProperty("style", "btn-danger")
            runway_attack_button.clicked.connect(self.new_package)

        if self.cp.captured and self.has_transfer_destinations:
            transfer_button = QPushButton("Transfer Units")
            transfer_button.setProperty("style", "btn-success")
            bottom_row.addWidget(transfer_button)
            transfer_button.clicked.connect(self.open_transfer_dialog)

        if self.cheat_capturable:
            capture_button = QPushButton("CHEAT: Capture")
            capture_button.setProperty("style", "btn-danger")
            bottom_row.addWidget(capture_button)
            capture_button.clicked.connect(self.cheat_capture)

        self.budget_display = QLabel(
            UnitTransactionFrame.BUDGET_FORMAT.format(self.game_model.game.blue.budget)
        )
        self.budget_display.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom
        )
        self.budget_display.setProperty("style", "budget-label")
        bottom_row.addWidget(self.budget_display)
        GameUpdateSignal.get_instance().budgetupdated.connect(self.update_budget)
        self.setLayout(main_layout)

    @property
    def cheat_capturable(self) -> bool:
        return self.game_model.game.settings.enable_base_capture_cheat

    def cheat_capture(self) -> None:
        events = GameUpdateEvents()
        self.cp.capture(self.game_model.game, events, for_player=not self.cp.captured)
        # Reinitialized ground planners and the like. The ATO needs to be reset because
        # missions planned against the flipped base are no longer valid.
        self.game_model.game.initialize_turn(events)
        EventStream.put_nowait(events)
        GameUpdateSignal.get_instance().updateGame(self.game_model.game)
        state = self.game_model.game.check_win_loss()
        GameUpdateSignal.get_instance().gameStateChanged(state)
        self.close()

    @property
    def has_transfer_destinations(self) -> bool:
        return self.game_model.game.transit_network_for(
            self.cp.captured
        ).has_destinations(self.cp)

    def update_cheat_runway_state_text(self) -> None:
        if self.cp.runway_can_be_repaired:
            self.cheat_runway_state.setText("CHEAT: Repair runway")
        else:
            self.cheat_runway_state.setText("CHEAT: Destroy runway")

    def on_cheat_runway_state(self) -> None:
        if self.cp.runway_can_be_repaired:
            self.cp.runway_status.repair()
        else:
            self.cp.runway_status.damage()
        self.update_cheat_runway_state_text()
        self.update_repair_button()
        self.update_intel_summary()
        with EventStream.event_context() as events:
            events.update_control_point(self.cp)

    @property
    def can_repair_runway(self) -> bool:
        return self.cp.captured and self.cp.runway_can_be_repaired

    @property
    def can_afford_runway_repair(self) -> bool:
        return self.game_model.game.blue.budget >= RUNWAY_REPAIR_COST

    def begin_runway_repair(self) -> None:
        if not self.can_afford_runway_repair:
            QMessageBox.critical(
                self,
                "Cannot repair runway",
                f"Runway repair costs ${RUNWAY_REPAIR_COST}M but you have "
                f"only ${self.game_model.game.blue.budget}M available.",
                QMessageBox.StandardButton.Ok,
            )
            return
        if not self.can_repair_runway:
            QMessageBox.critical(
                self,
                "Cannot repair runway",
                f"Cannot repair this runway.",
                QMessageBox.StandardButton.Ok,
            )
            return

        self.cp.begin_runway_repair()
        self.game_model.game.blue.budget -= RUNWAY_REPAIR_COST
        self.update_repair_button()
        self.update_intel_summary()
        GameUpdateSignal.get_instance().updateGame(self.game_model.game)

    def update_repair_button(self) -> None:
        self.repair_button.setVisible(True)
        turns_remaining = self.cp.runway_status.repair_turns_remaining
        if self.cp.captured and turns_remaining is not None:
            self.repair_button.setText("Repairing...")
            self.repair_button.setDisabled(True)
            return

        if self.can_repair_runway:
            if self.can_afford_runway_repair:
                self.repair_button.setText(f"Repair ${RUNWAY_REPAIR_COST}M")
                self.repair_button.setDisabled(False)
                return
            else:
                self.repair_button.setText(
                    f"Cannot afford repair ${RUNWAY_REPAIR_COST}M"
                )
                self.repair_button.setDisabled(True)
                return

        self.repair_button.setVisible(False)
        self.repair_button.setDisabled(True)

    def update_intel_summary(self) -> None:
        parking_type_all = ParkingType(
            fixed_wing=True, fixed_wing_stol=True, rotary_wing=True
        )

        aircraft = self.cp.allocated_aircraft(parking_type_all).total_present
        parking = self.cp.total_aircraft_parking(parking_type_all)

        parking_type_fixed_wing = ParkingType(
            fixed_wing=True, fixed_wing_stol=False, rotary_wing=False
        )
        parking_type_stol = ParkingType(
            fixed_wing=False, fixed_wing_stol=True, rotary_wing=False
        )
        parking_type_rotary_wing = ParkingType(
            fixed_wing=False, fixed_wing_stol=False, rotary_wing=True
        )

        fixed_wing_parking = self.cp.total_aircraft_parking(parking_type_fixed_wing)
        ground_spawn_parking = self.cp.total_aircraft_parking(parking_type_stol)
        rotary_wing_parking = self.cp.total_aircraft_parking(parking_type_rotary_wing)
        ground_unit_limit = self.cp.frontline_unit_count_limit
        deployable_unit_info = ""

        allocated = self.cp.allocated_ground_units(
            self.game_model.game.coalition_for(self.cp.captured).transfers
        )
        unit_overage = max(
            allocated.total_present - self.cp.frontline_unit_count_limit, 0
        )
        if self.cp.has_active_frontline:
            deployable_unit_info = (
                f" (Up to {ground_unit_limit} deployable, {unit_overage} reserve)"
            )

        self.intel_summary.setText(
            "\n".join(
                [
                    f"{aircraft}/{parking} aircraft",
                    f"{fixed_wing_parking} fixed wing parking",
                    f"{ground_spawn_parking} ground spawns",
                    f"{rotary_wing_parking} rotary wing parking",
                    f"{self.cp.base.total_armor} ground units" + deployable_unit_info,
                    f"{allocated.total_transferring} more ground units en route, {allocated.total_ordered} ordered",
                    str(self.cp.runway_status),
                    f"{self.cp.active_ammo_depots_count}/{self.cp.total_ammo_depots_count} ammo depots",
                    f"{'Factory can produce units' if self.cp.has_factory else 'Does not have a factory'}",
                ]
            )
        )

    def generate_intel_tooltip(self) -> str:
        tooltip = (
            f"Deployable unit limit ({self.cp.frontline_unit_count_limit}) = {FREE_FRONTLINE_UNIT_SUPPLY} (base) + "
            f" {AMMO_DEPOT_FRONTLINE_UNIT_CONTRIBUTION} (per connected ammo depot) * {self.cp.total_ammo_depots_count} "
            f"(depots)"
        )

        if self.cp.has_active_frontline:
            unit_overage = max(
                self.cp.base.total_armor - self.cp.frontline_unit_count_limit, 0
            )
            tooltip += (
                f"\n{unit_overage} units will be held in reserve and will not be deployed to "
                f"connected frontlines for this turn"
            )

        return tooltip

    def closeEvent(self, close_event: QCloseEvent):
        GameUpdateSignal.get_instance().updateGame(self.game_model.game)

    def get_base_image(self):
        if (
            self.cp.cptype == ControlPointType.AIRCRAFT_CARRIER_GROUP
            or self.cp.cptype == ControlPointType.LHA_GROUP
        ):
            carrier_type = self.cp.get_carrier_group_type(always_supercarrier=True)
            return f"./resources/ui/units/ships/{carrier_type.id}.png"
        elif self.cp.cptype == ControlPointType.FOB and self.cp.has_helipads:
            return "./resources/ui/heliport.png"
        elif self.cp.cptype == ControlPointType.FOB:
            return "./resources/ui/fob.png"
        else:
            return "./resources/ui/airbase.png"

    def new_package(self) -> None:
        Dialog.open_new_package_dialog(self.cp, parent=self.window())

    def open_transfer_dialog(self) -> None:
        NewUnitTransferDialog(self.game_model, self.cp, parent=self.window()).show()

    def update_budget(self, game: Game) -> None:
        self.budget_display.setText(
            UnitTransactionFrame.BUDGET_FORMAT.format(game.blue.budget)
        )
