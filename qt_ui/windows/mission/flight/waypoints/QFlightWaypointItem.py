from PySide6.QtGui import QStandardItem, Qt

from game.ato.flightwaypoint import FlightWaypoint


class QWaypointItem(QStandardItem):
    def __init__(self, point: FlightWaypoint, number):
        super(QWaypointItem, self).__init__()
        self.setData(point, Qt.UserRole)
        self.number = number
        self.setText("{:<16}".format(point.pretty_name))
        self.setEditable(True)
