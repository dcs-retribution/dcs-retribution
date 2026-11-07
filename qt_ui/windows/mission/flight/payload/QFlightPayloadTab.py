from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QSpinBox,
    QSlider,
    QCheckBox,
    QScrollArea,
)

from game import Game
from game.ato.flight import Flight
from game.ato.flightmember import FlightMember
from game.ato.loadouts import Loadout
from game.missiongenerator.aircraft.modex import (
    MIN_BOARD_NUMBER,
    is_modex_flight,
    max_board_number_lead,
    take_board_number,
)
from qt_ui.blocksignals import block_signals
from qt_ui.widgets.QLabeledWidget import QLabeledWidget
from qt_ui.widgets.combos.QSquadronLiverySelector import SquadronLiverySelector
from .QLoadoutEditor import QLoadoutEditor
from .ownlasercodeinfo import OwnLaserCodeInfo
from .propertyeditor import PropertyEditor
from .weaponlasercodeselector import WeaponLaserCodeSelector


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
        self.setMinimum(1)
        self.setMaximum(flight.count)

    @property
    def selected_member(self) -> FlightMember:
        return self.flight.roster.members[self.value() - 1]


class BoardNumberSelector(QVBoxLayout):
    """Pins the flight's board number: the lead's, with the wingmen following.

    Taking a number another flight of the coalition has pinned moves that
    flight to the next free run, so no two packages wear the same modex.
    """

    def __init__(self, flight: Flight) -> None:
        super().__init__()
        self.flight = flight
        self._moves: list[tuple[Flight, int, int | None]] = []

        row = QHBoxLayout()
        self.enabled = QCheckBox("Set board number")
        self.enabled.setToolTip(
            "Pin the lead's board number (modex). The rest of the flight follows "
            "in order: 105, 106, 107, 108. Unticked, the mission generator "
            "numbers the flight."
        )
        row.addWidget(self.enabled)
        self.number = QSpinBox()
        self.number.setRange(MIN_BOARD_NUMBER, max_board_number_lead(flight.count))
        row.addWidget(self.number)
        row.addStretch(1)
        self.addLayout(row)

        self.summary = QLabel()
        self.summary.setWordWrap(True)
        self.addWidget(self.summary)

        pinned = getattr(flight, "board_number", None)
        with block_signals(self.enabled), block_signals(self.number):
            self.enabled.setChecked(pinned is not None)
            self.number.setValue(pinned if pinned is not None else 100)
        self.number.setEnabled(pinned is not None)
        self.enabled.toggled.connect(self.apply)
        self.number.valueChanged.connect(self.apply)
        self.refresh()

    def _other_flights(self) -> list[Flight]:
        return [
            flight
            for package in self.flight.squadron.coalition.ato.packages
            for flight in package.flights
            if flight is not self.flight
        ]

    def _fit_range(self) -> None:
        with block_signals(self.number):
            self.number.setMaximum(max_board_number_lead(self.flight.count))

    def apply(self) -> None:
        self._fit_range()
        self.number.setEnabled(self.enabled.isChecked())
        self._moves = []
        if not self.enabled.isChecked():
            self.flight.board_number = None
        else:
            self._moves = take_board_number(
                self.flight, self.number.value(), self._other_flights()
            )
        self.refresh()

    def refresh(self) -> None:
        self._fit_range()
        if not self.enabled.isChecked():
            self.summary.setText("Numbered automatically at mission generation.")
            return
        lead = self.number.value()
        numbers = ", ".join(
            f"{lead + offset:03}" for offset in range(self.flight.count)
        )
        lines = [f"Flight: {numbers}."]
        for other, old, new in self._moves:
            where = "automatic" if new is None else f"{new:03}"
            lines.append(
                f"{other} ({other.package.package_description} package, "
                f"{other.package.target.name}) moved from {old:03} to {where}."
            )
        if self.flight.unit_type.dcs_unit_type.id.startswith("F-14"):
            lines.append(
                "The Tomcat's painted number is its livery: a jet shows this "
                "number only where the squadron has a livery painted with it."
            )
        self.summary.setText("\n".join(lines))


class DcsFuelSelector(QHBoxLayout):
    LBS2KGS_FACTOR = 0.45359237

    def __init__(self, flight: Flight) -> None:
        super().__init__()
        self.flight = flight
        self.unit_changing = False

        self.label = QLabel("Internal Fuel Quantity: ")
        self.addWidget(self.label)

        self.max_fuel = int(flight.unit_type.dcs_unit_type.fuel_max)
        self.fuel = QSlider(Qt.Orientation.Horizontal)
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

        hbox = QHBoxLayout()
        self.same_livery_for_all_checkbox = QCheckBox(
            "Use same livery for all flight members"
        )
        self.same_livery_for_all_checkbox.setChecked(
            self.flight.use_same_livery_for_all_members
        )
        self.same_livery_for_all_checkbox.toggled.connect(self.on_same_livery_toggled)
        hbox.addWidget(self.same_livery_for_all_checkbox)
        self.livery_selector = SquadronLiverySelector(
            self.flight.squadron, update_squadron=False
        )
        self.livery_selector.currentIndexChanged.connect(self.on_livery_change)
        hbox.addWidget(self.livery_selector)
        layout.addLayout(hbox)

        # Navy only: the Hornets and Tomcats that wear sequenced modexes.
        self.board_number_selector: BoardNumberSelector | None = None
        if is_modex_flight(self.flight):
            self.board_number_selector = BoardNumberSelector(self.flight)
            layout.addLayout(self.board_number_selector)

        scroll_content = QWidget()
        scrolling_layout = QVBoxLayout()
        scroll_content.setLayout(scrolling_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_content)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(scroll, stretch=1)

        self.own_laser_code_info = OwnLaserCodeInfo(
            game, self.member_selector.selected_member
        )
        scrolling_layout.addLayout(self.own_laser_code_info)

        self.weapon_laser_code_selector = WeaponLaserCodeSelector(
            game, self.member_selector.selected_member, self
        )
        self.own_laser_code_info.assigned_laser_code_changed.connect(
            self.weapon_laser_code_selector.rebuild
        )
        scrolling_layout.addLayout(
            QLabeledWidget(
                "Preset laser code for weapons:", self.weapon_laser_code_selector
            )
        )
        scrolling_layout.addWidget(
            QLabel(
                "Equipped weapons will be pre-configured to the selected laser code at "
                "mission start."
            )
        )

        self.property_editor = PropertyEditor(
            self.flight, self.member_selector.selected_member, game
        )
        scrolling_layout.addLayout(self.property_editor)

        # Docs Link
        docsText = QLabel(
            '<a href="https://github.com/dcs-retribution/dcs-retribution/wiki/Custom-Loadouts"><span style="color:#FFFFFF;">How to create your own default loadout</span></a>'
        )
        docsText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        docsText.setOpenExternalLinks(True)

        self.fuel_selector = DcsFuelSelector(flight)
        layout.addLayout(self.fuel_selector)

        self.loadout_selector = DcsLoadoutSelector(
            flight, self.member_selector.selected_member
        )
        self.loadout_selector.currentIndexChanged.connect(self.on_new_loadout)
        layout.addWidget(self.loadout_selector)
        layout.addWidget(self.payload_editor, stretch=3)
        layout.addWidget(docsText)

        self.setLayout(layout)

    def resize_for_flight(self) -> None:
        self.member_selector.setMaximum(self.flight.count - 1)
        if self.board_number_selector is not None:
            # A longer run can overlap another pin; re-taking it moves that one.
            self.board_number_selector.apply()

    def reload_from_flight(self) -> None:
        self.loadout_selector.setCurrentText(
            self.member_selector.selected_member.loadout.name
        )

    def rebind_to_selected_member(self) -> None:
        member = self.member_selector.selected_member
        self.property_editor.set_flight_member(member)
        self.loadout_selector.setCurrentText(member.loadout.name)
        self.loadout_selector.setDisabled(member.loadout.is_custom)
        self.livery_selector.setCurrentIndex(
            self.livery_selector.findData(member.livery)
        )
        self.payload_editor.set_flight_member(member)
        self.weapon_laser_code_selector.set_flight_member(member)
        self.own_laser_code_info.set_flight_member(member)
        if self.member_selector.value() != 1:
            self.loadout_selector.setDisabled(
                self.flight.use_same_loadout_for_all_members
            )
            self.payload_editor.setDisabled(
                self.flight.use_same_loadout_for_all_members
            )
            self.livery_selector.setDisabled(
                self.flight.use_same_livery_for_all_members
            )
        else:
            self.loadout_selector.setEnabled(True)
            self.payload_editor.setEnabled(True)
            self.livery_selector.setEnabled(True)

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
        loadout = self.loadout_at(index)
        self.member_selector.selected_member.loadout = loadout
        if self.flight.use_same_loadout_for_all_members:
            self.flight.roster.use_same_loadout_for_all_members()
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
        if self.flight.use_same_loadout_for_all_members:
            self.flight.roster.use_same_loadout_for_all_members()

    def on_saved_payload(self, payload_name: str) -> None:
        loadout = self.member_selector.selected_member.loadout
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
        else:
            self.flight.roster.use_distinct_loadouts_for_each_member()

    def on_same_livery_toggled(self, checked: bool) -> None:
        self.flight.use_same_livery_for_all_members = checked
        if self.member_selector.value():
            self.livery_selector.setDisabled(checked)
        if checked:
            self.flight.roster.use_same_livery_for_all_members()
            if self.member_selector.value():
                self.rebind_to_selected_member()

    def on_livery_change(self) -> None:
        livery = self.livery_selector.currentData()
        use_livery_set = self.livery_selector.using_livery_set
        if self.flight.use_same_livery_for_all_members:
            for m in self.flight.roster.members:
                m.livery = livery
                m.use_livery_set = use_livery_set
        else:
            self.member_selector.selected_member.livery = livery
            self.member_selector.selected_member.use_livery_set = use_livery_set
