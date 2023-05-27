from __future__ import unicode_literals

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel

from game.campaignloader import Campaign
from qt_ui.widgets.spinsliders import FloatSpinSlider
from qt_ui.windows.newgame.SettingNames import RUNWAY_REPAIR, FRONTLINE, AIRCRAFT


class NewGameSettings(QtWidgets.QWizardPage):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setTitle("Campaign options")
        self.setSubTitle(
            "\nAll other options unrelated to campaign generation."
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

        new_squadron_rules = QtWidgets.QCheckBox("Enable new squadron rules")
        self.registerField("use_new_squadron_rules", new_squadron_rules)
        economy_layout.addWidget(new_squadron_rules)
        economy_layout.addWidget(
            QLabel(
                "With new squadron rules enabled, squadrons will not be able to exceed a maximum number of aircraft "
                "(configurable), and the campaign will begin with all squadrons at full strength."
            )
        )

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
