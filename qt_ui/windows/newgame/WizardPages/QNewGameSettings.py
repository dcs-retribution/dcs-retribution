from __future__ import unicode_literals

from PySide6 import QtWidgets, QtGui

from game.campaignloader import Campaign
from game.settings import Settings
from qt_ui.windows.settings.QSettingsWindow import QSettingsWidget


class NewGameSettings(QtWidgets.QWizardPage):
    def __init__(self, campaign: Campaign, parent=None) -> None:
        super().__init__(parent)

        self.setTitle("Campaign options")
        self.setSubTitle(
            "\nAll other options unrelated to campaign generation. Defaults can be changed by overwriting Defualt.zip"
        )
        self.setPixmap(
            QtWidgets.QWizard.WizardPixmap.LogoPixmap,
            QtGui.QPixmap("./resources/ui/wizard/logo1.png"),
        )

        settings = Settings()
        settings.__setstate__(campaign.settings)
        self.settings_widget = QSettingsWidget(settings)
        self.settings_widget.load_default_settings()
        settings = self.settings_widget.settings
        settings.__dict__.update(campaign.settings)
        settings.player_income_multiplier = (
            campaign.recommended_player_income_multiplier
        )
        settings.enemy_income_multiplier = campaign.recommended_enemy_income_multiplier
        self.settings_widget.update_from_settings()
        self.setLayout(self.settings_widget.layout)

    def set_campaign_values(self, c: Campaign):
        sw = self.settings_widget
        sw.settings.__setstate__(c.settings)
        sw.settings.player_income_multiplier = c.recommended_player_income_multiplier
        sw.settings.enemy_income_multiplier = c.recommended_enemy_income_multiplier
        sw.settings.__dict__.update(c.settings)
        sw.update_from_settings()
