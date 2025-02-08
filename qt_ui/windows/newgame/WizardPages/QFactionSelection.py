from __future__ import unicode_literals

import json
from copy import deepcopy
from typing import Union, Callable, Set, Optional, List

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QScrollArea,
    QWidget,
    QGridLayout,
    QCheckBox,
    QLabel,
    QTextBrowser,
    QPushButton,
    QComboBox,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QDialog,
    QFileDialog,
)

from game import persistency
from game.armedforces.forcegroup import ForceGroup
from game.ato import FlightType
from game.campaignloader import Campaign
from game.dcs.aircrafttype import AircraftType
from game.dcs.groundunittype import GroundUnitType
from game.dcs.shipunittype import ShipUnitType
from game.dcs.unittype import UnitType
from game.factions import Faction, FACTIONS
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.windows.newgame.jinja_env import jinja_env


class QFactionUnits(QScrollArea):
    preset_groups_changed = Signal(Faction)

    def __init__(self, faction: Faction, parent=None, show_jtac: bool = False):
        super().__init__()
        self.setWidgetResizable(True)
        self.content = QWidget()
        self.setWidget(self.content)
        self.parent = parent
        self.faction = faction
        self._create_checkboxes(show_jtac)
        self.show_jtac = show_jtac

    def _add_checkboxes(
        self,
        units: set,
        counter: int,
        grid: QGridLayout,
        combo_layout: Optional[QHBoxLayout] = None,
    ) -> int:
        counter += 1
        for i, v in enumerate(sorted(units, key=lambda x: str(x)), counter):
            cb = QCheckBox(str(v))
            cb.setCheckState(Qt.CheckState.Checked)
            self.checkboxes[str(v)] = cb
            grid.addWidget(cb, i, 1)
            counter += 1
        if combo_layout:
            counter += 1
            grid.addLayout(combo_layout, counter, 1)
        counter += 1
        return counter

    def _create_checkboxes(self, show_jtac: bool) -> None:
        counter = 0
        self.checkboxes: dict[str, QCheckBox] = {}
        grid = QGridLayout()
        grid.setColumnStretch(1, 1)
        self.add_ac_combo = QComboBox()
        hbox = self._create_aircraft_combobox(
            self.add_ac_combo,
            lambda: self._on_add_ac(self.faction.aircraft, self.add_ac_combo),
            self._aircraft_predicate,
        )
        grid.addWidget(QLabel("<strong>Aircraft:</strong>"), counter, 0)
        counter = self._add_checkboxes(self.faction.aircraft, counter, grid, hbox)

        self.add_awacs_combo = QComboBox()
        hbox = self._create_aircraft_combobox(
            self.add_awacs_combo,
            lambda: self._on_add_ac(self.faction.awacs, self.add_awacs_combo),
            self._awacs_predicate,
        )
        grid.addWidget(QLabel("<strong>AWACS:</strong>"), counter, 0)
        counter = self._add_checkboxes(self.faction.awacs, counter, grid, hbox)

        self.add_tanker_combo = QComboBox()
        hbox = self._create_aircraft_combobox(
            self.add_tanker_combo,
            lambda: self._on_add_ac(self.faction.tankers, self.add_tanker_combo),
            self._tanker_predicate,
        )
        grid.addWidget(QLabel("<strong>Tankers:</strong>"), counter, 0)
        counter = self._add_checkboxes(self.faction.tankers, counter, grid, hbox)

        self.add_frontline_combo = QComboBox()
        hbox = self._create_unit_combobox(
            self.add_frontline_combo,
            lambda: self._on_add_unit(
                self.faction.frontline_units, self.add_frontline_combo
            ),
            self.faction.frontline_units,
            ["Frontline vehicles"],
        )
        grid.addWidget(QLabel("<strong>Frontlines vehicles:</strong>"), counter, 0)
        counter = self._add_checkboxes(
            self.faction.frontline_units, counter, grid, hbox
        )

        self.add_artillery_combo = QComboBox()
        hbox = self._create_unit_combobox(
            self.add_artillery_combo,
            lambda: self._on_add_unit(
                self.faction.artillery_units, self.add_artillery_combo
            ),
            self.faction.artillery_units,
            ["Artillery"],
        )
        grid.addWidget(QLabel("<strong>Artillery units:</strong>"), counter, 0)
        counter = self._add_checkboxes(
            self.faction.artillery_units, counter, grid, hbox
        )

        self.add_logistics_combo = QComboBox()
        hbox = self._create_unit_combobox(
            self.add_logistics_combo,
            lambda: self._on_add_unit(
                self.faction.logistics_units, self.add_logistics_combo
            ),
            self.faction.logistics_units,
            ["Logistics"],
        )
        grid.addWidget(QLabel("<strong>Logistics units:</strong>"), counter, 0)
        counter = self._add_checkboxes(
            self.faction.logistics_units, counter, grid, hbox
        )

        self.add_infantry_combo = QComboBox()
        hbox = self._create_unit_combobox(
            self.add_infantry_combo,
            lambda: self._on_add_unit(
                self.faction.infantry_units, self.add_infantry_combo
            ),
            self.faction.infantry_units,
            ["Infantry"],
        )
        grid.addWidget(QLabel("<strong>Infantry units:</strong>"), counter, 0)
        counter = self._add_checkboxes(self.faction.infantry_units, counter, grid, hbox)

        self.add_preset_group_combo = QComboBox()
        hbox = self._create_preset_group_combobox(
            self.add_preset_group_combo,
            lambda: self._on_add_preset_group(
                self.faction.preset_groups, self.add_preset_group_combo
            ),
        )
        grid.addWidget(QLabel("<strong>Preset groups:</strong>"), counter, 0)
        counter = self._add_checkboxes(self.faction.preset_groups, counter, grid, hbox)

        self.add_air_defense_combo = QComboBox()
        hbox = self._create_unit_combobox(
            self.add_air_defense_combo,
            lambda: self._on_add_unit(
                self.faction.air_defense_units, self.add_air_defense_combo
            ),
            self.faction.air_defense_units,
            ["EarlyWarningRadar", "AAA", "SHORAD"],
        )
        grid.addWidget(QLabel("<strong>Air defenses:</strong>"), counter, 0)
        counter = self._add_checkboxes(
            self.faction.air_defense_units, counter, grid, hbox
        )

        self.add_naval_combo = QComboBox()
        hbox = self._create_naval_combobox(
            self.add_naval_combo,
            lambda: self._on_add_unit(self.faction.naval_units, self.add_naval_combo),
        )
        grid.addWidget(QLabel("<strong>Naval units:</strong>"), counter, 0)
        counter = self._add_checkboxes(self.faction.naval_units, counter, grid, hbox)

        self.add_missile_combo = QComboBox()
        hbox = self._create_unit_combobox(
            self.add_missile_combo,
            lambda: self._on_add_unit(self.faction.missiles, self.add_missile_combo),
            self.faction.missiles,
            ["Missile"],
        )
        grid.addWidget(QLabel("<strong>Missile units:</strong>"), counter, 0)
        counter = self._add_checkboxes(self.faction.missiles, counter, grid, hbox)

        if show_jtac:
            grid.addWidget(QLabel("<strong>JTAC</strong>"), counter, 0)
            self.create_has_jtac_checkbox(counter, grid)

        self.content.setLayout(grid)

    def create_has_jtac_checkbox(self, counter: int, grid: QGridLayout) -> None:
        counter += 1
        cb = QCheckBox("Has JTAC")
        cb.setCheckState(
            Qt.CheckState.Checked if self.faction.has_jtac else Qt.CheckState.Unchecked
        )
        cb.clicked.connect(self._set_jtac)
        self.checkboxes["Has JTAC"] = cb
        grid.addWidget(cb, counter, 1)
        counter += 2

    def _set_jtac(self, state: bool) -> None:
        self.faction.has_jtac = state

    def _aircraft_predicate(self, ac: AircraftType):
        if (
            FlightType.AEWC not in ac.task_priorities
            and FlightType.REFUELING not in ac.task_priorities
        ):
            self.add_ac_combo.addItem(ac.variant_id, ac)

    def _awacs_predicate(self, ac: AircraftType):
        if FlightType.AEWC in ac.task_priorities:
            self.add_awacs_combo.addItem(ac.variant_id, ac)

    def _tanker_predicate(self, ac: AircraftType):
        if FlightType.REFUELING in ac.task_priorities:
            self.add_tanker_combo.addItem(ac.variant_id, ac)

    def _create_aircraft_combobox(
        self, cb: QComboBox, callback: Callable, predicate: Callable
    ):
        for ac_dcs in sorted(AircraftType.each_dcs_type(), key=lambda x: x.id):
            for ac in AircraftType.for_dcs_type(ac_dcs):
                if (
                    ac in self.faction.aircraft
                    or ac in self.faction.awacs
                    or ac in self.faction.tankers
                ):
                    continue
                predicate(ac)
        hbox = self._format(cb, callback)
        return hbox

    def _create_unit_combobox(
        self, cb: QComboBox, callback: Callable, units: Set[GroundUnitType], type: list
    ):
        for dcs_unit in sorted(GroundUnitType.each_dcs_type(), key=lambda x: x.id):
            if dcs_unit not in self.faction.country.vehicles:
                continue
            for unit in GroundUnitType.for_dcs_type(dcs_unit):
                if unit in units:
                    continue
                if "Frontline vehicles" in type:
                    cb.addItem(unit.variant_id, unit)
                elif unit.unit_class.value in type:
                    cb.addItem(unit.variant_id, unit)
                else:
                    continue
        hbox = self._format(cb, callback)
        return hbox

    def _create_naval_combobox(self, cb: QComboBox, callback: Callable):
        for ship_dcs in sorted(ShipUnitType.each_dcs_type(), key=lambda x: x.id):
            for ship in ShipUnitType.for_dcs_type(ship_dcs):
                if ship in self.faction.naval_units:
                    continue
                cb.addItem(ship.variant_id, ship)
        hbox = self._format(cb, callback)
        return hbox

    def _create_preset_group_combobox(self, cb: QComboBox, callback: Callable):
        ForceGroup._load_all()
        preset_group_names = {pg.name for pg in self.faction.preset_groups}
        for preset_group in ForceGroup._by_name:
            if preset_group in preset_group_names:
                continue
            cb.addItem(preset_group, ForceGroup._by_name[preset_group])
        hbox = self._format(cb, callback)
        return hbox

    def _on_add_unit(self, units: Set[UnitType], cb: QComboBox):
        units.add(cb.currentData())
        if self.faction.__dict__.get("accessible_units"):
            # invalidate the cached property
            del self.faction.__dict__["accessible_units"]
        self.updateFaction(self.faction)

    def _on_add_ac(self, aircraft: Set[AircraftType], cb: QComboBox):
        aircraft.add(cb.currentData())
        if self.faction.__dict__.get("all_aircrafts"):
            # invalidate the cached property
            del self.faction.__dict__["all_aircrafts"]
        self.updateFaction(self.faction)

    def _on_add_preset_group(self, groups: List[ForceGroup], cb: QComboBox):
        groups.append(cb.currentData())
        if self.faction.__dict__.get("accessible_units"):
            # invalidate the cached property
            del self.faction.__dict__["accessible_units"]
        self.updateFaction(self.faction)
        self.preset_groups_changed.emit(self.faction)

    def updateFaction(self, faction: Faction):
        self.faction = faction
        self.content = QWidget()
        self.setWidget(self.content)
        self._create_checkboxes(self.show_jtac)
        self.update()
        if self.parent:
            self.parent.update()

    def updateFactionUnits(self, units: Union[set, list]):
        deletes = []
        for a in units:
            if not self.checkboxes[str(a)].isChecked():
                deletes.append(a)
        for d in deletes:
            units.remove(d)

    def _format(self, cb: QComboBox, callback: Callable):
        add_button = QPushButton("+")
        add_button.setStyleSheet("QPushButton{ font-weight: bold; }")
        add_button.setFixedWidth(50)
        add_button.clicked.connect(callback)
        hbox = QHBoxLayout()
        hbox.addWidget(cb)
        hbox.addWidget(add_button)
        if cb.count() == 0:
            cb.setEnabled(False)
            add_button.setEnabled(False)
        else:
            cb.setEnabled(True)
            add_button.setEnabled(True)
        return hbox


class FactionSelection(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(FactionSelection, self).__init__(parent)

        self.setTitle("Faction selection")
        self.setSubTitle(
            "\nChoose the two opposing factions and select the player side."
        )
        self.setPixmap(
            QtWidgets.QWizard.WizardPixmap.LogoPixmap,
            QtGui.QPixmap("./resources/ui/misc/generator.png"),
        )

        self.setMinimumHeight(250)

        # Factions selection
        self.factionsGroup = QtWidgets.QGroupBox("Factions")
        self.factionsGroupLayout = QtWidgets.QHBoxLayout()
        self.blueGroupLayout = QtWidgets.QGridLayout()
        self.redGroupLayout = QtWidgets.QGridLayout()

        blueFaction = QtWidgets.QLabel("<b>Player Faction :</b>")
        self.blueFactionSelect = QtWidgets.QComboBox()
        blueFaction.setBuddy(self.blueFactionSelect)

        redFaction = QtWidgets.QLabel("<b>Enemy Faction :</b>")
        self.redFactionSelect = QtWidgets.QComboBox()
        redFaction.setBuddy(self.redFactionSelect)

        # Faction description
        self.blueFactionDescription = QTextBrowser()
        self.blueFactionDescription.setReadOnly(True)
        self.blueFactionDescription.setOpenExternalLinks(True)
        self.blueFactionDescription.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        self.blueFactionDescription.setMaximumHeight(120)

        self.redFactionDescription = QTextBrowser()
        self.redFactionDescription.setReadOnly(True)
        self.redFactionDescription.setOpenExternalLinks(True)
        self.redFactionDescription.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        self.redFactionDescription.setMaximumHeight(120)

        # Setup default selected factions
        for i, r in enumerate(FACTIONS):
            self.blueFactionSelect.addItem(r, FACTIONS[r])
            self.redFactionSelect.addItem(r, FACTIONS[r])
            if r == "Russia 1990":
                self.redFactionSelect.setCurrentIndex(i)
            if r == "USA 2005":
                self.blueFactionSelect.setCurrentIndex(i)

        self.saveBlueFactionButton = QPushButton("Save as new faction")
        self.saveRedFactionButton = QPushButton("Save as new faction")
        self.blueGroupLayout.addWidget(self.saveBlueFactionButton, 3, 0, 1, 2)
        self.redGroupLayout.addWidget(self.saveRedFactionButton, 3, 0, 1, 2)
        self.saveBlueFactionButton.clicked.connect(
            lambda: self.show_save_faction_dialog(self.selected_blue_faction)
        )
        self.saveRedFactionButton.clicked.connect(
            lambda: self.show_save_faction_dialog(self.selected_red_faction)
        )

        # Faction units
        self.blueFactionUnits = QFactionUnits(
            self.blueFactionSelect.currentData(), self.blueGroupLayout, show_jtac=True
        )
        self.redFactionUnits = QFactionUnits(
            self.redFactionSelect.currentData(), self.redGroupLayout, show_jtac=False
        )

        self.blueGroupLayout.addWidget(blueFaction, 0, 0)
        self.blueGroupLayout.addWidget(self.blueFactionSelect, 0, 1)
        self.blueGroupLayout.addWidget(self.blueFactionDescription, 1, 0, 1, 2)
        self.blueGroupLayout.addWidget(self.blueFactionUnits, 2, 0, 1, 2)

        self.redGroupLayout.addWidget(redFaction, 0, 0)
        self.redGroupLayout.addWidget(self.redFactionSelect, 0, 1)
        self.redGroupLayout.addWidget(self.redFactionDescription, 1, 0, 1, 2)
        self.redGroupLayout.addWidget(self.redFactionUnits, 2, 0, 1, 2)

        self.factionsGroupLayout.addLayout(self.blueGroupLayout)
        self.factionsGroupLayout.addLayout(self.redGroupLayout)
        self.factionsGroup.setLayout(self.factionsGroupLayout)

        # Docs Link
        docsText = QtWidgets.QLabel(
            '<a href="https://github.com/dcs-retribution/dcs-retribution/wiki/Custom-Factions"><span style="color:#FFFFFF;">How to create your own faction</span></a>'
        )
        docsText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        docsText.setOpenExternalLinks(True)

        # Link form fields
        self.registerField("blueFaction", self.blueFactionSelect)
        self.registerField("redFaction", self.redFactionSelect)

        # Build layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.factionsGroup)
        layout.addWidget(docsText)
        self.setLayout(layout)
        self.updateUnitRecap()

        self.blueFactionSelect.activated.connect(self.updateUnitRecap)
        self.redFactionSelect.activated.connect(self.updateUnitRecap)

    def setDefaultFactions(self, campaign: Campaign):
        """Set default faction for selected campaign"""

        self.blueFactionSelect.clear()
        self.redFactionSelect.clear()

        for f in FACTIONS:
            self.blueFactionSelect.addItem(f)

        for i, r in enumerate(FACTIONS):
            self.redFactionSelect.addItem(r)
            if r == campaign.recommended_enemy_faction:
                self.redFactionSelect.setCurrentIndex(i)
            if r == campaign.recommended_player_faction:
                self.blueFactionSelect.setCurrentIndex(i)

        self.updateUnitRecap()

    def updateUnitRecap(self):
        red_faction = FACTIONS[self.redFactionSelect.currentText()]
        blue_faction = FACTIONS[self.blueFactionSelect.currentText()]

        template = jinja_env.get_template("factiontemplate_EN.j2")

        blue_faction_txt = template.render({"faction": blue_faction})
        red_faction_txt = template.render({"faction": red_faction})

        self.blueFactionDescription.setText(blue_faction_txt)
        self.redFactionDescription.setText(red_faction_txt)

        self.blueGroupLayout.removeWidget(self.blueFactionUnits)
        self.blueFactionUnits.updateFaction(blue_faction)
        self.blueGroupLayout.addWidget(self.blueFactionUnits, 2, 0, 1, 2)
        self.redGroupLayout.removeWidget(self.redFactionUnits)
        self.redFactionUnits.updateFaction(red_faction)
        self.redGroupLayout.addWidget(self.redFactionUnits, 2, 0, 1, 2)

    @staticmethod
    def _filter_selected_units(qfu: QFactionUnits) -> Faction:
        fac = deepcopy(qfu.faction)
        qfu.updateFactionUnits(fac.aircraft)
        qfu.updateFactionUnits(fac.awacs)
        qfu.updateFactionUnits(fac.tankers)
        qfu.updateFactionUnits(fac.frontline_units)
        qfu.updateFactionUnits(fac.artillery_units)
        qfu.updateFactionUnits(fac.logistics_units)
        qfu.updateFactionUnits(fac.infantry_units)
        qfu.updateFactionUnits(fac.preset_groups)
        qfu.updateFactionUnits(fac.air_defense_units)
        qfu.updateFactionUnits(fac.naval_units)
        qfu.updateFactionUnits(fac.missiles)
        return fac

    def show_save_faction_dialog(self, faction: Faction):
        dialog = QFactionSaver(faction)
        dialog.exec()
        for r in FACTIONS:
            if self.blueFactionSelect.findText(r) == -1:
                self.blueFactionSelect.addItem(r, FACTIONS[r])
            if self.redFactionSelect.findText(r) == -1:
                self.redFactionSelect.addItem(r, FACTIONS[r])

    @property
    def selected_blue_faction(self) -> Faction:
        return self._filter_selected_units(self.blueFactionUnits)

    @property
    def selected_red_faction(self) -> Faction:
        return self._filter_selected_units(self.redFactionUnits)


class QFactionSaver(QDialog):
    def __init__(self, faction: Faction):
        super().__init__()
        self.faction = faction

        self.setMinimumWidth(400)
        self.setWindowTitle("Save new faction")
        self.setWindowIcon(EVENT_ICONS["strike"])

        layout = QVBoxLayout()

        self.name_label = QLabel("Name:")
        self.name_text = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_text)

        self.description_label = QLabel("Description:")
        self.description_text = QLineEdit()
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_text)

        self.authors_label = QLabel("Author(s):")
        self.authors_text = QLineEdit()
        layout.addWidget(self.authors_label)
        layout.addWidget(self.authors_text)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_faction)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def save_faction(self) -> None:
        self.faction.name = self.name_text.text()
        self.faction.description = f"<p>{self.description_text.text()}</p>"
        self.faction.authors = self.authors_text.text()
        user_faction_path = persistency.factions_dir()

        fd = QFileDialog(
            caption="Save Faction", directory=str(user_faction_path), filter="*.json"
        )
        fd.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        if fd.exec_():
            json_filename = fd.selectedFiles()[0]
            with open(json_filename, "w") as file:
                json.dump(self.faction.to_dict(), file, indent=2)
            FACTIONS.factions[self.faction.name] = self.faction
        self.accept()
