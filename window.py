from PySide import QtCore, QtGui
from PySide.QtCore import Qt

from window_ui import Ui_MainWindow

class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.canvas.paintEvent = self.on_canvas_paint_event
        self.ui.canvas.mouseReleaseEvent = self.on_canvas_mouse_release_event
        self.ui.canvas.mouseMoveEvent = self.on_canvas_mouse_move_event
        self.ui.scrollArea.resizeEvent = self.on_scroll_area_resize_event

        self.ui.actionZoomIn.triggered.connect(self.on_zoom_in)
        self.ui.actionZoomOut.triggered.connect(self.on_zoom_out)

        self.ui.canvas.setMouseTracking(True)

        self.zoom = 0.9
        self.points = [(0, 0), (0, 1), (1, 1), (1, 0)]
        self.highlight_point = None
        self.selected_point = None

    def point_to_window(self, point):
        size = min(self.ui.scrollArea.width(), self.ui.scrollArea.height()) * self.zoom
        margin = 10
        return (margin + point[0] * (size - 2 * margin), margin + point[1] * (size - 2 * margin))

    def window_to_point(self, point):
        size = min(self.ui.scrollArea.width(), self.ui.scrollArea.height()) * self.zoom
        margin = 10
        return ((point[0] - margin) / (size - 2 * margin), (point[1] - margin) / (size - 2 * margin))

    def find_point_near(self, mouse_point):
        found_point = None
        size = min(self.ui.scrollArea.width(), self.ui.scrollArea.height()) * self.zoom
        threshold = 10 / size
        for point in self.points:
            dx = mouse_point[0] - point[0]
            dy = mouse_point[1] - point[1]
            distance = dx * dx + dy * dy
            if distance <= threshold * threshold:
                found_point = point
                break
        return found_point

    def on_canvas_paint_event(self, event):
        painter = QtGui.QPainter(self.ui.canvas)
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0), 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin)
        pen.setCosmetic(True)
        brush = QtGui.QBrush(QtGui.QColor(0xFF, 0xFF, 0x80))
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        draw_points = [QtCore.QPoint(*self.point_to_window(point)) for point in self.points]
        painter.drawPolygon(draw_points)

        if self.highlight_point:
            brush = QtGui.QBrush(QtGui.QColor(0x00, 0x00, 0x00))
            painter.setBrush(brush)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QtCore.QPoint(*self.point_to_window(self.highlight_point)), 2, 2)

        if self.selected_point:
            brush = QtGui.QBrush(QtGui.QColor(0xFF, 0x00, 0x00))
            painter.setBrush(brush)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QtCore.QPoint(*self.point_to_window(self.selected_point)), 3, 3)

    def on_canvas_mouse_release_event(self, event):
        mouse_point = self.window_to_point((event.pos().x(), event.pos().y()))
        selected_point = self.find_point_near(mouse_point)
        if selected_point == self.selected_point:
            selected_point = None

        if selected_point != self.selected_point:
            self.selected_point = selected_point
            self.ui.canvas.update()

    def on_canvas_mouse_move_event(self, event):
        mouse_point = self.window_to_point((event.pos().x(), event.pos().y()))
        highlight_point = self.find_point_near(mouse_point)

        if highlight_point != self.highlight_point:
            self.highlight_point = highlight_point
            self.ui.canvas.update()

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