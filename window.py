from PySide import QtCore, QtGui
from PySide.QtCore import Qt

from window_ui import Ui_MainWindow

class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.canvas.paintEvent = self.on_canvas_paint_event
        self.ui.scrollArea.resizeEvent = self.on_scroll_area_resize_event

        self.ui.actionZoomIn.triggered.connect(self.on_zoom_in)
        self.ui.actionZoomOut.triggered.connect(self.on_zoom_out)
        self.zoom = 0.9

    def on_canvas_paint_event(self, event):
        painter = QtGui.QPainter(self.ui.canvas)
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0), 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin)
        pen.setCosmetic(True)
        brush = QtGui.QBrush(QtGui.QColor(0xFF, 0xFF, 0x80))
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setWindow(0, 0, 1, 1)
        painter.drawPolygon([QtCore.QPoint(0, 0), QtCore.QPoint(0, 1), QtCore.QPoint(1, 1), QtCore.QPoint(1, 0)])

    def on_scroll_area_resize_event(self, event):
        self.resize_canvas()

    def resize_canvas(self):
        size = min(self.ui.scrollArea.width(), self.ui.scrollArea.height()) * self.zoom
        hmax = self.ui.scrollArea.horizontalScrollBar().maximum()
        hvalue = self.ui.scrollArea.horizontalScrollBar().value()
        vmax = self.ui.scrollArea.verticalScrollBar().maximum()
        vvalue = self.ui.scrollArea.verticalScrollBar().value()

        if hmax:
            x = hvalue / hmax
        else:
            x = 0.5

        if vmax:
            y = vvalue / vmax
        else:
            y = 0.5

        self.ui.canvas.setMinimumSize(QtCore.QSize(size, size))
        self.ui.canvas.setMaximumSize(QtCore.QSize(size, size))

        hmax = self.ui.scrollArea.horizontalScrollBar().maximum()
        vmax = self.ui.scrollArea.verticalScrollBar().maximum()

        self.ui.scrollArea.horizontalScrollBar().setValue(x * hmax)
        self.ui.scrollArea.verticalScrollBar().setValue(y * vmax)

    def on_zoom_in(self):
        self.zoom *= 1.25
        self.resize_canvas()

    def on_zoom_out(self):
        self.zoom /= 1.25
        self.resize_canvas()