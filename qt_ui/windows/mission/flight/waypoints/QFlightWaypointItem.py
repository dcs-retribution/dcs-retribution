from PySide6.QtGui import QStandardItem, Qt

from game.ato.flightwaypoint import FlightWaypoint


class QWaypointItem(QStandardItem):
    def __init__(self, point: FlightWaypoint, number: int) -> None:
        super(QWaypointItem, self).__init__()
        self.setData(point, Qt.ItemDataRole.UserRole)
        self.number = number
        self.setText("{:<16}".format(point.display_name))
        self.setEditable(True)
