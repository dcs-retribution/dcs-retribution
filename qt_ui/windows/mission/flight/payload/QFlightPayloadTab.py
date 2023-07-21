from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QComboBox,
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QScrollArea,
    QWidget,
    QSpinBox,
    QSlider,
    QCheckBox,
)

from game import Game
from game.ato.flight import Flight
from game.ato.flightmember import FlightMember
from game.ato.loadouts import Loadout
from qt_ui.widgets.QLabeledWidget import QLabeledWidget
from .QLoadoutEditor import QLoadoutEditor
from .propertyeditor import PropertyEditor


class DcsLoadoutSelector(QComboBox):
    def __init__(self, flight: Flight, member: FlightMember) -> None:
        super().__init__()
        for loadout in Loadout.iter_for(flight):
            self.addItem(loadout.name, loadout)
        self.model().sort(0)
        self.setDisabled(member.loadout.is_custom)
        if member.loadout.is_custom:
            self.setCurrentText(Loadout.default_for(flight).name)
        else:
            self.setCurrentText(member.loadout.name)


class FlightMemberSelector(QSpinBox):
    def __init__(self, flight: Flight, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.flight = flight
        self.setMinimum(0)
        self.setMaximum(flight.count - 1)

    @property
    def selected_member(self) -> FlightMember:
        return self.flight.roster.members[self.value()]


class DcsFuelSelector(QHBoxLayout):
    LBS2KGS_FACTOR = 0.45359237

    def __init__(self, flight: Flight) -> None:
        super().__init__()
        self.flight = flight
        self.unit_changing = False

        self.label = QLabel("Internal Fuel Quantity: ")
        self.addWidget(self.label)

        self.max_fuel = int(flight.unit_type.dcs_unit_type.fuel_max)
        self.fuel = QSlider(Qt.Horizontal)
        self.fuel.setRange(0, self.max_fuel)
        self.fuel.setValue(min(round(self.flight.fuel), self.max_fuel))
        self.fuel.valueChanged.connect(self.on_fuel_change)
        self.addWidget(self.fuel, 1)

        self.fuel_spinner = QSpinBox()
        self.fuel_spinner.setRange(0, self.max_fuel)
        self.fuel_spinner.setValue(self.fuel.value())
        self.fuel_spinner.valueChanged.connect(self.update_fuel_slider)
        self.addWidget(self.fuel_spinner)

        self.unit = QComboBox()
        self.unit.insertItems(0, ["kg", "lbs"])
        self.unit.currentIndexChanged.connect(self.on_unit_change)
        self.unit.setCurrentIndex(1)
        self.addWidget(self.unit)

    def on_fuel_change(self, value: int) -> None:
        self.flight.fuel = value
        if self.unit.currentIndex() == 0:
            self.fuel_spinner.setValue(value)
        elif self.unit.currentIndex() == 1 and not self.unit_changing:
            self.fuel_spinner.setValue(self.kg2lbs(value))

    def update_fuel_slider(self, value: int) -> None:
        if self.unit_changing:
            return
        if self.unit.currentIndex() == 0:
            self.fuel.setValue(value)
        elif self.unit.currentIndex() == 1:
            self.unit_changing = True
            self.fuel.setValue(self.lbs2kg(value))
            self.unit_changing = False

    def on_unit_change(self, index: int) -> None:
        self.unit_changing = True
        if index == 0:
            self.fuel_spinner.setMaximum(self.max_fuel)
            self.fuel_spinner.setValue(self.fuel.value())
        elif index == 1:
            self.fuel_spinner.setMaximum(self.kg2lbs(self.max_fuel))
            self.fuel_spinner.setValue(self.kg2lbs(self.fuel.value()))
        self.unit_changing = False

    def kg2lbs(self, value: int) -> int:
        return round(value / self.LBS2KGS_FACTOR)

    def lbs2kg(self, value: int) -> int:
        return round(value * self.LBS2KGS_FACTOR)


class QFlightPayloadTab(QFrame):
    def __init__(self, flight: Flight, game: Game):
        super(QFlightPayloadTab, self).__init__()
        self.flight = flight
        self.payload_editor = QLoadoutEditor(
            flight, self.flight.roster.members[0], game
        )
        self.payload_editor.toggled.connect(self.on_custom_toggled)
        self.payload_editor.saved.connect(self.on_saved_payload)

        layout = QVBoxLayout()

        self.member_selector = FlightMemberSelector(self.flight, self)
        self.member_selector.valueChanged.connect(self.rebind_to_selected_member)
        layout.addLayout(QLabeledWidget("Flight member:", self.member_selector))
        self.same_loadout_for_all_checkbox = QCheckBox(
            "Use same loadout for all flight members"
        )
        self.same_loadout_for_all_checkbox.setChecked(
            self.flight.use_same_loadout_for_all_members
        )
        self.same_loadout_for_all_checkbox.toggled.connect(self.on_same_loadout_toggled)
        layout.addWidget(self.same_loadout_for_all_checkbox)
        layout.addWidget(
            QLabel(
                "<strong>Warning: AI flights should use the same loadout for all members.</strong>"
            )
        )

        scroll_content = QWidget()
        scrolling_layout = QVBoxLayout()
        scroll_content.setLayout(scrolling_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_content)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(scroll)

        # Docs Link
        docsText = QLabel(
            '<a href="https://github.com/dcs-retribution/dcs-retribution/wiki/Custom-Loadouts"><span style="color:#FFFFFF;">How to create your own default loadout</span></a>'
        )
        docsText.setAlignment(Qt.AlignCenter)
        docsText.setOpenExternalLinks(True)

        self.scroll_area = QScrollArea()
        self.property_editor = QWidget()
        self.property_editor.setLayout(PropertyEditor(self.flight))
        self.scroll_area.setWidget(self.property_editor)
        layout.addWidget(self.scroll_area)

        self.fuel_selector = DcsFuelSelector(flight)
        layout.addLayout(self.fuel_selector)

        self.loadout_selector = DcsLoadoutSelector(flight)
        self.property_editor = PropertyEditor(
            self.flight, self.member_selector.selected_member
        )
        scrolling_layout.addLayout(self.property_editor)
        self.loadout_selector = DcsLoadoutSelector(
            flight, self.member_selector.selected_member
        )
        self.loadout_selector.currentIndexChanged.connect(self.on_new_loadout)
        layout.addWidget(self.loadout_selector)
        layout.addWidget(self.payload_editor, stretch=1)
        layout.addWidget(docsText)

        self.setLayout(layout)

    def resize_for_flight(self) -> None:
        self.member_selector.setMaximum(self.flight.count - 1)

    def reload_from_flight(self) -> None:
        self.loadout_selector.setCurrentText(
            self.member_selector.selected_member.loadout.name
        )

    def rebind_to_selected_member(self) -> None:
        member = self.member_selector.selected_member
        self.property_editor.set_flight_member(member)
        self.loadout_selector.setCurrentText(member.loadout.name)
        self.loadout_selector.setDisabled(member.loadout.is_custom)
        self.payload_editor.set_flight_member(member)
        if self.member_selector.value() != 0:
            self.loadout_selector.setDisabled(
                self.flight.use_same_loadout_for_all_members
            )
            self.payload_editor.setDisabled(
                self.flight.use_same_loadout_for_all_members
            )

    def loadout_at(self, index: int) -> Loadout:
        loadout = self.loadout_selector.itemData(index)
        if loadout is None:
            return Loadout.empty_loadout()
        return loadout

    def current_loadout(self) -> Loadout:
        loadout = self.loadout_selector.currentData()
        if loadout is None:
            return Loadout.empty_loadout()
        return loadout

    def on_new_loadout(self, index: int) -> None:
        self.member_selector.selected_member.loadout = self.loadout_at(index)
        self.payload_editor.reset_pylons()

    def on_custom_toggled(self, use_custom: bool) -> None:
        self.loadout_selector.setDisabled(use_custom)
        member = self.member_selector.selected_member
        member.use_custom_loadout = use_custom
        if use_custom:
            member.loadout = member.loadout.derive_custom("Custom")
        else:
            member.loadout = self.current_loadout()
            self.payload_editor.reset_pylons()

    def on_saved_payload(self, payload_name: str) -> None:
        loadout = self.flight.loadout
        self.loadout_selector.addItem(payload_name, loadout)
        self.loadout_selector.setCurrentIndex(self.loadout_selector.count() - 1)
    
    def on_same_loadout_toggled(self, checked: bool) -> None:
        self.flight.use_same_loadout_for_all_members = checked
        if self.member_selector.value():
            self.loadout_selector.setDisabled(checked)
            self.payload_editor.setDisabled(checked)
        if checked:
            self.flight.roster.use_same_loadout_for_all_members()
            if self.member_selector.value():
                self.rebind_to_selected_member()
