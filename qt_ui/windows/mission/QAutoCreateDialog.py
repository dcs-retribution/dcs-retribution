from typing import List

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QComboBox,
    QCheckBox,
    QPushButton,
    QMessageBox,
    QWidget,
    QHBoxLayout,
    QSpinBox,
)

from game import Game
from game.ato import FlightType
from game.commander.missionproposals import ProposedFlight, ProposedMission
from game.commander.packagefulfiller import PackageFulfiller
from game.profiling import MultiEventTracer
from qt_ui.models import PackageModel
from qt_ui.uiconstants import EVENT_ICONS


def _spinbox_template() -> QSpinBox:
    spinbox_template = QSpinBox()
    spinbox_template.setMaximum(4)
    spinbox_template.setMinimum(1)
    spinbox_template.setValue(2)
    spinbox_template.setMaximumWidth(50)
    return spinbox_template


class QAutoCreateDialog(QDialog):
    def __init__(
        self, game: Game, model: PackageModel, is_ownfor: bool, parent=None
    ) -> None:
        super().__init__(parent)
        self.game = game
        self.package_model = model
        self.package = model.package
        self.is_ownfor = is_ownfor

        self.setMinimumSize(300, 400)
        self.setWindowTitle(
            f"Auto-Create Package: {self.package_model.mission_target.name}"
        )
        self.setWindowIcon(EVENT_ICONS["strike"])

        self.layout = QVBoxLayout()

        hbox = QHBoxLayout()
        self.primary_combobox = QComboBox()
        self.primary_combobox.setFixedWidth(100)
        self.primary_count = _spinbox_template()
        self.primary_type = QComboBox()
        nr_targets = len(self.package.target.strike_targets)
        count = max(1, min(4, nr_targets // 2) + nr_targets % 1) if nr_targets else 4
        self.primary_count.setValue(count)
        hbox.addWidget(self.primary_combobox)
        hbox.addWidget(self.primary_count)
        hbox.addWidget(self.primary_type)
        self.layout.addLayout(hbox)

        self.checkboxes = {}

        hbox = QHBoxLayout()
        self.tarcap = self._create_checkbox("TARCAP")
        self.tarcap_count = _spinbox_template()
        hbox.addWidget(self.tarcap)
        hbox.addWidget(self.tarcap_count)
        self.tarcap_type = self._create_type_selector(FlightType.TARCAP)
        hbox.addWidget(self.tarcap_type)
        self.layout.addLayout(hbox)
        self.checkboxes[self.tarcap] = (
            FlightType.TARCAP,
            self.tarcap_count,
            self.tarcap_type,
        )

        hbox = QHBoxLayout()
        self.escort = self._create_checkbox("Escort")
        self.escort_count = _spinbox_template()
        hbox.addWidget(self.escort)
        hbox.addWidget(self.escort_count)
        self.escort_type = self._create_type_selector(FlightType.ESCORT)
        hbox.addWidget(self.escort_type)
        self.layout.addLayout(hbox)
        self.checkboxes[self.escort] = (
            FlightType.ESCORT,
            self.escort_count,
            self.escort_type,
        )

        hbox = QHBoxLayout()
        self.sead_escort = self._create_checkbox("SEAD Escort")
        self.sead_escort_count = _spinbox_template()
        hbox.addWidget(self.sead_escort)
        hbox.addWidget(self.sead_escort_count)
        self.sead_escort_type = self._create_type_selector(FlightType.SEAD_ESCORT)
        hbox.addWidget(self.sead_escort_type)

        self.layout.addLayout(hbox)
        self.checkboxes[self.sead_escort] = (
            FlightType.SEAD_ESCORT,
            self.sead_escort_count,
            self.sead_escort_type,
        )

        hbox = QHBoxLayout()
        self.sead = self._create_checkbox("SEAD")
        self.sead_count = _spinbox_template()
        hbox.addWidget(self.sead)
        hbox.addWidget(self.sead_count)
        self.sead_type = self._create_type_selector(FlightType.SEAD)
        hbox.addWidget(self.sead_type)
        self.layout.addLayout(hbox)
        self.checkboxes[self.sead] = (FlightType.SEAD, self.sead_count, self.sead_type)

        hbox = QHBoxLayout()
        self.sead_sweep = self._create_checkbox("SEAD Sweep")
        self.sead_sweep_count = _spinbox_template()
        hbox.addWidget(self.sead_sweep)
        hbox.addWidget(self.sead_sweep_count)
        self.sead_sweep_type = self._create_type_selector(FlightType.SEAD_SWEEP)
        hbox.addWidget(self.sead_sweep_type)
        self.layout.addLayout(hbox)
        self.checkboxes[self.sead_sweep] = (
            FlightType.SEAD_SWEEP,
            self.sead_sweep_count,
            self.sead_sweep_type,
        )

        hbox = QHBoxLayout()
        self.armed_recon = self._create_checkbox("Armed Recon")
        self.armed_recon_count = _spinbox_template()
        hbox.addWidget(self.armed_recon)
        hbox.addWidget(self.armed_recon_count)
        self.armed_recon_type = self._create_type_selector(FlightType.ARMED_RECON)
        hbox.addWidget(self.armed_recon_type)
        self.layout.addLayout(hbox)
        self.checkboxes[self.armed_recon] = (
            FlightType.ARMED_RECON,
            self.armed_recon_count,
            self.armed_recon_type,
        )

        hbox = QHBoxLayout()
        self.refueling = self._create_checkbox("Refueling")
        self.refueling_count = _spinbox_template()
        self.refueling_count.setValue(1)
        hbox.addWidget(self.refueling)
        hbox.addWidget(self.refueling_count)
        self.refueling_type = self._create_type_selector(FlightType.REFUELING)
        hbox.addWidget(self.refueling_type, 1)
        self.layout.addLayout(hbox)
        self.checkboxes[self.refueling] = (
            FlightType.REFUELING,
            self.refueling_count,
            self.refueling_type,
        )

        self.create_button = QPushButton("Create")
        self.create_button.setProperty("style", "start-button")
        self.create_button.clicked.connect(self.on_create_clicked)
        self.layout.addWidget(self.create_button)

        self.setLayout(self.layout)

        self.primary_combobox.currentIndexChanged.connect(self.on_primary_task_changed)
        primary_tasks = {
            FlightType.STRIKE,
            FlightType.OCA_AIRCRAFT,
            FlightType.OCA_RUNWAY,
            FlightType.DEAD,
            FlightType.ANTISHIP,
            FlightType.BAI,
            FlightType.CAS,
            FlightType.ARMED_RECON,
            FlightType.AIR_ASSAULT,
        }
        for mt in self.package.target.mission_types(self.is_ownfor):
            if mt in primary_tasks:
                self.primary_combobox.addItem(mt.value, mt)
        self.primary_combobox.setCurrentIndex(0)
        self._load_aircraft_types()

    @staticmethod
    def _create_checkbox(label: str) -> QCheckBox:
        cb = QCheckBox(label)
        cb.setFixedWidth(100)
        return cb

    def _create_type_selector(self, flight_type: FlightType) -> QComboBox:
        air_wing = self.game.blue.air_wing if self.is_ownfor else self.game.red.air_wing
        cb = QComboBox()
        for ac in air_wing.best_available_aircrafts_for(flight_type):
            cb.addItem(ac.variant_id, ac)
        return cb

    def _load_aircraft_types(self):
        self.primary_type.clear()
        air_wing = self.game.blue.air_wing if self.is_ownfor else self.game.red.air_wing
        for ac in air_wing.best_available_aircrafts_for(
            self.primary_combobox.currentData()
        ):
            self.primary_type.addItem(ac.variant_id, ac)
        self.primary_type.setCurrentIndex(0)

    def on_primary_task_changed(self) -> None:
        disable = self.primary_combobox.currentData() == FlightType.CAS
        to_disable = [self.escort, self.sead_escort, self.sead]
        for cb in to_disable:
            if disable:
                cb.setChecked(False)
            cb.setDisabled(disable)
        self._load_aircraft_types()

    def on_create_clicked(self) -> None:
        pf: List[ProposedFlight] = []
        count = self.primary_count.value()
        pf.append(
            ProposedFlight(
                self.primary_combobox.currentData(),
                count,
                preferred_type=self.primary_type.currentData(),
            )
        )
        for cb in self.checkboxes:
            if cb.isChecked():
                type, spinner, ac_box = self.checkboxes[cb]
                pf.append(
                    ProposedFlight(
                        type, spinner.value(), preferred_type=ac_box.currentData()
                    )
                )
        with MultiEventTracer() as tracer:
            with tracer.trace(f"Auto-plan package"):
                pm = ProposedMission(self.package.target, pf, asap=True)
                pff = PackageFulfiller(
                    self.game.coalition_for(self.is_ownfor),
                    self.game.theater,
                    self.game.db.flights,
                    self.game.settings,
                )
                now = self.package_model.game_model.sim_controller.current_time_in_sim
                package = pff.plan_mission(pm, 1, now, tracer, ignore_range=True)
                if package:
                    package.set_tot_asap(now)
                    self.package = package
                    self.package_model.package = package
                else:
                    QMessageBox.warning(
                        QWidget(),
                        "Unable to plan package",
                        "Auto-create package failed due to insufficient aircraft and/or pilots.",
                    )
                    return
        self.accept()
