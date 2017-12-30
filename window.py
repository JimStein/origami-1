from PySide import QtCore, QtGui
from PySide.QtCore import Qt

from window_ui import Ui_MainWindow

import geo

import math

class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.canvas.paintEvent = self.on_canvas_paint_event
        self.ui.canvas.mouseReleaseEvent = self.on_canvas_mouse_release_event
        self.ui.canvas.mouseMoveEvent = self.on_canvas_mouse_move_event
        self.ui.scrollArea.resizeEvent = self.on_scroll_area_resize_event

        self.ui.actionZoomIn.triggered.connect(self.on_action_zoom_in)
        self.ui.actionZoomOut.triggered.connect(self.on_action_zoom_out)
        self.ui.actionPoints.triggered.connect(self.on_action_points)
        self.ui.actionPointPoint.triggered.connect(self.on_action_point_point)
        self.ui.actionLineLine.triggered.connect(self.on_action_line_line)

        self.ui.canvas.setMouseTracking(True)

        self.zoom = 0.9
        self.points = [geo.Point(0, 0), geo.Point(0, 1), geo.Point(1, 1), geo.Point(1, 0)]
        self.highlight = None
        self.selected = []
        self.lines = []
        self.update_actions()

    def point_to_window(self, point):
        size = min(self.ui.scrollArea.width(), self.ui.scrollArea.height()) * self.zoom
        margin = 10
        return QtCore.QPoint(margin + point.x * (size - 2 * margin), margin + point.y * (size - 2 * margin))

    def window_to_point(self, point):
        size = min(self.ui.scrollArea.width(), self.ui.scrollArea.height()) * self.zoom
        margin = 10
        return geo.Point((point.x() - margin) / (size - 2 * margin), (point.y() - margin) / (size - 2 * margin))

    def find_point_near(self, mouse_point):
        found_point = None
        size = min(self.ui.scrollArea.width(), self.ui.scrollArea.height()) * self.zoom
        threshold = 10 / size
        for point in self.points:
            distance2 = (mouse_point - point).magnitude2()
            if distance2 <= threshold * threshold:
                found_point = point
                break
        return found_point

    def find_segment_near(self, mouse_point):
        found_segment = None
        size = min(self.ui.scrollArea.width(), self.ui.scrollArea.height()) * self.zoom
        threshold = 10 / size
        last_point = self.points[-1]
        for point in self.points:
            segment = geo.Segment(last_point, point)
            line = segment.line()
            offset = (mouse_point - geo.Point(0, 0)) * line.normal

            if abs(offset - line.offset) <= threshold:
                length2 = segment.length2()
                length2a = (mouse_point - point).magnitude2()
                length2b = (mouse_point - last_point).magnitude2()
                if length2a < length2 and length2b < length2:
                    found_segment = segment
                break
            last_point = point
        return found_segment

    def on_canvas_paint_event(self, event):
        painter = QtGui.QPainter(self.ui.canvas)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        def draw_segment(segment):
            draw_points = [self.point_to_window(point) for point in segment.points()]
            painter.drawLine(*draw_points)

        def draw_point(point):
            painter.drawEllipse(self.point_to_window(point), 3, 3)

        def draw_line(line):
            if abs(line.normal.x) > abs(line.normal.y):
                x0 = line.offset / line.normal.x
                x1 = (line.offset - line.normal.y) / line.normal.x
                points = [geo.Point(x0, 0), geo.Point(x1, 1)]
            else:
                y0 = line.offset / line.normal.y
                y1 = (line.offset - line.normal.x) / line.normal.y
                points = [geo.Point(0, y0), geo.Point(1, y1)]
            draw_points = [self.point_to_window(point) for point in points]
            painter.drawLine(*draw_points)

        def draw_polygon(points):
            draw_points = [self.point_to_window(point) for point in points]
            painter.drawPolygon(draw_points)

        pen = QtGui.QPen(QtGui.QColor(0, 0, 0), 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin)
        brush = QtGui.QBrush(QtGui.QColor(0xFF, 0xFF, 0x80))
        painter.setPen(pen)
        painter.setBrush(brush)
        draw_polygon(self.points)

        highlight = self.highlight
        if highlight:
            if highlight in self.selected or self.num_selected(type(highlight)) == 2:
                highlight = None

        if highlight and isinstance(highlight, geo.Segment):
            pen = QtGui.QPen(QtGui.QColor(0, 0, 0), 3, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin)
            painter.setPen(pen)
            draw_segment(highlight)

        idx = 0
        for selected in self.selected:
            if not isinstance(selected, geo.Segment):
                continue
            colors = [(0xFF, 0x80, 0x00), (0x80, 0x40, 0x00)]
            pen = QtGui.QPen(QtGui.QColor(*colors[idx]), 3, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin)
            painter.setPen(pen)
            draw_segment(selected)
            idx += 1

        painter.setPen(Qt.NoPen)
        if highlight and isinstance(highlight, geo.Point):
            brush = QtGui.QBrush(QtGui.QColor(0x00, 0x00, 0x00))
            painter.setBrush(brush)
            draw_point(highlight)

        idx = 0
        for selected in self.selected:
            if not isinstance(selected, geo.Point):
                continue
            colors = [(0x00, 0xFF, 0x80), (0x00, 0x80, 0x40)]
            brush = QtGui.QBrush(QtGui.QColor(*colors[idx]))
            painter.setBrush(brush)
            draw_point(selected)
            idx += 1

        pen = QtGui.QPen(QtGui.QColor(0x80, 0x80, 0x80), 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin)
        painter.setPen(pen)
        for line in self.lines:
            draw_line(line)

    def num_selected(self, type):
        count = 0
        for selected in self.selected:
            if isinstance(selected, type):
                count += 1
        return count

    def on_canvas_mouse_release_event(self, event):
        mouse_point = self.window_to_point(event.pos())

        if self.highlight:
            if self.highlight in self.selected:
                self.selected.remove(self.highlight)
            else:
                if self.num_selected(type(self.highlight)) < 2:
                    self.selected.append(self.highlight)
                    self.highlight = None
        else:
            self.selected.clear()

        self.ui.canvas.update()
        self.update_actions()

    def on_canvas_mouse_move_event(self, event):
        mouse_point = self.window_to_point(event.pos())
        highlight = self.find_point_near(mouse_point)
        if not highlight:
            highlight = self.find_segment_near(mouse_point)

        if highlight != self.highlight:
            self.highlight = highlight
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

    def update_actions(self):
        self.ui.actionPoints.setEnabled(self.num_selected(geo.Point) == 2 and self.num_selected(geo.Segment) == 0)
        self.ui.actionPointPoint.setEnabled(self.num_selected(geo.Point) == 2 and self.num_selected(geo.Segment) == 0)
        self.ui.actionLineLine.setEnabled(self.num_selected(geo.Point) == 0 and self.num_selected(geo.Segment) == 2)

    def on_action_zoom_in(self):
        self.zoom *= 1.25
        self.resize_canvas()

    def on_action_zoom_out(self):
        self.zoom /= 1.25
        self.resize_canvas()

    def on_action_points(self):
        p1 = self.selected[0]
        p2 = self.selected[1]
        segment = geo.Segment(p1, p2)
        self.lines.append(segment.line())
        self.selected.clear()
        self.update_actions()
        self.ui.canvas.update()

    def on_action_point_point(self):
        p1 = self.selected[0]
        p2 = self.selected[1]
        normal = p2 - p1
        offset = (normal * (p1 - geo.Point(0, 0)) + normal * (p2 - geo.Point(0, 0))) / 2
        self.lines.append(geo.Line(normal, offset))
        self.selected.clear()
        self.update_actions()
        self.ui.canvas.update()

    def on_action_line_line(self):
        line1 = self.selected[0].line()
        line2 = self.selected[1].line()

        theta1 = math.atan2(line1.normal.y, line1.normal.x)
        theta2 = math.atan2(line2.normal.y, line2.normal.x)
        if theta1 - theta2 > math.pi/2:
            theta2 += math.pi
        if theta2 - theta1 > math.pi/2:
            theta1 += math.pi
        theta = (theta1 + theta2) / 2

        normal = geo.Vector(math.cos(theta), math.sin(theta))
        t1 = line1.offset / (line1.normal * normal)
        t2 = line2.offset / (line2.normal * normal)
        t = (t1 + t2) / 2
        offset = t * normal.magnitude2()
        self.lines.append(geo.Line(normal, offset))
        self.selected.clear()
        self.update_actions()
        self.ui.canvas.update()
