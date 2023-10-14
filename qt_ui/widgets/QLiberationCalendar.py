from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QCalendarWidget


class QLiberationCalendar(QCalendarWidget):
    def __init__(self, parent=None):
        super(QLiberationCalendar, self).__init__(parent)
        self.setVerticalHeaderFormat(
            QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader
        )
        self.setGridVisible(False)

        # Overrride default QCalendar behaviour that is rendering week end days in red
        for d in (
            QtCore.Qt.DayOfWeek.Monday,
            QtCore.Qt.DayOfWeek.Tuesday,
            QtCore.Qt.DayOfWeek.Wednesday,
            QtCore.Qt.DayOfWeek.Thursday,
            QtCore.Qt.DayOfWeek.Friday,
            QtCore.Qt.DayOfWeek.Saturday,
            QtCore.Qt.DayOfWeek.Sunday,
        ):
            fmt = self.weekdayTextFormat(d)
            fmt.setForeground(QtCore.Qt.GlobalColor.darkGray)
            self.setWeekdayTextFormat(d, fmt)

    def paintCell(self, painter, rect, date):
        if date == self.selectedDate():
            painter.save()
            painter.fillRect(rect, QtGui.QColor("#D3D3D3"))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(QtGui.QColor(52, 68, 85))
            r = QtCore.QRect(
                QtCore.QPoint(), min(rect.width(), rect.height()) * QtCore.QSize(1, 1)
            )
            r.moveCenter(rect.center())
            painter.drawEllipse(r)
            painter.setPen(QtGui.QPen(QtGui.QColor("white")))
            painter.drawText(rect, QtCore.Qt.AlignmentFlag.AlignCenter, str(date.day()))
            painter.restore()
        else:
            super(QLiberationCalendar, self).paintCell(painter, rect, date)
