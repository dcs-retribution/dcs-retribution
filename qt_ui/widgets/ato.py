"""Widgets for displaying air tasking orders."""
import logging
from copy import deepcopy
from typing import Optional

from PySide6.QtCore import (
    QItemSelectionModel,
    QModelIndex,
    QSize,
    Qt,
)
from PySide6.QtGui import (
    QContextMenuEvent,
    QAction,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListView,
    QMenu,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QMessageBox,
    QCheckBox,
)

from game.ato.flight import Flight
from game.ato.package import Package
from game.server import EventStream
from game.sim import GameUpdateEvents
from .QLabeledWidget import QLabeledWidget
from ..delegates import TwoColumnRowDelegate
from ..models import AtoModel, GameModel, NullListModel, PackageModel


class FlightDelegate(TwoColumnRowDelegate):
    def __init__(self, package: Package) -> None:
        super().__init__(rows=3, columns=2, font_size=10)
        self.package = package

    @staticmethod
    def flight(index: QModelIndex) -> Flight:
        return index.data(PackageModel.FlightRole)

    def text_for(self, index: QModelIndex, row: int, column: int) -> str:
        flight = self.flight(index)
        if (row, column) == (0, 0):
            return f"{flight}"
        elif (row, column) == (0, 1):
            clients = self.num_clients(index)
            return f"Player Slots: {clients}" if clients else ""
        elif (row, column) == (1, 0):
            origin = flight.departure.name
            if flight.arrival != flight.departure:
                return f"From {origin} to {flight.arrival.name}"
            return f"From {origin}"
        elif (row, column) == (1, 1):
            missing_pilots = flight.missing_pilots
            return f"Missing pilots: {flight.missing_pilots}" if missing_pilots else ""
        elif (row, column) == (2, 0):
            return flight.state.description.title()
        return ""

    def num_clients(self, index: QModelIndex) -> int:
        flight = self.flight(index)
        return flight.client_count


class QFlightList(QListView):
    """List view for displaying the flights of a package."""

    def __init__(
        self, game_model: GameModel, package_model: Optional[PackageModel]
    ) -> None:
        super().__init__()
        self.game_model = game_model
        self.package_model = package_model
        self.set_package(package_model)
        if package_model is not None:
            self.setItemDelegate(FlightDelegate(package_model.package))
        self.setIconSize(QSize(91, 24))
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.doubleClicked.connect(self.on_double_click)

    def set_package(self, model: Optional[PackageModel]) -> None:
        """Sets the package model to display."""
        if model is None:
            self.disconnect_model()
        else:
            self.package_model = model
            self.setItemDelegate(FlightDelegate(model.package))
            self.setModel(model)
            # noinspection PyUnresolvedReferences
            model.deleted.connect(self.disconnect_model)
            self.selectionModel().setCurrentIndex(
                model.index(0, 0, QModelIndex()),
                QItemSelectionModel.SelectionFlag.Select,
            )

    def disconnect_model(self) -> None:
        """Clears the listview of any model attachments.

        Displays an empty list until set_package is called with a valid model.
        """
        model = self.model()
        if model is not None and isinstance(model, PackageModel):
            model.deleted.disconnect(self.disconnect_model)
        self.setModel(NullListModel())

    @property
    def selected_item(self) -> Optional[Flight]:
        """Returns the selected flight, if any."""
        index = self.currentIndex()
        if not index.isValid():
            return None
        return self.package_model.flight_at_index(index)

    def on_double_click(self, index: QModelIndex) -> None:
        if not index.isValid():
            return
        self.edit_flight(index)

    def edit_flight(self, index: QModelIndex) -> None:
        from qt_ui.dialogs import Dialog

        Dialog.open_edit_flight_dialog(
            self.package_model,
            self.package_model.flight_at_index(index),
            parent=self.window(),
        )

    def clone_flight(self, index: QModelIndex) -> None:
        flight = self.package_model.flight_at_index(index)
        try:
            clone = Flight.clone_flight(flight)
        except ValueError as ve:
            QMessageBox.critical(
                None,
                "Can't clone flight!",
                f"Insufficient aircraft to clone flight:\n\n{ve}",
            )
            return
        self.package_model.add_flight(clone)
        clone.flight_plan.layout = deepcopy(flight.flight_plan.layout)
        EventStream.put_nowait(GameUpdateEvents().new_flight(clone))

    def cancel_or_abort_flight(self, index: QModelIndex) -> None:
        self.package_model.cancel_or_abort_flight_at_index(index)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        index = self.indexAt(event.pos())

        menu = QMenu("Menu")

        edit_action = QAction("Edit")
        edit_action.triggered.connect(lambda: self.edit_flight(index))
        menu.addAction(edit_action)

        delete_action = QAction(f"Delete")
        delete_action.triggered.connect(lambda: self.cancel_or_abort_flight(index))
        menu.addAction(delete_action)

        menu.exec_(event.globalPos())


class QFlightPanel(QGroupBox):
    """The flight display portion of the ATO panel.

    Displays the flights assigned to the selected package, and includes edit and
    delete buttons for flight management.
    """

    def __init__(
        self, game_model: GameModel, package_model: Optional[PackageModel] = None
    ) -> None:
        super().__init__("Flights")
        self.game_model = game_model
        self.package_model = package_model

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.tip = QLabel(
            "To add flights to a package, edit the package by double clicking "
            "it or pressing the edit button."
        )
        self.vbox.addWidget(self.tip)

        self.flight_list = QFlightList(game_model, package_model)
        self.vbox.addWidget(self.flight_list)

        self.button_row = QHBoxLayout()
        self.vbox.addLayout(self.button_row)

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.on_edit)
        self.button_row.addWidget(self.edit_button)

        self.clone_button = QPushButton("Clone")
        self.clone_button.setProperty("style", "btn-success")
        self.clone_button.clicked.connect(self.on_clone)
        self.button_row.addWidget(self.clone_button)

        self.delete_button = QPushButton("Cancel")
        self.delete_button.setProperty("style", "btn-danger")
        self.delete_button.clicked.connect(self.on_cancel_flight)
        self.button_row.addWidget(self.delete_button)

        self.selection_changed.connect(self.on_selection_changed)
        self.on_selection_changed()

    def set_package(self, model: Optional[PackageModel]) -> None:
        """Sets the package model to display."""
        self.package_model = model
        self.flight_list.set_package(model)
        self.selection_changed.connect(self.on_selection_changed)
        self.on_selection_changed()

    @property
    def selection_changed(self):
        """Returns the signal emitted when the flight selection changes."""
        return self.flight_list.selectionModel().selectionChanged

    def on_selection_changed(self) -> None:
        """Updates the status of the edit and delete buttons."""
        index = self.flight_list.currentIndex()
        enabled = index.isValid()
        self.edit_button.setEnabled(enabled)
        self.clone_button.setEnabled(enabled)
        self.delete_button.setEnabled(enabled)
        self.change_map_flight_selection(index)
        delete_text = "Cancel"
        if (flight := self.flight_list.selected_item) is not None:
            if not flight.state.cancelable:
                delete_text = "Abort"
        self.delete_button.setText(delete_text)

    def change_map_flight_selection(self, index: QModelIndex) -> None:
        events = GameUpdateEvents()
        if not index.isValid():
            events.deselect_flight()
        else:
            events.select_flight(self.package_model.flight_at_index(index))
        EventStream.put_nowait(events)

    def on_edit(self) -> None:
        """Opens the flight edit dialog."""
        index = self.flight_list.currentIndex()
        if not index.isValid():
            logging.error(f"Cannot edit flight when no flight is selected.")
            return
        self.flight_list.edit_flight(index)

    def on_clone(self) -> None:
        index = self.flight_list.currentIndex()
        if not index.isValid():
            logging.error(f"Cannot clone flight when no flight is selected.")
            return
        self.flight_list.clone_flight(index)

    def on_cancel_flight(self) -> None:
        """Removes the selected flight from the package."""
        index = self.flight_list.currentIndex()
        if not index.isValid():
            logging.error(f"Cannot delete flight when no flight is selected.")
            return
        self.flight_list.cancel_or_abort_flight(index)


class PackageDelegate(TwoColumnRowDelegate):
    def __init__(self, game_model: GameModel) -> None:
        super().__init__(rows=2, columns=2)
        self.game_model = game_model

    @staticmethod
    def package(index: QModelIndex) -> Package:
        return index.data(AtoModel.PackageRole)

    def text_for(self, index: QModelIndex, row: int, column: int) -> str:
        package = self.package(index)
        if (row, column) == (0, 0):
            string = f"{package.package_description} {package.target.name}"
            if package.custom_name:
                string = string + f" ({package.custom_name})"
            return string
        elif (row, column) == (0, 1):
            clients = self.num_clients(index)
            return f"Player Slots: {clients}" if clients else ""
        elif (row, column) == (1, 0):
            return f"TOT at {package.time_over_target:%H:%M:%S}"
        elif (row, column) == (1, 1):
            unassigned_pilots = self.missing_pilots(index)
            return f"Missing pilots: {unassigned_pilots}" if unassigned_pilots else ""
        return ""

    def num_clients(self, index: QModelIndex) -> int:
        package = self.package(index)
        return sum(f.client_count for f in package.flights)

    def missing_pilots(self, index: QModelIndex) -> int:
        package = self.package(index)
        return sum(f.missing_pilots for f in package.flights)


class QPackageList(QListView):
    """List view for displaying the packages of an ATO."""

    def __init__(self, game_model: GameModel, model: AtoModel) -> None:
        super().__init__()
        self.ato_model = model
        self.setModel(model)
        self.setItemDelegate(PackageDelegate(game_model))
        self.setIconSize(QSize(0, 0))
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.model().rowsInserted.connect(self.on_new_packages)
        self.doubleClicked.connect(self.on_double_click)

    @property
    def selected_item(self) -> Optional[Package]:
        """Returns the selected package, if any."""
        index = self.currentIndex()
        if not index.isValid():
            return None
        return self.ato_model.package_at_index(index)

    def edit_package(self, index: QModelIndex) -> None:
        from qt_ui.dialogs import Dialog

        Dialog.open_edit_package_dialog(self.ato_model.get_package_model(index))

    def clone_package(self, index: QModelIndex) -> None:
        package_model = self.ato_model.get_package_model(index)
        try:
            clone = Package.clone_package(package_model.package)
        except ValueError as ve:
            QMessageBox.critical(
                None,
                "Can't clone package!",
                f"Insufficient aircraft to clone package:\n\n{ve}",
            )
            return
        self.ato_model.add_package(clone)
        events = GameUpdateEvents()
        for f in clone.flights:
            events.new_flight(f)
        EventStream.put_nowait(events)

    def delete_package(self, index: QModelIndex) -> None:
        self.ato_model.cancel_or_abort_package_at_index(index)

    def on_new_packages(self, _parent: QModelIndex, first: int, _last: int) -> None:
        # Select the newly created pacakges. This should only ever happen due to
        # the player saving a new package, so selecting it helps them view/edit
        # it faster.
        self.selectionModel().setCurrentIndex(
            self.model().index(first, 0), QItemSelectionModel.SelectionFlag.Select
        )

    def on_double_click(self, index: QModelIndex) -> None:
        if not index.isValid():
            return
        self.edit_package(index)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        index = self.indexAt(event.pos())

        menu = QMenu("Menu")

        edit_action = QAction("Edit")
        edit_action.triggered.connect(lambda: self.edit_package(index))
        menu.addAction(edit_action)

        delete_action = QAction(f"Delete")
        delete_action.triggered.connect(lambda: self.delete_package(index))
        menu.addAction(delete_action)

        menu.exec_(event.globalPos())


class QPackagePanel(QGroupBox):
    """The package display portion of the ATO panel.

    Displays the package assigned to the player's ATO, and includes edit and
    delete buttons for package management.
    """

    def __init__(self, game_model: GameModel, ato_model: AtoModel) -> None:
        super().__init__("Packages")
        self.ato_model = ato_model
        self.ato_model.layoutChanged.connect(self.on_current_changed)

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.tip = QLabel(
            "To create a new package, right click the mission target on the "
            "map. To target airbase objectives, use\n"
            "the attack button in the airbase view."
        )
        self.vbox.addWidget(self.tip)

        self.package_list = QPackageList(game_model, self.ato_model)
        self.vbox.addWidget(self.package_list)

        self.button_row = QHBoxLayout()
        self.vbox.addLayout(self.button_row)

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.on_edit)
        self.button_row.addWidget(self.edit_button)

        self.clone_button = QPushButton("Clone")
        self.clone_button.setProperty("style", "btn-success")
        self.clone_button.clicked.connect(self.on_clone)
        self.button_row.addWidget(self.clone_button)

        self.delete_button = QPushButton("Cancel/abort")
        self.delete_button.setProperty("style", "btn-danger")
        self.delete_button.clicked.connect(self.on_delete)
        self.button_row.addWidget(self.delete_button)

        self.current_changed.connect(self.on_current_changed)
        self.on_current_changed()

    @property
    def current_changed(self):
        """Returns the signal emitted when the flight selection changes."""
        return self.package_list.selectionModel().currentChanged

    def on_current_changed(self) -> None:
        """Updates the status of the edit and delete buttons."""
        index = self.package_list.currentIndex()
        enabled = index.isValid()
        self.edit_button.setEnabled(enabled)
        self.clone_button.setEnabled(enabled)
        self.delete_button.setEnabled(enabled)
        self.change_map_package_selection(index)

    def change_map_package_selection(self, index: QModelIndex) -> None:
        if not index.isValid():
            EventStream.put_nowait(GameUpdateEvents().deselect_flight())
            return

        package = self.ato_model.get_package_model(index)
        if package.rowCount() == 0:
            EventStream.put_nowait(GameUpdateEvents().deselect_flight())
        else:
            EventStream.put_nowait(
                GameUpdateEvents().select_flight(
                    package.flight_at_index(package.index(0))
                )
            )

    def on_edit(self) -> None:
        """Opens the package edit dialog."""
        index = self.package_list.currentIndex()
        if not index.isValid():
            logging.error(f"Cannot edit package when no package is selected.")
            return
        self.package_list.edit_package(index)

    def on_clone(self) -> None:
        index = self.package_list.currentIndex()
        if not index.isValid():
            logging.error(f"Cannot clone package when no package is selected.")
            return
        self.package_list.clone_package(index)

    def on_delete(self) -> None:
        """Removes the package from the ATO."""
        index = self.package_list.currentIndex()
        if not index.isValid():
            logging.error(f"Cannot delete package when no package is selected.")
            return
        self.package_list.delete_package(index)

    def enable_buttons(self, enabled: bool) -> None:
        self.edit_button.setEnabled(enabled)
        self.clone_button.setEnabled(enabled)
        self.delete_button.setEnabled(enabled)


class QAirTaskingOrderPanel(QSplitter):
    """A split panel for displaying the packages and flights of an ATO.

    Used as the left-bar of the main UI. The top half of the panel displays the
    packages of the player's ATO, and the bottom half displays the flights of
    the selected package.
    """

    def __init__(self, game_model: GameModel) -> None:
        super().__init__(Qt.Orientation.Vertical)
        self.game_model = game_model
        self.ato_model = game_model.ato_model

        # ATO
        self.red_ato_checkbox = QCheckBox()
        self.red_ato_checkbox.toggled.connect(self.on_ato_changed)
        self.red_ato_labeled = QLabeledWidget(
            "Show/Plan OPFOR's ATO: ", self.red_ato_checkbox
        )

        self.ato_group_box = QGroupBox("ATO")
        self.ato_group_box.setLayout(self.red_ato_labeled)
        self.addWidget(self.ato_group_box)

        self.package_panel = QPackagePanel(game_model, self.ato_model)
        self.package_panel.current_changed.connect(self.on_package_change)
        self.addWidget(self.package_panel)

        self.flight_panel = QFlightPanel(game_model)
        self.addWidget(self.flight_panel)

    def on_package_change(self) -> None:
        """Sets the newly selected flight for display in the bottom panel."""
        index = self.package_panel.package_list.currentIndex()
        if index.isValid():
            self.package_panel.enable_buttons(True)
            self.flight_panel.set_package(self.ato_model.get_package_model(index))
        else:
            self.package_panel.enable_buttons(False)
            self.flight_panel.set_package(None)

    def on_ato_changed(self) -> None:
        opfor = self.red_ato_checkbox.isChecked()
        ato_model = (
            self.game_model.red_ato_model if opfor else self.game_model.ato_model
        )
        ato_model.layoutChanged.connect(self.package_panel.on_current_changed)
        self.ato_model = ato_model
        self.package_panel.ato_model = ato_model
        self.package_panel.package_list.ato_model = ato_model
        self.package_panel.package_list.setModel(ato_model)
        self.package_panel.enable_buttons(False)
        self.package_panel.current_changed.connect(self.on_package_change)
        self.flight_panel.flight_list.set_package(None)
        events = GameUpdateEvents().deselect_flight()
        EventStream.put_nowait(events)
        self.game_model.is_ownfor = not opfor
