import json
import logging
import textwrap
import zipfile
from typing import Callable, Optional, Dict

from PySide6 import QtWidgets
from PySide6.QtCore import QItemSelectionModel, QPoint, QSize, Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QDialog,
    QGridLayout,
    QGroupBox,
    QLabel,
    QListView,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QFileDialog,
)

import qt_ui.uiconstants as CONST
from game.game import Game
from game.persistency import settings_dir
from game.server import EventStream
from game.settings import (
    BooleanOption,
    BoundedFloatOption,
    BoundedIntOption,
    ChoicesOption,
    MinutesOption,
    OptionDescription,
    Settings,
)
from game.settings.ISettingsContainer import SettingsContainer
from game.sim import GameUpdateEvents
from qt_ui.widgets.QLabeledWidget import QLabeledWidget
from qt_ui.widgets.spinsliders import FloatSpinSlider, TimeInputs
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.settings.plugins import PluginOptionsPage, PluginsPage


class CheatSettingsBox(QGroupBox):
    def __init__(
        self, sc: SettingsContainer, apply_settings: Callable[[], None]
    ) -> None:
        super().__init__("Cheat Settings")
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.red_ato_checkbox = QCheckBox()
        self.red_ato_checkbox.setChecked(sc.settings.show_red_ato)
        self.red_ato_checkbox.toggled.connect(apply_settings)

        self.frontline_cheat_checkbox = QCheckBox()
        self.frontline_cheat_checkbox.setChecked(sc.settings.enable_frontline_cheats)
        self.frontline_cheat_checkbox.toggled.connect(apply_settings)

        self.base_capture_cheat_checkbox = QCheckBox()
        self.base_capture_cheat_checkbox.setChecked(
            sc.settings.enable_base_capture_cheat
        )
        self.base_capture_cheat_checkbox.toggled.connect(apply_settings)

        self.transfer_cheat_checkbox = QCheckBox()
        self.transfer_cheat_checkbox.setChecked(sc.settings.enable_transfer_cheat)
        self.transfer_cheat_checkbox.toggled.connect(apply_settings)

        self.red_ato = QLabeledWidget("Show Red ATO:", self.red_ato_checkbox)
        self.main_layout.addLayout(self.red_ato)
        self.frontline_cheat = QLabeledWidget(
            "Enable Frontline Cheats:", self.frontline_cheat_checkbox
        )
        self.main_layout.addLayout(self.frontline_cheat)
        self.base_capture_cheat = QLabeledWidget(
            "Enable Base Capture Cheat:", self.base_capture_cheat_checkbox
        )

        self.base_runway_state_cheat_checkbox = QCheckBox()
        self.base_runway_state_cheat_checkbox.setChecked(
            sc.settings.enable_runway_state_cheat
        )
        self.base_runway_state_cheat_checkbox.toggled.connect(apply_settings)
        self.main_layout.addLayout(
            QLabeledWidget(
                "Enable Runway State Cheat:", self.base_runway_state_cheat_checkbox
            )
        )

        self.main_layout.addLayout(self.base_capture_cheat)
        self.transfer_cheat = QLabeledWidget(
            "Enable Instant Squadron Transfer Cheat:", self.transfer_cheat_checkbox
        )
        self.main_layout.addLayout(self.transfer_cheat)

    @property
    def show_red_ato(self) -> bool:
        return self.red_ato_checkbox.isChecked()

    @property
    def show_frontline_cheat(self) -> bool:
        return self.frontline_cheat_checkbox.isChecked()

    @property
    def show_base_capture_cheat(self) -> bool:
        return self.base_capture_cheat_checkbox.isChecked()

    @property
    def show_transfer_cheat(self) -> bool:
        return self.transfer_cheat_checkbox.isChecked()

    @property
    def enable_runway_state_cheat(self) -> bool:
        return self.base_runway_state_cheat_checkbox.isChecked()


class AutoSettingsLayout(QGridLayout):
    def __init__(
        self,
        page: str,
        section: str,
        sc: SettingsContainer,
        write_full_settings: Callable[[], None],
    ) -> None:
        super().__init__()
        self.page = page
        self.section = section
        self.sc = sc
        self.write_full_settings = write_full_settings
        self.settings_map: Dict[str, QWidget] = {}

        self.init_ui()

    def init_ui(self):
        for row, (name, description) in enumerate(
            Settings.fields(self.page, self.section)
        ):
            self.add_label(row, description)
            if isinstance(description, BooleanOption):
                self.add_checkbox_for(row, name, description)
            elif isinstance(description, ChoicesOption):
                self.add_combobox_for(row, name, description)
            elif isinstance(description, BoundedFloatOption):
                self.add_float_spin_slider_for(row, name, description)
            elif isinstance(description, BoundedIntOption):
                self.add_spinner_for(row, name, description)
            elif isinstance(description, MinutesOption):
                self.add_duration_controls_for(row, name, description)
            else:
                raise TypeError(f"Unhandled option type: {description}")

    def add_label(self, row: int, description: OptionDescription) -> None:
        wrapped_title = "<br />".join(textwrap.wrap(description.text, width=55))
        text = f"<strong>{wrapped_title}</strong>"
        if description.detail is not None:
            wrapped = "<br />".join(textwrap.wrap(description.detail, width=55))
            text += f"<br />{wrapped}"
        label = QLabel(text)
        if description.tooltip is not None:
            label.setToolTip(description.tooltip)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.addWidget(label, row, 0)

    def add_checkbox_for(self, row: int, name: str, description: BooleanOption) -> None:
        def on_toggle(value: bool) -> None:
            if description.invert:
                value = not value
            self.sc.settings.__dict__[name] = value
            if description.causes_expensive_game_update:
                self.write_full_settings()

        checkbox = QCheckBox()
        value = self.sc.settings.__dict__[name]
        if description.invert:
            value = not value
        checkbox.setChecked(value)
        checkbox.toggled.connect(on_toggle)
        self.addWidget(checkbox, row, 1, Qt.AlignmentFlag.AlignRight)
        self.settings_map[name] = checkbox

    def add_combobox_for(self, row: int, name: str, description: ChoicesOption) -> None:
        combobox = QComboBox()

        def on_changed(index: int) -> None:
            self.sc.settings.__dict__[name] = combobox.itemData(index)

        for text, value in description.choices.items():
            combobox.addItem(text, value)
        combobox.setCurrentText(
            description.text_for_value(self.sc.settings.__dict__[name])
        )
        combobox.currentIndexChanged.connect(on_changed)
        self.addWidget(combobox, row, 1, Qt.AlignmentFlag.AlignRight)
        self.settings_map[name] = combobox

    def add_float_spin_slider_for(
        self, row: int, name: str, description: BoundedFloatOption
    ) -> None:
        spinner = FloatSpinSlider(
            description.min,
            description.max,
            self.sc.settings.__dict__[name],
            divisor=description.divisor,
        )

        def on_changed() -> None:
            self.sc.settings.__dict__[name] = spinner.value

        spinner.spinner.valueChanged.connect(on_changed)
        self.addLayout(spinner, row, 1, Qt.AlignmentFlag.AlignRight)
        self.settings_map[name] = spinner

    def add_spinner_for(
        self, row: int, name: str, description: BoundedIntOption
    ) -> None:
        def on_changed(value: int) -> None:
            self.sc.settings.__dict__[name] = value
            if description.causes_expensive_game_update:
                self.write_full_settings()

        spinner = QSpinBox()
        spinner.setMinimum(description.min)
        spinner.setMaximum(description.max)
        spinner.setValue(self.sc.settings.__dict__[name])

        spinner.valueChanged.connect(on_changed)
        self.addWidget(spinner, row, 1, Qt.AlignmentFlag.AlignRight)
        self.settings_map[name] = spinner

    def add_duration_controls_for(
        self, row: int, name: str, description: MinutesOption
    ) -> None:
        inputs = TimeInputs(
            self.sc.settings.__dict__[name], description.min, description.max
        )

        def on_changed() -> None:
            self.sc.settings.__dict__[name] = inputs.value

        inputs.spinner.valueChanged.connect(on_changed)
        self.addLayout(inputs, row, 1, Qt.AlignmentFlag.AlignRight)
        self.settings_map[name] = inputs

    def update_from_settings(self) -> None:
        for name, description in Settings.fields(self.page, self.section):
            widget = self.settings_map[name]
            value = self.sc.settings.__dict__[name]
            if isinstance(widget, QCheckBox):
                widget.setChecked(value)
            elif isinstance(widget, QComboBox):
                if (index := widget.findData(value)) > -1:
                    widget.setCurrentIndex(index)
                elif (index := widget.findText(value)) > -1:
                    widget.setCurrentIndex(index)
                else:
                    logging.error(
                        f"Incompatible type '{type(value)}' for ComboBox option {name}"
                    )
            elif isinstance(widget, FloatSpinSlider):
                widget.spinner.setValue(int(value * widget.spinner.divisor))
            elif isinstance(widget, QSpinBox):
                widget.setValue(value)
            elif isinstance(widget, TimeInputs):
                widget.spinner.setValue(value.seconds // 60)


class AutoSettingsGroup(QGroupBox):
    def __init__(
        self,
        page: str,
        section: str,
        sc: SettingsContainer,
        write_full_settings: Callable[[], None],
    ) -> None:
        super().__init__(section)
        self.layout = AutoSettingsLayout(page, section, sc, write_full_settings)
        self.setLayout(self.layout)

    def update_from_settings(self) -> None:
        self.layout.update_from_settings()


class AutoSettingsPageLayout(QVBoxLayout):
    def __init__(
        self,
        page: str,
        sc: SettingsContainer,
        write_full_settings: Callable[[], None],
    ) -> None:
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.widgets = []
        for section in Settings.sections(page):
            self.widgets.append(
                AutoSettingsGroup(page, section, sc, write_full_settings)
            )
            self.addWidget(self.widgets[-1])

    def update_from_settings(self) -> None:
        for w in self.widgets:
            w.update_from_settings()


class AutoSettingsPage(QWidget):
    def __init__(
        self,
        page: str,
        sc: SettingsContainer,
        write_full_settings: Callable[[], None],
    ) -> None:
        super().__init__()
        self.layout = AutoSettingsPageLayout(page, sc, write_full_settings)
        self.setLayout(self.layout)

    def update_from_settings(self) -> None:
        self.layout.update_from_settings()


class QSettingsWindow(QDialog):
    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        self.setLayout(QSettingsWidget(game.settings, game).layout)

        self.setModal(True)
        self.setWindowTitle("Settings")
        self.setWindowIcon(CONST.ICONS["Settings"])
        self.setMinimumSize(840, 480)


class QSettingsWidget(QtWidgets.QWizardPage, SettingsContainer):
    def __init__(self, settings: Settings, game: Optional[Game] = None):
        super().__init__()

        self.settings = game.settings if game else settings
        self.game = game

        self.pages: dict[str, AutoSettingsPage] = {}
        for page in Settings.pages():
            self.pages[page] = AutoSettingsPage(page, self, self.applySettings)

        self.pluginsPage = PluginsPage(self)
        self.pluginsOptionsPage = PluginOptionsPage(self)

        self.updating_ui = False

        self.initUi()

    def initUi(self):
        self.layout = QGridLayout()

        self.categoryList = QListView()
        self.right_layout = QStackedLayout()

        self.categoryList.setMaximumWidth(175)

        self.categoryModel = QStandardItemModel(self.categoryList)

        self.categoryList.setIconSize(QSize(32, 32))

        for name, page in self.pages.items():
            page_item = QStandardItem(name)
            if name in CONST.ICONS:
                page_item.setIcon(CONST.ICONS[name])
            else:
                page_item.setIcon(CONST.ICONS["Generator"])
            page_item.setEditable(False)
            page_item.setSelectable(True)
            self.categoryModel.appendRow(page_item)
            scroll = QScrollArea()
            scroll.setWidget(page)
            scroll.setWidgetResizable(True)
            self.right_layout.addWidget(scroll)

        self.initCheatLayout()
        cheat = QStandardItem("Cheat Menu")
        cheat.setIcon(CONST.ICONS["Cheat"])
        cheat.setEditable(False)
        cheat.setSelectable(True)
        self.categoryModel.appendRow(cheat)
        self.right_layout.addWidget(self.cheatPage)

        plugins = QStandardItem("LUA Plugins")
        plugins.setIcon(CONST.ICONS["Plugins"])
        plugins.setEditable(False)
        plugins.setSelectable(True)
        self.categoryModel.appendRow(plugins)
        self.right_layout.addWidget(self.pluginsPage)

        pluginsOptions = QStandardItem("LUA Plugins Options")
        pluginsOptions.setIcon(CONST.ICONS["PluginsOptions"])
        pluginsOptions.setEditable(False)
        pluginsOptions.setSelectable(True)
        self.categoryModel.appendRow(pluginsOptions)
        scroll = QScrollArea()
        scroll.setWidget(self.pluginsOptionsPage)
        scroll.setWidgetResizable(True)
        self.right_layout.addWidget(scroll)

        self.categoryList.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.categoryList.setModel(self.categoryModel)
        self.categoryList.selectionModel().setCurrentIndex(
            self.categoryList.indexAt(QPoint(1, 1)),
            QItemSelectionModel.SelectionFlag.Select,
        )
        self.categoryList.selectionModel().selectionChanged.connect(
            self.onSelectionChanged
        )

        self.layout.addWidget(self.categoryList, 0, 0, 1, 1)
        self.layout.addLayout(self.right_layout, 0, 1, 5, 1)

        load = QPushButton("Load Settings")
        load.clicked.connect(self.load_settings)
        self.layout.addWidget(load, 1, 0, 1, 1)
        save = QPushButton("Save Settings")
        save.clicked.connect(self.save_settings)
        self.layout.addWidget(save, 2, 0, 1, 1)

        self.setLayout(self.layout)

    def initCheatLayout(self):
        self.cheatPage = QWidget()
        self.cheatLayout = QVBoxLayout()
        self.cheatPage.setLayout(self.cheatLayout)

        self.cheat_options = CheatSettingsBox(self, self.applySettings)
        self.cheatLayout.addWidget(self.cheat_options)

        self.moneyCheatBox = QGroupBox("Money Cheat")
        self.moneyCheatBox.setDisabled(self.game is None)
        self.moneyCheatBox.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.moneyCheatBoxLayout = QGridLayout()
        self.moneyCheatBox.setLayout(self.moneyCheatBoxLayout)

        cheats_amounts = [25, 50, 100, 200, 500, 1000, -25, -50, -100, -200]
        for i, amount in enumerate(cheats_amounts):
            if amount > 0:
                btn = QPushButton("Cheat +" + str(amount) + "M")
                btn.setProperty("style", "btn-success")
            else:
                btn = QPushButton("Cheat " + str(amount) + "M")
                btn.setProperty("style", "btn-danger")
            btn.clicked.connect(self.cheatLambda(amount))
            self.moneyCheatBoxLayout.addWidget(btn, i / 2, i % 2)
        self.cheatLayout.addWidget(self.moneyCheatBox, stretch=1)

    def cheatLambda(self, amount):
        return lambda: self.cheatMoney(amount)

    def cheatMoney(self, amount):
        logging.info("CHEATING FOR AMOUNT : " + str(amount) + "M")
        self.game.blue.budget += amount
        GameUpdateSignal.get_instance().updateGame(self.game)

    def applySettings(self):
        if self.updating_ui:
            return
        self.settings.show_red_ato = self.cheat_options.show_red_ato
        self.settings.enable_frontline_cheats = self.cheat_options.show_frontline_cheat
        self.settings.enable_base_capture_cheat = (
            self.cheat_options.show_base_capture_cheat
        )
        self.settings.enable_transfer_cheat = self.cheat_options.show_transfer_cheat
        self.settings.enable_runway_state_cheat = (
            self.cheat_options.enable_runway_state_cheat
        )

        if self.game:
            events = GameUpdateEvents()
            self.game.compute_unculled_zones(events)
            EventStream.put_nowait(events)
            GameUpdateSignal.get_instance().updateGame(self.game)

    def onSelectionChanged(self) -> None:
        index = self.categoryList.selectionModel().currentIndex().row()
        self.right_layout.setCurrentIndex(index)

    def update_from_settings(self) -> None:
        self.updating_ui = True
        for p in self.pages.values():
            p.update_from_settings()

        self.cheat_options.red_ato_checkbox.setChecked(self.settings.show_red_ato)
        self.cheat_options.base_capture_cheat_checkbox.setChecked(
            self.settings.enable_base_capture_cheat
        )
        self.cheat_options.frontline_cheat_checkbox.setChecked(
            self.settings.enable_frontline_cheats
        )
        self.cheat_options.transfer_cheat_checkbox.setChecked(
            self.settings.enable_transfer_cheat
        )

        self.pluginsPage.update_from_settings()
        self.pluginsOptionsPage.update_from_settings()

        self.updating_ui = False

    def load_settings(self):
        sd = settings_dir()
        if not sd.exists():
            sd.mkdir()
        fd = QFileDialog(caption="Load Settings", directory=str(sd), filter="*.zip")
        if fd.exec_():
            zipfilename = fd.selectedFiles()[0]
            with zipfile.ZipFile(zipfilename, "r") as zf:
                filename = zipfilename.split("/")[-1].replace(".zip", ".json")
                settings = json.loads(
                    zf.read(filename).decode("utf-8"),
                    object_hook=self.settings.obj_hook,
                )
                self.settings.__setstate__(settings)
                self.update_from_settings()

    def save_settings(self):
        sd = settings_dir()
        if not sd.exists():
            sd.mkdir()
        fd = QFileDialog(caption="Save Settings", directory=str(sd), filter="*.zip")
        fd.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        if fd.exec_():
            zipfilename = fd.selectedFiles()[0]
            with zipfile.ZipFile(zipfilename, "w", zipfile.ZIP_DEFLATED) as zf:
                filename = zipfilename.split("/")[-1].replace(".zip", ".json")
                zf.writestr(
                    filename,
                    json.dumps(
                        self.settings.__dict__,
                        indent=2,
                        default=self.settings.default_json,
                    ),
                    zipfile.ZIP_DEFLATED,
                )
