from __future__ import unicode_literals, annotations

from datetime import datetime
from typing import List, Optional, Tuple

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Signal, QDate, QPoint, QItemSelectionModel, Qt, QModelIndex
from PySide6.QtGui import QStandardItem, QPixmap, QStandardItemModel
from PySide6.QtWidgets import (
    QCheckBox,
    QTextBrowser,
    QTextEdit,
    QLabel,
    QListView,
    QAbstractItemView,
)

from game.campaignloader import Campaign
from qt_ui.liberation_install import get_dcs_install_directory
from qt_ui.widgets.QLiberationCalendar import QLiberationCalendar
from qt_ui.windows.newgame.WizardPages.QFactionSelection import FactionSelection
from qt_ui.windows.newgame.jinja_env import jinja_env

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
            QtWidgets.QWizard.WizardPixmap.LogoPixmap,
            QtGui.QPixmap("./resources/ui/wizard/logo1.png"),
        )

        self.setPixmap(
            QtWidgets.QWizard.WizardPixmap.WatermarkPixmap,
            QtGui.QPixmap("./resources/ui/wizard/watermark3.png"),
        )

        # List of campaigns
        self.show_incompatible_campaigns_checkbox = QCheckBox(
            text="Show incompatible campaigns"
        )
        self.show_incompatible_campaigns_checkbox.setChecked(False)

        # Filter and Sort Controls
        filter_sort_group = QtWidgets.QGroupBox("Filter && Sort Campaigns")
        filter_sort_layout = QtWidgets.QGridLayout()
        filter_sort_layout.setColumnStretch(1, 1)

        # Get unique values for filters
        all_versions = set()
        all_maps = set()

        for campaign in campaigns:
            all_versions.add(campaign.version)
            all_maps.add(campaign.data.get("theater", ""))

        # Version filter
        filter_sort_layout.addWidget(QtWidgets.QLabel("Version:"), 0, 0)
        self.version_filter = QtWidgets.QComboBox()
        self.version_filter.addItem("All Versions", None)
        for version in sorted(all_versions, reverse=True):  # Newest first
            if version != (0, 0):  # Skip unknown versions
                self.version_filter.addItem(f"v{version[0]}.{version[1]}", version)
        self.version_filter.currentTextChanged.connect(self.on_filter_changed)
        filter_sort_layout.addWidget(self.version_filter, 0, 1)

        # Map filter
        filter_sort_layout.addWidget(QtWidgets.QLabel("Map:"), 1, 0)
        self.map_filter = QtWidgets.QComboBox()
        self.map_filter.addItem("All Maps", "")
        for map_name in sorted(all_maps):
            if map_name:  # Skip empty map names
                self.map_filter.addItem(map_name, map_name)
        self.map_filter.currentTextChanged.connect(self.on_filter_changed)
        filter_sort_layout.addWidget(self.map_filter, 1, 1)

        # Sort option
        filter_sort_layout.addWidget(QtWidgets.QLabel("Sort by:"), 2, 0)
        self.sort_option = QtWidgets.QComboBox()
        self.sort_option.addItems(["Name", "Version", "Performance"])
        self.sort_option.currentTextChanged.connect(self.on_filter_changed)
        filter_sort_layout.addWidget(self.sort_option, 2, 1)

        filter_sort_layout.addWidget(
            self.show_incompatible_campaigns_checkbox, 3, 0, 1, 2
        )

        filter_sort_group.setLayout(filter_sort_layout)

        self.campaignList = QCampaignList(
            campaigns, self.show_incompatible_campaigns_checkbox.isChecked()
        )
        self.show_incompatible_campaigns_checkbox.toggled.connect(
            self.on_filter_changed
        )

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
        self.invertMap = QtWidgets.QCheckBox()
        self.invertMap.stateChanged.connect(self.on_invert_map)
        self.registerField("invertMap", self.invertMap)
        mapSettingsLayout.addWidget(QtWidgets.QLabel("Invert Map"), 0, 0)
        mapSettingsLayout.addWidget(self.invertMap, 0, 1)
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
            if campaign is None:
                self.campaignMapDescription.setText("No campaign selected")
                self.performanceText.setText("No campaign selected")
                return

            self.campaignMapDescription.setText(template.render({"campaign": campaign}))
            self.faction_selection.setDefaultFactions(campaign)
            if self.invertMap.isChecked():
                self.on_invert_map()
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
            self.campaignList.indexAt(QPoint(1, 1)),
            QItemSelectionModel.SelectionFlag.Rows,
        )

        self.campaignList.selectionModel().selectionChanged.connect(
            on_campaign_selected
        )
        on_campaign_selected()

        docsText = QtWidgets.QLabel(
            "<p>Want more campaigns? You can "
            '<a href="https://github.com/dcs-retribution/dcs-retribution/wiki/Campaign-maintenance"><span style="color:#FFFFFF;">offer to help</span></a>, '
            '<a href="https://github.com/dcs-retribution/dcs-retribution/wiki/Community-campaigns"><span style="color:#FFFFFF;">play a community campaign</span></a>, '
            'or <a href="https://github.com/dcs-retribution/dcs-retribution/wiki/Custom-Campaigns"><span style="color:#FFFFFF;">create your own</span></a>.'
            "</p>"
        )
        docsText.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        layout.addWidget(filter_sort_group, 0, 0, 1, 1)
        layout.addWidget(self.campaignList, 1, 0, 5, 1)
        layout.addWidget(docsText, 6, 0, 1, 1)
        layout.addWidget(self.campaignMapDescription, 0, 1, 1, 1)
        layout.addWidget(self.performanceText, 1, 1, 1, 1)
        layout.addWidget(mapSettingsGroup, 2, 1, 1, 1)
        layout.addWidget(timeGroup, 3, 1, 3, 1)
        self.setLayout(layout)

    def on_filter_changed(self) -> None:
        """Handle changes in filter or sort options."""
        version_filter = self.version_filter.currentData()
        map_filter = self.map_filter.currentData() or ""
        sort_option = self.sort_option.currentText()

        # Apply filters and sort
        self.campaignList.set_filters(version_filter, map_filter)
        self.campaignList.set_sort_option(sort_option)
        self.campaignList.setup_content(
            show_incompatible=self.show_incompatible_campaigns_checkbox.isChecked()
        )

    def on_invert_map(self) -> None:
        blue = self.faction_selection.blueFactionSelect.currentIndex()
        red = self.faction_selection.redFactionSelect.currentIndex()
        self.faction_selection.blueFactionSelect.setCurrentIndex(red)
        self.faction_selection.redFactionSelect.setCurrentIndex(blue)
        self.faction_selection.updateUnitRecap()


class QCampaignItem(QStandardItem):
    def __init__(self, campaign: Campaign) -> None:
        super(QCampaignItem, self).__init__()
        self.setData(campaign, QCampaignList.CampaignRole)

        # Define terrain icon path from the DCS installation directory by default
        dcs_path = get_dcs_install_directory()
        icon_path = dcs_path / campaign.menu_thumbnail_dcs_relative_path

        # If the path does not exist (user does not have the terrain installed),
        # use the old icons as fallback to avoid an ugly campaign list with missing icons
        if not icon_path.exists():
            icon_path = campaign.fallback_icon_path

        self.setIcon(QtGui.QIcon(QPixmap(str(icon_path))))
        self.setEditable(False)
        if campaign.is_compatible:
            name = campaign.name
        else:
            name = f"[INCOMPATIBLE] {campaign.name}"
        self.setText(name)


class QCampaignList(QListView):
    CampaignRole = Qt.ItemDataRole.UserRole

    def __init__(self, campaigns: list[Campaign], show_incompatible: bool) -> None:
        super(QCampaignList, self).__init__()
        self.campaign_model = QStandardItemModel(self)
        self.setModel(self.campaign_model)
        self.setMinimumWidth(250)
        self.setMinimumHeight(350)
        self.campaigns = campaigns
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)

        # Filter and sort settings
        self.current_version_filter: Optional[Tuple[int, int]] = None
        self.current_map_filter = ""
        self.current_sort_option = "Name"

        self.setup_content(show_incompatible)

    @property
    def selected_campaign(self) -> Optional[Campaign]:
        return self.currentIndex().data(QCampaignList.CampaignRole)

    def set_filters(
        self,
        version_filter: Optional[Tuple[int, int]] = None,
        map_filter: str = "",
    ) -> None:
        """Set the filter criteria for campaigns."""
        self.current_version_filter = version_filter
        self.current_map_filter = map_filter

    def set_sort_option(self, sort_option: str) -> None:
        """Set the sort option for campaigns."""
        self.current_sort_option = sort_option

    def _filter_campaign(self, campaign: Campaign) -> bool:
        """Check if a campaign passes all current filters."""
        if (
            self.current_version_filter is not None
            and campaign.version != self.current_version_filter
        ):
            return False

        if self.current_map_filter and self.current_map_filter != campaign.data.get(
            "theater", ""
        ):
            return False

        return True

    def _sort_campaigns(self, campaigns: list[Campaign]) -> list[Campaign]:
        """Sort campaigns based on current sort option."""
        if self.current_sort_option == "Name":
            return sorted(campaigns, key=lambda c: c.name.lower())
        elif self.current_sort_option == "Version":
            return sorted(
                campaigns, key=lambda c: c.version, reverse=True
            )  # Newest first
        elif self.current_sort_option == "Performance":
            return sorted(campaigns, key=lambda c: c.performance)
        else:
            return campaigns

    def setup_content(self, show_incompatible: bool = False) -> None:
        self.selectionModel().blockSignals(True)
        try:
            self.campaign_model.clear()

            # Filter campaigns
            filtered_campaigns = []
            for campaign in self.campaigns:
                if (
                    show_incompatible or campaign.is_compatible
                ) and self._filter_campaign(campaign):
                    filtered_campaigns.append(campaign)

            # Sort campaigns
            sorted_campaigns = self._sort_campaigns(filtered_campaigns)

            # Add to model
            for campaign in sorted_campaigns:
                item = QCampaignItem(campaign)
                self.campaign_model.appendRow(item)
        finally:
            self.selectionModel().blockSignals(False)

        # Select first item if available
        if self.campaign_model.rowCount() > 0:
            self.selectionModel().setCurrentIndex(
                self.campaign_model.index(0, 0, QModelIndex()),
                QItemSelectionModel.SelectionFlag.Select,
            )
