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
    def __init__(self, game: Game, model: PackageModel, parent=None) -> None:
        super().__init__(parent)
        self.game = game
        self.package_model = model
        self.package = model.package

        self.setMinimumSize(300, 400)
        self.setWindowTitle(
            f"Auto-Create Package: {self.package_model.mission_target.name}"
        )
        self.setWindowIcon(EVENT_ICONS["strike"])

        self.layout = QVBoxLayout()

        hbox = QHBoxLayout()
        self.primary_combobox = QComboBox()
        self.primary_count = _spinbox_template()
        nr_targets = len(self.package.target.strike_targets)
        count = max(1, min(4, nr_targets // 2) + nr_targets % 1) if nr_targets else 4
        self.primary_count.setValue(count)
        hbox.addWidget(self.primary_combobox)
        hbox.addWidget(self.primary_count)
        self.layout.addLayout(hbox)

        self.checkboxes = {}

        hbox = QHBoxLayout()
        self.tarcap = QCheckBox()
        self.tarcap.setText("TARCAP")
        self.tarcap_count = _spinbox_template()
        hbox.addWidget(self.tarcap)
        hbox.addWidget(self.tarcap_count)
        self.layout.addLayout(hbox)
        self.checkboxes[self.tarcap] = (FlightType.TARCAP, self.tarcap_count)

        hbox = QHBoxLayout()
        self.escort = QCheckBox()
        self.escort.setText("Escort")
        self.escort_count = _spinbox_template()
        hbox.addWidget(self.escort)
        hbox.addWidget(self.escort_count)
        self.layout.addLayout(hbox)
        self.checkboxes[self.escort] = (FlightType.ESCORT, self.escort_count)

        hbox = QHBoxLayout()
        self.sead_escort = QCheckBox()
        self.sead_escort.setText("SEAD Escort")
        self.sead_escort_count = _spinbox_template()
        hbox.addWidget(self.sead_escort)
        hbox.addWidget(self.sead_escort_count)
        self.layout.addLayout(hbox)
        self.checkboxes[self.sead_escort] = (
            FlightType.SEAD_ESCORT,
            self.sead_escort_count,
        )

        hbox = QHBoxLayout()
        self.sead = QCheckBox()
        self.sead.setText("SEAD")
        self.sead_count = _spinbox_template()
        hbox.addWidget(self.sead)
        hbox.addWidget(self.sead_count)
        self.layout.addLayout(hbox)
        self.checkboxes[self.sead] = (FlightType.SEAD, self.sead_count)

        hbox = QHBoxLayout()
        self.sead_sweep = QCheckBox()
        self.sead_sweep.setText("SEAD Sweep")
        self.sead_sweep_count = _spinbox_template()
        hbox.addWidget(self.sead_sweep)
        hbox.addWidget(self.sead_sweep_count)
        self.layout.addLayout(hbox)
        self.checkboxes[self.sead_sweep] = (
            FlightType.SEAD_SWEEP,
            self.sead_sweep_count,
        )

        hbox = QHBoxLayout()
        self.refueling = QCheckBox()
        self.refueling.setText("Refueling")
        self.refueling_count = _spinbox_template()
        self.refueling_count.setValue(1)
        hbox.addWidget(self.refueling)
        hbox.addWidget(self.refueling_count)
        self.layout.addLayout(hbox)
        self.checkboxes[self.refueling] = (FlightType.REFUELING, self.refueling_count)

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
        }
        for mt in self.package.target.mission_types(True):
            if mt in primary_tasks:
                self.primary_combobox.addItem(mt.value, mt)
        self.primary_combobox.setCurrentIndex(0)

    def on_primary_task_changed(self) -> None:
        disable = self.primary_combobox.currentData() == FlightType.CAS
        to_disable = [self.escort, self.sead_escort, self.sead]
        for cb in to_disable:
            if disable:
                cb.setChecked(False)
            cb.setDisabled(disable)

    def on_create_clicked(self) -> None:
        pf: List[ProposedFlight] = []
        count = self.primary_count.value()
        pf.append(ProposedFlight(self.primary_combobox.currentData(), count))
        for cb in self.checkboxes:
            if cb.isChecked():
                type, spinner = self.checkboxes[cb]
                pf.append(ProposedFlight(type, spinner.value()))
        with MultiEventTracer() as tracer:
            with tracer.trace(f"Auto-plan package"):
                pm = ProposedMission(self.package.target, pf, asap=True)
                pff = PackageFulfiller(
                    self.game.coalition_for(True),
                    self.game.theater,
                    self.game.db.flights,
                    self.game.settings,
                )
                now = self.package_model.game_model.sim_controller.current_time_in_sim
                package = pff.plan_mission(pm, 1, now, tracer)
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
