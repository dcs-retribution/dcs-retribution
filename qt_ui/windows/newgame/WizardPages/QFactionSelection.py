from __future__ import unicode_literals

from copy import deepcopy
from typing import Union, Callable, Set, Optional

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt
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
)

from game.ato import FlightType
from game.campaignloader import Campaign
from game.dcs.aircrafttype import AircraftType
from game.dcs.groundunittype import GroundUnitType
from game.dcs.unittype import UnitType
from game.factions import Faction, FACTIONS
from qt_ui.windows.newgame.jinja_env import jinja_env


class QFactionUnits(QScrollArea):
    def __init__(self, faction: Faction, parent=None):
        super().__init__()
        self.setWidgetResizable(True)
        self.content = QWidget()
        self.setWidget(self.content)
        self.parent = parent
        self.faction = faction
        self._create_checkboxes()

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

    def _create_checkboxes(self):
        counter = 0
        self.checkboxes: dict[str, QCheckBox] = {}
        grid = QGridLayout()
        grid.setColumnStretch(1, 1)
        if len(self.faction.aircraft) > 0:
            self.add_ac_combo = QComboBox()
            hbox = self._create_aircraft_combobox(
                self.add_ac_combo,
                lambda: self._on_add_ac(self.faction.aircraft, self.add_ac_combo),
                self._aircraft_predicate,
            )
            grid.addWidget(QLabel("<strong>Aircraft:</strong>"), counter, 0)
            counter = self._add_checkboxes(self.faction.aircraft, counter, grid, hbox)
        if len(self.faction.awacs) > 0:
            self.add_awacs_combo = QComboBox()
            hbox = self._create_aircraft_combobox(
                self.add_awacs_combo,
                lambda: self._on_add_ac(self.faction.awacs, self.add_awacs_combo),
                self._awacs_predicate,
            )
            grid.addWidget(QLabel("<strong>AWACS:</strong>"), counter, 0)
            counter = self._add_checkboxes(self.faction.awacs, counter, grid, hbox)
        if len(self.faction.tankers) > 0:
            self.add_tanker_combo = QComboBox()
            hbox = self._create_aircraft_combobox(
                self.add_tanker_combo,
                lambda: self._on_add_ac(self.faction.tankers, self.add_tanker_combo),
                self._tanker_predicate,
            )
            grid.addWidget(QLabel("<strong>Tankers:</strong>"), counter, 0)
            counter = self._add_checkboxes(self.faction.tankers, counter, grid, hbox)
        if len(self.faction.frontline_units) > 0:
            self.add_frontline_combo = QComboBox()
            hbox = self._create_unit_combobox(
                self.add_frontline_combo,
                lambda: self._on_add_unit(
                    self.faction.frontline_units, self.add_frontline_combo
                ),
                self.faction.frontline_units,
            )
            grid.addWidget(QLabel("<strong>Frontlines vehicles:</strong>"), counter, 0)
            counter = self._add_checkboxes(
                self.faction.frontline_units, counter, grid, hbox
            )
        if len(self.faction.artillery_units) > 0:
            grid.addWidget(QLabel("<strong>Artillery units:</strong>"), counter, 0)
            counter = self._add_checkboxes(self.faction.artillery_units, counter, grid)
        if len(self.faction.logistics_units) > 0:
            grid.addWidget(QLabel("<strong>Logistics units:</strong>"), counter, 0)
            counter = self._add_checkboxes(self.faction.logistics_units, counter, grid)
        if len(self.faction.infantry_units) > 0:
            grid.addWidget(QLabel("<strong>Infantry units:</strong>"), counter, 0)
            counter = self._add_checkboxes(self.faction.infantry_units, counter, grid)
        if len(self.faction.preset_groups) > 0:
            grid.addWidget(QLabel("<strong>Preset groups:</strong>"), counter, 0)
            counter = self._add_checkboxes(self.faction.preset_groups, counter, grid)
        if len(self.faction.air_defense_units) > 0:
            grid.addWidget(QLabel("<strong>Air defenses:</strong>"), counter, 0)
            counter = self._add_checkboxes(
                self.faction.air_defense_units, counter, grid
            )
        if len(self.faction.naval_units) > 0:
            grid.addWidget(QLabel("<strong>Naval units:</strong>"), counter, 0)
            counter = self._add_checkboxes(self.faction.naval_units, counter, grid)
        if len(self.faction.missiles) > 0:
            grid.addWidget(QLabel("<strong>Missile units:</strong>"), counter, 0)
            self._add_checkboxes(self.faction.missiles, counter, grid)

        self.content.setLayout(grid)

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
                if ac in self.faction.aircraft:
                    continue
                predicate(ac)
        add_ac = QPushButton("+")
        add_ac.setStyleSheet("QPushButton{ font-weight: bold; }")
        add_ac.setFixedWidth(50)
        add_ac.clicked.connect(callback)
        hbox = QHBoxLayout()
        hbox.addWidget(cb)
        hbox.addWidget(add_ac)
        return hbox

    def _create_unit_combobox(
        self, cb: QComboBox, callback: Callable, units: Set[GroundUnitType]
    ):
        for dcs_unit in sorted(GroundUnitType.each_dcs_type(), key=lambda x: x.id):
            if dcs_unit not in self.faction.country.vehicles:
                continue
            for unit in GroundUnitType.for_dcs_type(dcs_unit):
                if unit in units:
                    continue
                cb.addItem(unit.variant_id, unit)
        add_unit = QPushButton("+")
        add_unit.setStyleSheet("QPushButton{ font-weight: bold; }")
        add_unit.setFixedWidth(50)
        add_unit.clicked.connect(callback)
        hbox = QHBoxLayout()
        hbox.addWidget(cb)
        hbox.addWidget(add_unit)
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

    def updateFaction(self, faction: Faction):
        self.faction = faction
        self.content = QWidget()
        self.setWidget(self.content)
        self._create_checkboxes()
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

        # Faction units
        self.blueFactionUnits = QFactionUnits(
            self.blueFactionSelect.currentData(), self.blueGroupLayout
        )
        self.redFactionUnits = QFactionUnits(
            self.redFactionSelect.currentData(), self.redGroupLayout
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

    @property
    def selected_blue_faction(self) -> Faction:
        return self._filter_selected_units(self.blueFactionUnits)

    @property
    def selected_red_faction(self) -> Faction:
        return self._filter_selected_units(self.redFactionUnits)
