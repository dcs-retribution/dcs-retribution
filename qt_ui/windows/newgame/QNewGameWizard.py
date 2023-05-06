from __future__ import unicode_literals

import logging
from copy import deepcopy
from datetime import datetime, timedelta
from typing import List

from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import QDate, QItemSelectionModel, QPoint, Qt, Signal
from PySide2.QtWidgets import (
    QCheckBox,
    QLabel,
    QTextEdit,
    QVBoxLayout,
    QTextBrowser,
    QWidget,
    QGridLayout,
    QScrollArea,
)
from jinja2 import Environment, FileSystemLoader, select_autoescape

from game.campaignloader.campaign import Campaign, DEFAULT_BUDGET
from game.dcs.aircrafttype import AircraftType
from game.factions import FACTIONS, Faction
from game.settings import Settings
from game.theater.start_generator import GameGenerator, GeneratorSettings, ModSettings
from qt_ui.widgets.QLiberationCalendar import QLiberationCalendar
from qt_ui.widgets.spinsliders import CurrencySpinner, FloatSpinSlider, TimeInputs
from qt_ui.windows.AirWingConfigurationDialog import AirWingConfigurationDialog
from qt_ui.windows.newgame.QCampaignList import QCampaignList

jinja_env = Environment(
    loader=FileSystemLoader("resources/ui/templates"),
    autoescape=select_autoescape(
        disabled_extensions=("",),
        default_for_string=True,
        default=True,
    ),
    trim_blocks=True,
    lstrip_blocks=True,
)

DEFAULT_MISSION_LENGTH: timedelta = timedelta(minutes=60)


"""
Possible time periods for new games

    `Name`: daytime(day, month, year),

`Identifier` is the name that will appear in the menu
The object is a python datetime object
"""
TIME_PERIODS = {
    "WW2 - Winter [1944]": datetime(1944, 1, 1),
    "WW2 - Spring [1944]": datetime(1944, 4, 1),
    "WW2 - Summer [1944]": datetime(1944, 6, 1),
    "WW2 - Fall [1944]": datetime(1944, 10, 1),
    "Early Cold War - Winter [1952]": datetime(1952, 1, 1),
    "Early Cold War - Spring [1952]": datetime(1952, 4, 1),
    "Early Cold War - Summer [1952]": datetime(1952, 6, 1),
    "Early Cold War - Fall [1952]": datetime(1952, 10, 1),
    "Cold War - Winter [1970]": datetime(1970, 1, 1),
    "Cold War - Spring [1970]": datetime(1970, 4, 1),
    "Cold War - Summer [1970]": datetime(1970, 6, 1),
    "Cold War - Fall [1970]": datetime(1970, 10, 1),
    "Late Cold War - Winter [1985]": datetime(1985, 1, 1),
    "Late Cold War - Spring [1985]": datetime(1985, 4, 1),
    "Late Cold War - Summer [1985]": datetime(1985, 6, 1),
    "Late Cold War - Fall [1985]": datetime(1985, 10, 1),
    "Gulf War - Winter [1990]": datetime(1990, 1, 1),
    "Gulf War - Spring [1990]": datetime(1990, 4, 1),
    "Gulf War - Summer [1990]": datetime(1990, 6, 1),
    "Mid-90s - Winter [1995]": datetime(1995, 1, 1),
    "Mid-90s - Spring [1995]": datetime(1995, 4, 1),
    "Mid-90s - Summer [1995]": datetime(1995, 6, 1),
    "Mid-90s - Fall [1995]": datetime(1995, 10, 1),
    "Gulf War - Fall [1990]": datetime(1990, 10, 1),
    "Modern - Winter [2010]": datetime(2010, 1, 1),
    "Modern - Spring [2010]": datetime(2010, 4, 1),
    "Modern - Summer [2010]": datetime(2010, 6, 1),
    "Modern - Fall [2010]": datetime(2010, 10, 1),
    "Georgian War [2008]": datetime(2008, 8, 7),
    "Syrian War [2011]": datetime(2011, 3, 15),
    "6 days war [1967]": datetime(1967, 6, 5),
    "Yom Kippour War [1973]": datetime(1973, 10, 6),
    "First Lebanon War [1982]": datetime(1982, 6, 6),
    "Arab-Israeli War [1948]": datetime(1948, 5, 15),
}

# fmt: off
RUNWAY_REPAIR = f"{Settings.automate_runway_repair=}".split("=")[0].split(".")[1]
FRONTLINE = f"{Settings.automate_front_line_reinforcements=}".split("=")[0].split(".")[1]
AIRCRAFT = f"{Settings.automate_aircraft_reinforcements=}".split("=")[0].split(".")[1]
MISSION_LENGTH = f"{Settings.desired_player_mission_duration=}".split("=")[0].split(".")[1]
SUPER_CARRIER = f"{Settings.supercarrier=}".split("=")[0].split(".")[1]
# fmt: on


class NewGameWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(NewGameWizard, self).__init__(parent)
        self.setOption(QtWidgets.QWizard.IndependentPages)

        self.campaigns = list(sorted(Campaign.load_each(), key=lambda x: x.name))

        self.faction_selection_page = FactionSelection(self)
        self.addPage(IntroPage(self))
        self.theater_page = TheaterConfiguration(
            self.campaigns, self.faction_selection_page, self
        )
        self.addPage(self.theater_page)
        self.addPage(self.faction_selection_page)
        self.go_page = GeneratorOptions(self.campaigns[0], self)
        self.addPage(self.go_page)
        self.difficulty_page = DifficultyAndAutomationOptions(self)
        self.difficulty_page.set_campaign_values(self.campaigns[0])

        # Update difficulty page on campaign select
        self.theater_page.campaign_selected.connect(lambda c: self.update_settings(c))
        self.addPage(self.difficulty_page)
        self.addPage(ConclusionPage(self))

        self.setPixmap(
            QtWidgets.QWizard.WatermarkPixmap,
            QtGui.QPixmap("./resources/ui/wizard/watermark1.png"),
        )
        self.setWizardStyle(QtWidgets.QWizard.ModernStyle)

        self.setWindowTitle("New Game")
        self.generatedGame = None

    def accept(self):
        logging.info("New Game Wizard accept")
        logging.info("======================")

        campaign = self.field("selectedCampaign")
        if campaign is None:
            campaign = self.theater_page.campaignList.selected_campaign
        if campaign is None:
            campaign = self.campaigns[0]

        logging.info("New campaign selected: %s", campaign.name)

        if self.field("usePreset"):
            start_date = TIME_PERIODS[
                list(TIME_PERIODS.keys())[self.field("timePeriod")]
            ]
        else:
            start_date = self.theater_page.calendar.selectedDate().toPython()

        logging.info("New campaign start date: %s", start_date.strftime("%m/%d/%Y"))
        settings = Settings()
        settings.__setstate__(campaign.settings)
        settings.player_income_multiplier = self.field("player_income_multiplier") / 10
        settings.enemy_income_multiplier = self.field("enemy_income_multiplier") / 10
        settings.automate_runway_repair = self.field(RUNWAY_REPAIR)
        settings.automate_front_line_reinforcements = self.field(FRONTLINE)
        settings.desired_player_mission_duration = timedelta(
            minutes=self.field(MISSION_LENGTH)
        )
        settings.automate_aircraft_reinforcements = self.field(AIRCRAFT)
        settings.supercarrier = self.field(SUPER_CARRIER)
        settings.perf_culling = (
            campaign.settings.get("perf_culling_distance") is not None
        )

        generator_settings = GeneratorSettings(
            start_date=start_date,
            start_time=campaign.recommended_start_time,
            player_budget=int(self.field("starting_money")),
            enemy_budget=int(self.field("enemy_starting_money")),
            # QSlider forces integers, so we use 1 to 50 and divide by 10 to
            # give 0.1 to 5.0.
            inverted=self.field("invertMap"),
            advanced_iads=self.field("advanced_iads"),
            no_carrier=self.field("no_carrier"),
            no_lha=self.field("no_lha"),
            no_player_navy=self.field("no_player_navy"),
            no_enemy_navy=self.field("no_enemy_navy"),
            tgo_config=campaign.load_ground_forces_config(),
        )
        mod_settings = ModSettings(
            a4_skyhawk=self.field("a4_skyhawk"),
            a6a_intruder=self.field("a6a_intruder"),
            a7e_corsair2=self.field("a7e_corsair2"),
            f4bc_phantom=self.field("f4bc_phantom"),
            f15d_baz=self.field("f15d_baz"),
            f_16_idf=self.field("f_16_idf"),
            fa_18efg=self.field("fa_18efg"),
            f22_raptor=self.field("f22_raptor"),
            f84g_thunderjet=self.field("f84g_thunderjet"),
            f100_supersabre=self.field("f100_supersabre"),
            f104_starfighter=self.field("f104_starfighter"),
            f105_thunderchief=self.field("f105_thunderchief"),
            hercules=self.field("hercules"),
            uh_60l=self.field("uh_60l"),
            jas39_gripen=self.field("jas39_gripen"),
            su30_flanker_h=self.field("su30_flanker_h"),
            su57_felon=self.field("su57_felon"),
            ov10a_bronco=self.field("ov10a_bronco"),
            frenchpack=self.field("frenchpack"),
            high_digit_sams=self.field("high_digit_sams"),
            swedishmilitaryassetspack=self.field("swedishmilitaryassetspack"),
            SWPack=self.field("SWPack"),
        )

        blue_faction = self.faction_selection_page.selected_blue_faction
        red_faction = self.faction_selection_page.selected_red_faction

        logging.info("New campaign blue faction: %s", blue_faction.name)
        logging.info("New campaign red faction: %s", red_faction.name)

        theater = campaign.load_theater(generator_settings.advanced_iads)

        logging.info("New campaign theater: %s", theater.terrain.name)

        generator = GameGenerator(
            blue_faction,
            red_faction,
            theater,
            campaign.load_air_wing_config(theater),
            settings,
            generator_settings,
            mod_settings,
        )
        self.generatedGame = generator.generate()

        AirWingConfigurationDialog(self.generatedGame, self).exec_()

        g = self.generatedGame
        herc = AircraftType.named("C-130J-30 Super Hercules")
        if herc in g.blue.air_wing.squadrons or herc in g.red.air_wing.squadrons:
            g.settings.set_plugin_option("herculescargo", True)

        self.generatedGame.begin_turn_0()

        super(NewGameWizard, self).accept()

    def update_settings(self, campaign: Campaign) -> None:
        self.difficulty_page.set_campaign_values(campaign)
        self.go_page.update_settings(campaign)


class IntroPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setTitle("Introduction")
        self.setPixmap(
            QtWidgets.QWizard.WatermarkPixmap,
            QtGui.QPixmap("./resources/ui/wizard/watermark1.png"),
        )

        label = QtWidgets.QLabel(
            "This wizard will help you setup a new game.\n\n"
            "Please make sure you saved and backed up your previous game before going through."
        )
        label.setWordWrap(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class QFactionUnits(QScrollArea):
    def __init__(self, faction: Faction, parent=None):
        super().__init__()
        self.setWidgetResizable(True)
        self.content = QWidget()
        self.setWidget(self.content)
        self.parent = parent
        self.faction = faction
        self._create_checkboxes()

    def _add_checkboxes(self, units: list, counter: int, grid: QGridLayout) -> int:
        counter += 1
        for i, v in enumerate(sorted(units, key=lambda x: x.name), counter):
            cb = QCheckBox(v.name)
            cb.setCheckState(Qt.CheckState.Checked)
            self.checkboxes[v.name] = cb
            grid.addWidget(cb, i, 1)
            counter += 1
        counter += 1
        return counter

    def _create_checkboxes(self):
        counter = 0
        self.checkboxes: dict[str, QCheckBox] = {}
        grid = QGridLayout()
        if len(self.faction.aircraft) > 0:
            grid.addWidget(QLabel("<strong>Aircraft:</strong>"), counter, 0)
            counter = self._add_checkboxes(self.faction.aircraft, counter, grid)
        if len(self.faction.awacs) > 0:
            grid.addWidget(QLabel("<strong>AWACS:</strong>"), counter, 0)
            counter = self._add_checkboxes(self.faction.awacs, counter, grid)
        if len(self.faction.tankers) > 0:
            grid.addWidget(QLabel("<strong>Tankers:</strong>"), counter, 0)
            counter = self._add_checkboxes(self.faction.tankers, counter, grid)
        if len(self.faction.frontline_units) > 0:
            grid.addWidget(QLabel("<strong>Frontlines vehicles:</strong>"), counter, 0)
            counter = self._add_checkboxes(self.faction.frontline_units, counter, grid)
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

    def updateFaction(self, faction: Faction):
        self.faction = faction
        self.content = QWidget()
        self.setWidget(self.content)
        self._create_checkboxes()
        self.update()
        if self.parent:
            self.parent.update()

    def updateFactionUnits(self, units: list):
        deletes = []
        for a in units:
            if not self.checkboxes[a.name].isChecked():
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
            QtWidgets.QWizard.LogoPixmap,
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
        self.blueFactionDescription.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.blueFactionDescription.setMaximumHeight(120)

        self.redFactionDescription = QTextBrowser()
        self.redFactionDescription.setReadOnly(True)
        self.redFactionDescription.setOpenExternalLinks(True)
        self.redFactionDescription.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
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
            '<a href="https://github.com/dcs-liberation/dcs_liberation/wiki/Custom-Factions"><span style="color:#FFFFFF;">How to create your own faction</span></a>'
        )
        docsText.setAlignment(Qt.AlignCenter)
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
        qfu.updateFactionUnits(fac.aircrafts)
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


class TheaterConfiguration(QtWidgets.QWizardPage):
    campaign_selected = Signal(Campaign)

    def __init__(
        self,
        campaigns: List[Campaign],
        faction_selection: FactionSelection,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.faction_selection = faction_selection

        self.setTitle("Theater configuration")
        self.setSubTitle("\nChoose a terrain and time period for this game.")
        self.setPixmap(
            QtWidgets.QWizard.LogoPixmap,
            QtGui.QPixmap("./resources/ui/wizard/logo1.png"),
        )

        self.setPixmap(
            QtWidgets.QWizard.WatermarkPixmap,
            QtGui.QPixmap("./resources/ui/wizard/watermark3.png"),
        )

        # List of campaigns
        show_incompatible_campaigns_checkbox = QCheckBox(
            text="Show incompatible campaigns"
        )
        show_incompatible_campaigns_checkbox.setChecked(False)
        self.campaignList = QCampaignList(
            campaigns, show_incompatible_campaigns_checkbox.isChecked()
        )
        show_incompatible_campaigns_checkbox.toggled.connect(
            lambda checked: self.campaignList.setup_content(show_incompatible=checked)
        )
        self.registerField("selectedCampaign", self.campaignList)

        # Faction description
        self.campaignMapDescription = QTextBrowser()
        self.campaignMapDescription.setReadOnly(True)
        self.campaignMapDescription.setOpenExternalLinks(True)
        self.campaignMapDescription.setMaximumHeight(200)

        self.performanceText = QTextEdit("")
        self.performanceText.setReadOnly(True)
        self.performanceText.setMaximumHeight(90)

        # Campaign settings
        mapSettingsGroup = QtWidgets.QGroupBox("Map Settings")
        mapSettingsLayout = QtWidgets.QGridLayout()
        invertMap = QtWidgets.QCheckBox()
        self.registerField("invertMap", invertMap)
        mapSettingsLayout.addWidget(QtWidgets.QLabel("Invert Map"), 0, 0)
        mapSettingsLayout.addWidget(invertMap, 0, 1)
        self.advanced_iads = QtWidgets.QCheckBox()
        self.registerField("advanced_iads", self.advanced_iads)
        self.iads_label = QtWidgets.QLabel("Advanced IADS (WIP)")
        mapSettingsLayout.addWidget(self.iads_label, 1, 0)
        mapSettingsLayout.addWidget(self.advanced_iads, 1, 1)
        mapSettingsGroup.setLayout(mapSettingsLayout)

        # Time Period
        timeGroup = QtWidgets.QGroupBox("Time Period")
        timePeriod = QtWidgets.QLabel("Start date :")
        timePeriodSelect = QtWidgets.QComboBox()
        timePeriodPresetLabel = QLabel("Use preset :")
        timePeriodPreset = QtWidgets.QCheckBox()
        timePeriodPreset.setChecked(True)
        self.calendar = QLiberationCalendar()
        self.calendar.setSelectedDate(QDate())
        self.calendar.setDisabled(True)

        def onTimePeriodChanged():
            self.calendar.setSelectedDate(
                list(TIME_PERIODS.values())[timePeriodSelect.currentIndex()]
            )

        timePeriodSelect.currentTextChanged.connect(onTimePeriodChanged)

        for r in TIME_PERIODS:
            timePeriodSelect.addItem(r)
        timePeriod.setBuddy(timePeriodSelect)
        timePeriodSelect.setCurrentIndex(21)

        def onTimePeriodCheckboxChanged():
            if timePeriodPreset.isChecked():
                self.calendar.setDisabled(True)
                timePeriodSelect.setDisabled(False)
                onTimePeriodChanged()
            else:
                self.calendar.setDisabled(False)
                timePeriodSelect.setDisabled(True)

        timePeriodPreset.stateChanged.connect(onTimePeriodCheckboxChanged)

        # Bind selection method for campaign selection
        def on_campaign_selected():
            template = jinja_env.get_template("campaigntemplate_EN.j2")
            template_perf = jinja_env.get_template(
                "campaign_performance_template_EN.j2"
            )
            campaign = self.campaignList.selected_campaign
            self.setField("selectedCampaign", campaign)
            if campaign is None:
                self.campaignMapDescription.setText("No campaign selected")
                self.performanceText.setText("No campaign selected")
                return

            self.campaignMapDescription.setText(template.render({"campaign": campaign}))
            self.faction_selection.setDefaultFactions(campaign)
            self.performanceText.setText(
                template_perf.render({"performance": campaign.performance})
            )

            if (start_date := campaign.recommended_start_date) is not None:
                self.calendar.setSelectedDate(
                    QDate(start_date.year, start_date.month, start_date.day)
                )
                timePeriodPreset.setChecked(False)
            else:
                timePeriodPreset.setChecked(True)
            self.advanced_iads.setEnabled(campaign.advanced_iads)
            self.iads_label.setEnabled(campaign.advanced_iads)
            self.advanced_iads.setChecked(campaign.advanced_iads)
            if not campaign.advanced_iads:
                self.advanced_iads.setToolTip(
                    "Advanced IADS is not supported by this campaign"
                )
            else:
                self.advanced_iads.setToolTip("Enable Advanced IADS")

            self.campaign_selected.emit(campaign)

        self.campaignList.selectionModel().setCurrentIndex(
            self.campaignList.indexAt(QPoint(1, 1)), QItemSelectionModel.Rows
        )

        self.campaignList.selectionModel().selectionChanged.connect(
            on_campaign_selected
        )
        on_campaign_selected()

        docsText = QtWidgets.QLabel(
            "<p>Want more campaigns? You can "
            '<a href="https://github.com/dcs-liberation/dcs_liberation/wiki/Campaign-maintenance"><span style="color:#FFFFFF;">offer to help</span></a>, '
            '<a href="https://github.com/dcs-liberation/dcs_liberation/wiki/Community-campaigns"><span style="color:#FFFFFF;">play a community campaign</span></a>, '
            'or <a href="https://github.com/dcs-liberation/dcs_liberation/wiki/Custom-Campaigns"><span style="color:#FFFFFF;">create your own</span></a>.'
            "</p>"
        )
        docsText.setAlignment(Qt.AlignCenter)
        docsText.setOpenExternalLinks(True)

        # Register fields
        self.registerField("timePeriod", timePeriodSelect)
        self.registerField("usePreset", timePeriodPreset)

        timeGroupLayout = QtWidgets.QGridLayout()
        timeGroupLayout.addWidget(timePeriodPresetLabel, 0, 0)
        timeGroupLayout.addWidget(timePeriodPreset, 0, 1)
        timeGroupLayout.addWidget(timePeriod, 1, 0)
        timeGroupLayout.addWidget(timePeriodSelect, 1, 1)
        timeGroupLayout.addWidget(self.calendar, 0, 2, 3, 1)
        timeGroup.setLayout(timeGroupLayout)

        layout = QtWidgets.QGridLayout()
        layout.setColumnMinimumWidth(0, 20)
        layout.addWidget(self.campaignList, 0, 0, 5, 1)
        layout.addWidget(show_incompatible_campaigns_checkbox, 5, 0, 1, 1)
        layout.addWidget(docsText, 6, 0, 1, 1)
        layout.addWidget(self.campaignMapDescription, 0, 1, 1, 1)
        layout.addWidget(self.performanceText, 1, 1, 1, 1)
        layout.addWidget(mapSettingsGroup, 2, 1, 1, 1)
        layout.addWidget(timeGroup, 3, 1, 3, 1)
        self.setLayout(layout)


class BudgetInputs(QtWidgets.QGridLayout):
    def __init__(self, label: str, value: int) -> None:
        super().__init__()
        self.addWidget(QtWidgets.QLabel(label), 0, 0)

        minimum = 0
        maximum = 5000

        slider = QtWidgets.QSlider(Qt.Horizontal)
        slider.setMinimum(minimum)
        slider.setMaximum(maximum)
        slider.setValue(value)
        self.starting_money = CurrencySpinner(minimum, maximum, value)
        slider.valueChanged.connect(lambda x: self.starting_money.setValue(x))
        self.starting_money.valueChanged.connect(lambda x: slider.setValue(x))

        self.addWidget(slider, 1, 0)
        self.addWidget(self.starting_money, 1, 1)


class DifficultyAndAutomationOptions(QtWidgets.QWizardPage):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setTitle("Difficulty and automation options")
        self.setSubTitle(
            "\nOptions controlling game difficulty and level of " "player involvement."
        )
        self.setPixmap(
            QtWidgets.QWizard.LogoPixmap,
            QtGui.QPixmap("./resources/ui/wizard/logo1.png"),
        )

        layout = QtWidgets.QVBoxLayout()

        economy_group = QtWidgets.QGroupBox("Economy options")
        layout.addWidget(economy_group)
        economy_layout = QtWidgets.QVBoxLayout()
        economy_group.setLayout(economy_layout)

        economy_layout.addWidget(QLabel("Player income multiplier"))
        self.player_income = FloatSpinSlider(0, 5, 1, divisor=10)
        self.registerField("player_income_multiplier", self.player_income.spinner)
        economy_layout.addLayout(self.player_income)

        economy_layout.addWidget(QLabel("Enemy income multiplier"))
        self.enemy_income = FloatSpinSlider(0, 5, 1, divisor=10)
        self.registerField("enemy_income_multiplier", self.enemy_income.spinner)
        economy_layout.addLayout(self.enemy_income)

        self.player_budget = BudgetInputs("Player starting budget", DEFAULT_BUDGET)
        self.registerField("starting_money", self.player_budget.starting_money)
        economy_layout.addLayout(self.player_budget)

        self.enemy_budget = BudgetInputs("Enemy starting budget", DEFAULT_BUDGET)
        self.registerField("enemy_starting_money", self.enemy_budget.starting_money)
        economy_layout.addLayout(self.enemy_budget)

        assist_group = QtWidgets.QGroupBox("Player assists")
        layout.addWidget(assist_group)
        assist_layout = QtWidgets.QGridLayout()
        assist_group.setLayout(assist_layout)

        assist_layout.addWidget(QtWidgets.QLabel("Automate runway repairs"), 0, 0)
        self.runway_repairs = QtWidgets.QCheckBox()
        self.registerField(RUNWAY_REPAIR, self.runway_repairs)
        assist_layout.addWidget(self.runway_repairs, 0, 1, Qt.AlignRight)

        assist_layout.addWidget(QtWidgets.QLabel("Automate front-line purchases"), 1, 0)
        self.front_line = QtWidgets.QCheckBox()
        self.registerField(FRONTLINE, self.front_line)
        assist_layout.addWidget(self.front_line, 1, 1, Qt.AlignRight)

        assist_layout.addWidget(QtWidgets.QLabel("Automate aircraft purchases"), 2, 0)
        self.aircraft = QtWidgets.QCheckBox()
        self.registerField(AIRCRAFT, self.aircraft)
        assist_layout.addWidget(self.aircraft, 2, 1, Qt.AlignRight)

        self.setLayout(layout)

    def set_campaign_values(self, campaign: Campaign) -> None:
        self.player_budget.starting_money.setValue(campaign.recommended_player_money)
        self.enemy_budget.starting_money.setValue(campaign.recommended_enemy_money)
        self.player_income.spinner.setValue(
            int(campaign.recommended_player_income_multiplier * 10)
        )
        self.enemy_income.spinner.setValue(
            int(campaign.recommended_enemy_income_multiplier * 10)
        )
        s = campaign.settings
        self.runway_repairs.setChecked(s.get(RUNWAY_REPAIR, False))
        self.front_line.setChecked(s.get(FRONTLINE, False))
        self.aircraft.setChecked(s.get(AIRCRAFT, False))


class GeneratorOptions(QtWidgets.QWizardPage):
    def __init__(self, campaign: Campaign, parent=None):
        super().__init__(parent)

        self.setTitle("Generator settings")
        self.setSubTitle("\nOptions affecting the generation of the game.")
        self.setPixmap(
            QtWidgets.QWizard.LogoPixmap,
            QtGui.QPixmap("./resources/ui/wizard/logo1.png"),
        )

        # Campaign settings
        generatorSettingsGroup = QtWidgets.QGroupBox("Generator Settings")
        self.no_carrier = QtWidgets.QCheckBox()
        self.registerField("no_carrier", self.no_carrier)
        self.no_lha = QtWidgets.QCheckBox()
        self.registerField("no_lha", self.no_lha)
        self.supercarrier = QtWidgets.QCheckBox()
        self.registerField(SUPER_CARRIER, self.supercarrier)
        self.no_player_navy = QtWidgets.QCheckBox()
        self.registerField("no_player_navy", self.no_player_navy)
        self.no_enemy_navy = QtWidgets.QCheckBox()
        self.registerField("no_enemy_navy", self.no_enemy_navy)
        self.desired_player_mission_duration = TimeInputs(
            DEFAULT_MISSION_LENGTH, minimum=30, maximum=150
        )
        self.registerField(MISSION_LENGTH, self.desired_player_mission_duration.spinner)

        generatorLayout = QtWidgets.QGridLayout()
        generatorLayout.addWidget(QtWidgets.QLabel("No Aircraft Carriers"), 1, 0)
        generatorLayout.addWidget(self.no_carrier, 1, 1)
        generatorLayout.addWidget(QtWidgets.QLabel("No LHA"), 2, 0)
        generatorLayout.addWidget(self.no_lha, 2, 1)
        generatorLayout.addWidget(QtWidgets.QLabel("Use Supercarrier module"), 3, 0)
        generatorLayout.addWidget(self.supercarrier, 3, 1)
        generatorLayout.addWidget(QtWidgets.QLabel("No Player Navy"), 4, 0)
        generatorLayout.addWidget(self.no_player_navy, 4, 1)
        generatorLayout.addWidget(QtWidgets.QLabel("No Enemy Navy"), 5, 0)
        generatorLayout.addWidget(self.no_enemy_navy, 5, 1)
        generatorLayout.addWidget(QtWidgets.QLabel("Desired mission duration"), 6, 0)
        generatorLayout.addLayout(self.desired_player_mission_duration, 7, 0)
        generatorSettingsGroup.setLayout(generatorLayout)

        modSettingsGroup = QtWidgets.QGroupBox("Mod Settings")
        self.a4_skyhawk = QtWidgets.QCheckBox()
        self.registerField("a4_skyhawk", self.a4_skyhawk)
        self.a6a_intruder = QtWidgets.QCheckBox()
        self.registerField("a6a_intruder", self.a6a_intruder)
        self.a7e_corsair2 = QtWidgets.QCheckBox()
        self.registerField("a7e_corsair2", self.a6a_intruder)
        self.hercules = QtWidgets.QCheckBox()
        self.registerField("hercules", self.hercules)
        self.uh_60l = QtWidgets.QCheckBox()
        self.registerField("uh_60l", self.uh_60l)
        self.f4bc_phantom = QtWidgets.QCheckBox()
        self.registerField("f4bc_phantom", self.f4bc_phantom)
        self.f15d_baz = QtWidgets.QCheckBox()
        self.registerField("f15d_baz", self.f15d_baz)
        self.f_16_idf = QtWidgets.QCheckBox()
        self.registerField("f_16_idf", self.f_16_idf)
        self.fa_18efg = QtWidgets.QCheckBox()
        self.registerField("fa_18efg", self.fa_18efg)
        self.f22_raptor = QtWidgets.QCheckBox()
        self.registerField("f22_raptor", self.f22_raptor)
        self.f84g_thunderjet = QtWidgets.QCheckBox()
        self.registerField("f84g_thunderjet", self.f84g_thunderjet)
        self.f100_supersabre = QtWidgets.QCheckBox()
        self.registerField("f100_supersabre", self.f100_supersabre)
        self.f104_starfighter = QtWidgets.QCheckBox()
        self.registerField("f104_starfighter", self.f104_starfighter)
        self.f105_thunderchief = QtWidgets.QCheckBox()
        self.registerField("f105_thunderchief", self.f105_thunderchief)
        self.jas39_gripen = QtWidgets.QCheckBox()
        self.registerField("jas39_gripen", self.jas39_gripen)
        self.su30_flanker_h = QtWidgets.QCheckBox()
        self.registerField("su30_flanker_h", self.su30_flanker_h)
        self.su57_felon = QtWidgets.QCheckBox()
        self.registerField("su57_felon", self.su57_felon)
        self.ov10a_bronco = QtWidgets.QCheckBox()
        self.registerField("ov10a_bronco", self.ov10a_bronco)
        self.frenchpack = QtWidgets.QCheckBox()
        self.registerField("frenchpack", self.frenchpack)
        self.high_digit_sams = QtWidgets.QCheckBox()
        self.registerField("high_digit_sams", self.high_digit_sams)
        self.swedishmilitaryassetspack = QtWidgets.QCheckBox()
        self.registerField("swedishmilitaryassetspack", self.swedishmilitaryassetspack)
        self.SWPack = QtWidgets.QCheckBox()
        self.registerField("SWPack", self.SWPack)

        modHelpText = QtWidgets.QLabel(
            "<p>Select the mods you have installed. If your chosen factions support them, you'll be able to use these mods in your campaign.</p>"
        )
        modHelpText.setAlignment(Qt.AlignCenter)

        modLayout = QtWidgets.QGridLayout()
        modLayout_row = 1

        mod_pairs = [
            ("A-4E Skyhawk (v2.1.0)", self.a4_skyhawk),
            ("A-6A Intruder (v2.7.5.01)", self.a6a_intruder),
            ("A-7E Corsair II", self.a7e_corsair2),
            ("C-130J-30 Super Hercules", self.hercules),
            (
                "F-4B/C Phantom II (v2.8.1.01 Standalone + 29Jan23 Patch)",
                self.f4bc_phantom,
            ),
            ("F-15D Baz (v1.0)", self.f15d_baz),
            ("F-16I Sufa & F-16D (v3.6 by IDF Mods Project)", self.f_16_idf),
            ("F/A-18E/F/G Super Hornet (version 2.1)", self.fa_18efg),
            ("F-22A Raptor", self.f22_raptor),
            ("F-84G Thunderjet (v2.5.7.01)", self.f84g_thunderjet),
            ("F-100 Super Sabre (v2.7.18.30765 patch 20.10.22)", self.f100_supersabre),
            ("F-104 Starfighter (v2.7.11.222.01)", self.f104_starfighter),
            ("F-105 Thunderchief (v2.7.12.23x)", self.f105_thunderchief),
            ("Frenchpack", self.frenchpack),
            ("High Digit SAMs", self.high_digit_sams),
            ("Swedish Military Assets pack (1.10)", self.swedishmilitaryassetspack),
            ("JAS 39 Gripen (v1.8.5-beta)", self.jas39_gripen),
            ("OV-10A Bronco", self.ov10a_bronco),
            ("Su-30 Flanker-H (V2.01B)", self.su30_flanker_h),
            ("Su-57 Felon", self.su57_felon),
            ("UH-60L Black Hawk (v1.3.1)", self.uh_60l),
            ("Star Wars Modpack 2.54+", self.SWPack),
        ]

        for i in range(len(mod_pairs)):
            if i % 15 == 0:
                modLayout_row = 1
            col = 2 * (i // 15)
            if i % 5 == 0:
                # Section break here for readability
                modLayout.addWidget(QtWidgets.QWidget(), modLayout_row, col)
                modLayout_row += 1
            label, cb = mod_pairs[i]
            modLayout.addWidget(QLabel(label), modLayout_row, col)
            modLayout.addWidget(cb, modLayout_row, col + 1)
            modLayout_row += 1

        modSettingsGroup.setLayout(modLayout)

        mlayout = QVBoxLayout()
        mlayout.addWidget(generatorSettingsGroup)
        mlayout.addWidget(modSettingsGroup)
        mlayout.addWidget(modHelpText)
        self.setLayout(mlayout)
        self.update_settings(campaign)

    def update_settings(self, campaign: Campaign) -> None:
        s = campaign.settings

        self.no_carrier.setChecked(s.get("no_carrier", False))
        self.no_lha.setChecked(s.get("no_lha", False))
        self.supercarrier.setChecked(s.get(SUPER_CARRIER, False))
        self.no_player_navy.setChecked(s.get("no_player_navy", False))
        self.no_enemy_navy.setChecked(s.get("no_enemy_navy", False))
        self.desired_player_mission_duration.spinner.setValue(s.get(MISSION_LENGTH, 60))

        self.a4_skyhawk.setChecked(s.get("a4_skyhawk", False))
        self.a6a_intruder.setChecked(s.get("a6a_intruder", False))
        self.hercules.setChecked(s.get("hercules", False))
        self.uh_60l.setChecked(s.get("uh_60l", False))
        self.f4bc_phantom.setChecked(s.get("f4bc_phantom", False))
        self.f15d_baz.setChecked(s.get("f15d_baz", False))
        self.f_16_idf.setChecked(s.get("f_16_idf", False))
        self.fa_18efg.setChecked(s.get("fa_18efg", False))
        self.f22_raptor.setChecked(s.get("f22_raptor", False))
        self.f84g_thunderjet.setChecked(s.get("f84g_thunderjet", False))
        self.f100_supersabre.setChecked(s.get("f100_supersabre", False))
        self.f104_starfighter.setChecked(s.get("f104_starfighter", False))
        self.f105_thunderchief.setChecked(s.get("f105_thunderchief", False))
        self.jas39_gripen.setChecked(s.get("jas39_gripen", False))
        self.su30_flanker_h.setChecked(s.get("su30_flanker_h", False))
        self.su57_felon.setChecked(s.get("su57_felon", False))
        self.ov10a_bronco.setChecked(s.get("ov10a_bronco", False))
        self.frenchpack.setChecked(s.get("frenchpack", False))
        self.high_digit_sams.setChecked(s.get("high_digit_sams", False))
        self.swedishmilitaryassetspack.setChecked(
            s.get("swedishmilitaryassetspack", False)
        )


class ConclusionPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(ConclusionPage, self).__init__(parent)

        self.setTitle("Conclusion")
        self.setSubTitle("\n\n")
        self.setPixmap(
            QtWidgets.QWizard.WatermarkPixmap,
            QtGui.QPixmap("./resources/ui/wizard/watermark2.png"),
        )

        self.label = QtWidgets.QLabel(
            "Click 'Finish' to generate and start the new game."
        )
        self.label.setWordWrap(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
