from typing import Optional

from PySide6.QtCore import (
    QEvent,
    QItemSelectionModel,
    QModelIndex,
    QPoint,
    Qt,
    QTime,
    QTimer,
    Signal,
)
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDoubleSpinBox,
    QHeaderView,
    QMessageBox,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QTableView,
    QTimeEdit,
    QWidget,
)

from game.ato.flight import Flight
from game.ato.flightwaypoint import FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.ato.package import Package
from game.utils import Distance
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointItem import QWaypointItem

HEADER_LABELS = ["Name", "Alt (ft)", "Alt Type", "TOT/DEPART"]


class AltitudeEditorDelegate(QStyledItemDelegate):
    def createEditor(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> QDoubleSpinBox:
        editor = QDoubleSpinBox(parent)
        editor.setMinimum(0)
        editor.setMaximum(40000)
        editor.setDecimals(0)
        editor.setSingleStep(1000)
        return editor


class TotEditorDelegate(QStyledItemDelegate):
    def __init__(self, waypoint_list: "QFlightWaypointList", flight: Flight) -> None:
        super().__init__(waypoint_list)
        self.waypoint_list = waypoint_list
        self.flight = flight

    def createEditor(self, parent, option, index) -> QWidget:
        editor = QTimeEdit(parent)
        editor.setDisplayFormat("HH:mm:ss")
        return editor

    def setEditorData(self, editor: QTimeEdit, index) -> None:
        text = (
            (index.data(Qt.ItemDataRole.DisplayRole) or "")
            .replace("Depart ", "")
            .strip()
        )
        qt = QTime.fromString(text, "HH:mm:ss")
        if qt.isValid():
            editor.setTime(qt)

    def setModelData(self, editor: QTimeEdit, model, index) -> None:
        waypoint = index.data(Qt.ItemDataRole.UserRole)
        # Base the date on the package TOT; the user only edits the clock time.
        base = self.flight.package.time_over_target
        t = editor.time()
        desired = base.replace(
            hour=t.hour(), minute=t.minute(), second=t.second(), microsecond=0
        )
        if self.flight.flight_plan.would_invert_order(waypoint, desired):
            waypoints = self.flight.flight_plan.waypoints
            previous = self.flight.flight_plan.chained_tot_for_waypoint(
                waypoints[waypoints.index(waypoint) - 1]
            )
            previous_text = f"{previous:%H:%M:%S}" if previous is not None else "it"
            QMessageBox.warning(
                self.waypoint_list,
                "Invalid time over target",
                f"Time over target must be later than the previous waypoint "
                f"({previous_text}). To place this waypoint earlier, reorder the "
                f"waypoints with Move Up / Move Down instead.",
            )
            return
        self.flight.flight_plan.set_waypoint_tot(waypoint, desired)
        # set_waypoint_tot mutates the flight plan, not the model, so nothing else would
        # repaint the cascaded times or reveal the manual-timing controls. Signal the
        # owner to rebuild the list and refresh its widgets, but defer to the next event
        # loop tick: rebuilding the model (model.clear()) while this edit is still
        # committing is unsafe.
        QTimer.singleShot(0, self.waypoint_list.tot_changed.emit)


class QFlightWaypointList(QTableView):
    tot_changed = Signal()

    def __init__(self, package: Package, flight: Flight):
        super().__init__()
        self._last_waypoint: Optional[FlightWaypoint] = None
        self.package = package
        self.flight = flight

        self.model = QStandardItemModel(self)
        self.model.itemChanged.connect(self.on_changed)
        self.setModel(self.model)
        self.model.setHorizontalHeaderLabels(HEADER_LABELS)

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.update_list()

        self.selectionModel().setCurrentIndex(
            self.indexAt(QPoint(1, 1)), QItemSelectionModel.SelectionFlag.Select
        )

        self.altitude_editor_delegate = AltitudeEditorDelegate(self)
        self.setItemDelegateForColumn(1, self.altitude_editor_delegate)

        self.tot_editor_delegate = TotEditorDelegate(self, self.flight)
        self.setItemDelegateForColumn(3, self.tot_editor_delegate)

    def edit(  # type: ignore[override]
        self,
        index: QModelIndex,
        trigger: QAbstractItemView.EditTrigger,
        event: QEvent,
    ) -> bool:
        if (
            index.column() == 3
            and self.flight.client_count == 0
            and trigger != QAbstractItemView.EditTrigger.NoEditTriggers
        ):
            QMessageBox.information(
                self,
                "AI flight timing",
                "AI flight times over target are scheduled automatically and can't be "
                "edited. Add a player slot to this flight to time it manually.",
            )
            return False
        return super().edit(index, trigger, event)

    def update_list(self) -> None:
        # ignore signals when updating list so on_changed does not fire
        self.model.blockSignals(True)
        try:
            # We need to keep just the row and rebuild the index later because the
            # QModelIndex will not be valid after the model is cleared.
            current_index = self.currentIndex().row()
            self.model.clear()

            self.model.setHorizontalHeaderLabels(HEADER_LABELS)

            waypoints = self.flight.flight_plan.waypoints
            for row, waypoint in enumerate(waypoints):
                self._add_waypoint_row(row, self.flight, waypoint)
            self.selectionModel().setCurrentIndex(
                self.model.index(current_index, 0),
                QItemSelectionModel.SelectionFlag.Select,
            )
            self.model.setVerticalHeaderLabels([str(n) for n in range(len(waypoints))])
            self.verticalHeader().setMaximumWidth(25)

            self.resizeColumnsToContents()
            total_column_width = self.verticalHeader().width() + self.lineWidth()
            for i in range(0, self.model.columnCount()):
                total_column_width += self.columnWidth(i) + self.lineWidth()
            self.setFixedWidth(total_column_width)
        finally:
            # stop ignoring signals
            self.model.blockSignals(False)
            self.update(self.currentIndex())

    def _add_waypoint_row(
        self,
        row: int,
        flight: Flight,
        waypoint: FlightWaypoint,
    ) -> None:
        self.model.insertRow(self.model.rowCount())

        self.model.setItem(row, 0, QWaypointItem(waypoint, row))

        altitude = round(waypoint.alt.feet)
        altitude_item = QStandardItem(f"{altitude}")
        altitude_item.setEditable(True)
        self.model.setItem(row, 1, altitude_item)

        altitude_type = "AGL" if waypoint.alt_type == "RADIO" else "MSL"
        altitude_type_item = QStandardItem(f"{altitude_type}")
        altitude_type_item.setEditable(False)
        self.model.setItem(row, 2, altitude_type_item)

        tot = self.tot_text(flight, waypoint)
        tot_item = QStandardItem(tot)
        editable = flight.client_count > 0 and (
            waypoint.waypoint_type != FlightWaypointType.TAKEOFF
        )
        tot_item.setEditable(editable)
        tot_item.setData(waypoint, Qt.ItemDataRole.UserRole)
        self.model.setItem(row, 3, tot_item)

    def on_changed(self) -> None:
        for i in range(self.model.rowCount()):
            # waypoints materializes a fresh list each access; resolve once per row so the
            # altitude and name edits land on the same waypoint object.
            waypoint = self.flight.flight_plan.waypoints[i]
            altitude_feet = float(self.model.item(i, 1).text())
            waypoint.alt = Distance.from_feet(altitude_feet)
            waypoint.apply_name_edit(self.model.item(i, 0).text())

    def tot_text(
        self,
        flight: Flight,
        waypoint: FlightWaypoint,
    ) -> str:
        if flight.manually_timed and flight.manual_takeoff_time is not None:
            time = flight.flight_plan.effective_tot_for_waypoint(waypoint)
            return f"{time:%H:%M:%S}" if time is not None else ""
        if waypoint.waypoint_type == FlightWaypointType.TAKEOFF:
            self.update_last_tot(flight.flight_plan.takeoff_time())
            self._last_waypoint = waypoint
            return self.takeoff_text(flight)
        prefix = ""
        time = flight.flight_plan.tot_for_waypoint(waypoint)
        if time is None:
            prefix = "Depart "
            time = flight.flight_plan.depart_time_for_waypoint(waypoint)
        if time is None and self._last_waypoint is not None:
            prefix = ""
            timedelta = flight.flight_plan.travel_time_between_waypoints(
                self._last_waypoint, waypoint
            )
            time = self._last_tot + timedelta
        elif time is None:
            return ""
        self.update_last_tot(time)
        self._last_waypoint = waypoint
        return f"{prefix}{time:%H:%M:%S}"

    @staticmethod
    def takeoff_text(flight: Flight) -> str:
        return f"{flight.flight_plan.takeoff_time():%H:%M:%S}"

    def update_last_tot(self, time) -> None:
        if time is not None:
            self._last_tot = time
