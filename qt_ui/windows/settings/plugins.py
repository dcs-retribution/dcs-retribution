from typing import Dict, List

from PySide6.QtCore import Qt, QLocale
from PySide6.QtWidgets import (
    QCheckBox,
    QGridLayout,
    QGroupBox,
    QLabel,
    QVBoxLayout,
    QWidget,
    QDoubleSpinBox,
    QSpinBox,
)

from game.plugins import LuaPlugin, LuaPluginManager
from game.settings import Settings
from game.settings.ISettingsContainer import SettingsContainer


class PluginsBox(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Plugins")

        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.plugin_map: Dict[str, QCheckBox] = {}

        for row, plugin in enumerate(LuaPluginManager.plugins()):
            if not plugin.show_in_ui:
                continue

            layout.addWidget(QLabel(plugin.name), row, 0)

            checkbox = QCheckBox()
            checkbox.setChecked(plugin.get_value)
            checkbox.toggled.connect(plugin.set_value)
            layout.addWidget(checkbox, row, 1)
            self.plugin_map[plugin.identifier] = checkbox

    def update_from_settings(self, settings: Settings):
        for identifier, enabled in settings.plugins.items():
            if identifier in self.plugin_map:
                self.plugin_map[identifier].setChecked(enabled)


class PluginsPage(QWidget):
    def __init__(self, sc: SettingsContainer) -> None:
        super().__init__()

        self.sc = sc

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.plugins_box = PluginsBox()
        layout.addWidget(self.plugins_box)

    def update_from_settings(self):
        self.plugins_box.update_from_settings(self.sc.settings)


class PluginOptionsBox(QGroupBox):
    def __init__(self, plugin: LuaPlugin) -> None:
        super().__init__(plugin.name)

        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.widgets: Dict[str, QWidget] = {}

        for row, option in enumerate(plugin.options):
            layout.addWidget(QLabel(option.name), row, 0)

            val = option.get_value
            if type(val) == bool:
                checkbox = QCheckBox()
                checkbox.setChecked(val)
                checkbox.toggled.connect(option.set_value)
                layout.addWidget(checkbox, row, 1)
                self.widgets[option.identifier] = checkbox
            elif type(val) == float or type(val) == int:
                if type(val) == float:
                    spinbox = QDoubleSpinBox()
                    spinbox.setSingleStep(0.01)
                    spinbox.setLocale(QLocale.Language.English)
                else:
                    spinbox = QSpinBox()
                spinbox.setMinimum(option.min)
                spinbox.setMaximum(option.max)
                spinbox.setValue(val)
                spinbox.valueChanged.connect(option.set_value)
                layout.addWidget(spinbox, row, 1)
                self.widgets[option.identifier] = spinbox

    def update_from_settings(self, settings: Settings) -> None:
        for identifier in self.widgets:
            value = settings.plugin_option(identifier)
            w = self.widgets[identifier]
            if isinstance(w, QCheckBox):
                w.setChecked(value)
            elif isinstance(w, QDoubleSpinBox) or isinstance(w, QSpinBox):
                w.setValue(value)


class PluginOptionsPage(QWidget):
    def __init__(self, sc: SettingsContainer) -> None:
        super().__init__()

        self.sc = sc

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.pobs: List[PluginOptionsBox] = []

        for plugin in LuaPluginManager.plugins():
            if plugin.options:
                pob = PluginOptionsBox(plugin)
                layout.addWidget(pob)
                self.pobs.append(pob)

    def update_from_settings(self):
        for pob in self.pobs:
            pob.update_from_settings(self.sc.settings)
