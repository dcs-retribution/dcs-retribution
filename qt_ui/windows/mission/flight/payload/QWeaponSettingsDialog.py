from typing import Dict, Any, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QFormLayout,
    QScrollArea,
    QWidget,
    QMessageBox,
)

from dcs.weapon_settings import WeaponSettings, WeaponSetting
from game.data.weapons import Weapon


class QWeaponSettingsDialog(QDialog):
    """Dialog for editing weapon settings."""

    def __init__(
        self,
        weapon: Weapon,
        current_settings: Optional[Dict[str, Any]] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.weapon = weapon
        self.settings_instance = weapon.create_settings(current_settings)

        if self.settings_instance is None:
            QMessageBox.warning(
                self,
                "No Settings",
                f"The weapon {weapon.name} has no configurable settings.",
            )
            self.reject()
            return

        self.setting_widgets: Dict[str, QWidget] = {}
        self.init_ui()

    def init_ui(self) -> None:
        """Initialize the UI."""
        self.setWindowTitle(f"Weapon Settings - {self.weapon.name}")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        layout = QVBoxLayout()

        # Title
        title = QLabel(f"<h3>{self.weapon.name} Settings</h3>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Scrollable settings area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        settings_widget = QWidget()
        self.settings_layout = QFormLayout(settings_widget)
        scroll.setWidget(settings_widget)

        layout.addWidget(scroll)

        # Buttons
        button_layout = QHBoxLayout()

        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(reset_btn)

        button_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Save")
        save_btn.setDefault(True)
        save_btn.clicked.connect(self.accept)
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Populate settings
        self.rebuild_settings()

    def rebuild_settings(self) -> None:
        """Rebuild the settings form based on current visibility."""
        # Clear existing widgets
        while self.settings_layout.count():
            item = self.settings_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.setting_widgets.clear()

        # Add visible settings
        for setting in self.settings_instance.get_visible_settings():
            if (
                setting.max_value and setting.max_value >= 1000000000000
            ):  # TODO: Fix validation settings so we can show these
                continue
            widget = self.create_widget_for_setting(setting)
            if widget:
                label = QLabel(setting.label + ":")
                if setting.read_only:
                    label.setText(label.text() + " (Read-only)")
                self.settings_layout.addRow(label, widget)
                self.setting_widgets[setting.id] = widget

    def create_widget_for_setting(self, setting: WeaponSetting) -> Optional[QWidget]:
        """Create an appropriate widget for a setting."""
        if setting.control == "comboList":
            combo = QComboBox()
            for value_item in setting.values:
                combo.addItem(value_item["dispName"], value_item["id"])

            # Set current value
            current_idx = combo.findData(setting.current_value)
            if current_idx >= 0:
                combo.setCurrentIndex(current_idx)

            combo.setEnabled(not setting.read_only)
            combo.currentIndexChanged.connect(
                lambda: self.on_setting_changed(setting.id, combo.currentData())
            )
            return combo

        elif setting.control == "spinbox":
            spinbox = QSpinBox()
            if setting.min_value is not None:
                spinbox.setMinimum(int(setting.min_value))
            if setting.max_value is not None:
                spinbox.setMaximum(int(setting.max_value))
            spinbox.setValue(int(setting.current_value))
            spinbox.setEnabled(not setting.read_only)
            spinbox.valueChanged.connect(
                lambda val: self.on_setting_changed(setting.id, val)
            )

            # Add dimension/unit label if present
            if setting.dimension:
                widget = QWidget()
                layout = QHBoxLayout(widget)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(spinbox)
                layout.addWidget(QLabel(setting.dimension))
                layout.addStretch()
                return widget
            return spinbox

        elif setting.control == "doubleSpinbox":
            spinbox = QDoubleSpinBox()
            if setting.min_value is not None:
                spinbox.setMinimum(setting.min_value)
            if setting.max_value is not None:
                spinbox.setMaximum(setting.max_value)
            spinbox.setValue(float(setting.current_value))
            spinbox.setDecimals(3)
            spinbox.setEnabled(not setting.read_only)
            spinbox.valueChanged.connect(
                lambda val: self.on_setting_changed(setting.id, val)
            )

            # Add dimension/unit label if present
            if setting.dimension:
                widget = QWidget()
                layout = QHBoxLayout(widget)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(spinbox)
                layout.addWidget(QLabel(setting.dimension))
                layout.addStretch()
                return widget
            return spinbox

        return None

    def on_setting_changed(self, setting_id: str, value: Any) -> None:
        """Handle setting value change."""
        try:
            self.settings_instance.set_value(setting_id, value)
            self.rebuild_settings()
        except Exception as e:
            QMessageBox.warning(
                self,
                "Invalid Value",
                f"Could not set {setting_id} to {value}: {e}",
            )

    def reset_to_defaults(self) -> None:
        """Reset all settings to their default values."""
        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "Are you sure you want to reset all settings to their default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.settings_instance.reset_to_defaults()
            self.rebuild_settings()

    def get_settings_dict(self) -> Dict[str, Any]:
        """Get the current settings as a dictionary."""
        return self.settings_instance.to_dict()
