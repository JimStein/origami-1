from PySide import QtCore, QtGui
from PySide.QtCore import Qt

from window_ui import Ui_MainWindow

import geo
import geoutil

SELECTION_THRESHOLD = 10
MARGIN = 10
ZOOM_INCREMENT = 1.25

EDGE_COLOR = QtGui.QColor(0, 0, 0)
PAPER_COLOR = QtGui.QColor(0xFF, 0xFF, 0x80)
LINE_COLOR = QtGui.QColor(0x80, 0x80, 0x80)
SELECTED_LINE_COLORS = [QtGui.QColor(0xFF, 0x80, 0x00), QtGui.QColor(0x80, 0x40, 0x00)]
SELECTED_POINT_COLORS = [QtGui.QColor(0x00, 0xFF, 0x80), QtGui.QColor(0x00, 0x80, 0x40)]
HIGHLIGHT_COLOR = QtGui.QColor(0, 0, 0)
LINE_WIDTH = 2
LINE_WIDTH_SELECTED = 3
POINT_SIZE = 3

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
        self.ui.actionLinePoint.triggered.connect(self.on_action_line_point)
        self.ui.actionPointPointLine.triggered.connect(self.on_action_point_point_line)
        self.ui.actionLinePointLine.triggered.connect(self.on_action_line_point_line)

        self.ui.canvas.setMouseTracking(True)

        self.zoom = 1

        points = [geo.Point(0, 0), geo.Point(0, 1), geo.Point(1, 1), geo.Point(1, 0)]
        self.polygon = geo.Polygon(points)
        self.segments = self.polygon.segments()
        self.intersections = points
        self.highlight = None
        self.selected = []
        self.lines = []
        self.update_actions()

    def canvas_size(self):
        return min(self.ui.scrollArea.width(), self.ui.scrollArea.height()) * self.zoom

    def point_to_window(self, point):
        size = self.canvas_size()
        return QtCore.QPoint(MARGIN + point.x * (size - 2 * MARGIN), MARGIN + point.y * (size - 2 * MARGIN))

    def window_to_point(self, point):
        size = self.canvas_size()
        return geo.Point((point.x() - MARGIN) / (size - 2 * MARGIN), (point.y() - MARGIN) / (size - 2 * MARGIN))

    def selection_threshold(self):
        return SELECTION_THRESHOLD / self.canvas_size()

    def find_intersection_near(self, mouse_point):
        found_point = None
        threshold = self.selection_threshold()
        for point in self.intersections:
            distance2 = (mouse_point - point).magnitude2()
            if distance2 <= threshold * threshold:
                found_point = point
                break
        return found_point

    def find_line_near(self, mouse_point):
        found_line = None
        threshold = self.selection_threshold()
        for segment in self.segments:
            line = geoutil.line_from_segment(segment)
            if geoutil.distance_to_line(mouse_point, line) <= threshold and geoutil.is_point_within_segment(mouse_point, segment):
                found_line = line
                break

        if not found_line:
            for line in self.lines:
                if geoutil.distance_to_line(mouse_point, line) <= threshold:
                    found_line = line
                    break

        return found_line

    def on_canvas_paint_event(self, event):
        painter = QtGui.QPainter(self.ui.canvas)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        def draw_segment(segment):
            draw_points = [self.point_to_window(point) for point in segment.points()]
            painter.drawLine(*draw_points)

        def draw_point(point):
            painter.drawEllipse(self.point_to_window(point), POINT_SIZE, POINT_SIZE)

        def draw_line(line):
            min = self.window_to_point(QtCore.QPoint(0, 0))
            max = self.window_to_point(QtCore.QPoint(self.ui.canvas.width(), self.ui.canvas.height()))
            if abs(line.normal.x) > abs(line.normal.y):
                minline = geoutil.line_from_point_normal(min, geo.Vector(0, 1))
                maxline = geoutil.line_from_point_normal(max, geo.Vector(0, -1))
            else:
                minline = geoutil.line_from_point_normal(min, geo.Vector(1, 0))
                maxline = geoutil.line_from_point_normal(max, geo.Vector(-1, 0))

            minpoint = geoutil.intersect_lines(line, minline)
            maxpoint = geoutil.intersect_lines(line, maxline)
            points = [minpoint, maxpoint]
            draw_points = [self.point_to_window(point) for point in points]
            painter.drawLine(*draw_points)

        def draw_polygon(polygon):
            draw_points = [self.point_to_window(point) for point in polygon.points]
            painter.drawPolygon(draw_points)

        pen = QtGui.QPen(EDGE_COLOR, LINE_WIDTH, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin)
        brush = QtGui.QBrush(PAPER_COLOR)
        painter.setPen(pen)
        painter.setBrush(brush)
        draw_polygon(self.polygon)

        highlight = self.highlight
        if highlight:
            if highlight in self.selected or self.num_selected(type(highlight)) == 2:
                highlight = None

        pen = QtGui.QPen(LINE_COLOR, LINE_WIDTH, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin)
        painter.setPen(pen)
        for line in self.lines:
            draw_line(line)

        idx = 0
        for selected in self.selected:
            if not isinstance(selected, geo.Line):
                continue
            pen = QtGui.QPen(SELECTED_LINE_COLORS[idx], LINE_WIDTH_SELECTED, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin)
            painter.setPen(pen)
            draw_line(selected)
            idx += 1

        idx = 0
        painter.setPen(Qt.NoPen)
        for selected in self.selected:
            if not isinstance(selected, geo.Point):
                continue
            brush = QtGui.QBrush(SELECTED_POINT_COLORS[idx])
            painter.setBrush(brush)
            draw_point(selected)
            idx += 1

        if highlight:
            if isinstance(highlight, geo.Line):
                pen = QtGui.QPen(HIGHLIGHT_COLOR, LINE_WIDTH_SELECTED, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin)
                painter.setPen(pen)
                draw_line(highlight)

            elif isinstance(highlight, geo.Point):
                brush = QtGui.QBrush(HIGHLIGHT_COLOR)
                painter.setBrush(brush)
                painter.setPen(Qt.NoPen)
                draw_point(highlight)

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
        highlight = self.find_intersection_near(mouse_point)
        if not highlight:
            highlight = self.find_line_near(mouse_point)

        if highlight != self.highlight:
            self.highlight = highlight
            self.ui.canvas.update()

    def on_scroll_area_resize_event(self, event):
        self.resize_canvas()

    def resize_canvas(self):
        size = self.canvas_size()

        hmax = self.ui.scrollArea.horizontalScrollBar().maximum()
        hvalue = self.ui.scrollArea.horizontalScrollBar().value()
        vmax = self.ui.scrollArea.verticalScrollBar().maximum()
        vvalue = self.ui.scrollArea.verticalScrollBar().value()
        x = hvalue / hmax if hmax else 0.5
        y = vvalue / vmax if vmax else 0.5

        self.ui.canvas.setMinimumSize(QtCore.QSize(size, size))
        self.ui.canvas.setMaximumSize(QtCore.QSize(size, size))

        hmax = self.ui.scrollArea.horizontalScrollBar().maximum()
        vmax = self.ui.scrollArea.verticalScrollBar().maximum()

        self.ui.scrollArea.horizontalScrollBar().setValue(x * hmax)
        self.ui.scrollArea.verticalScrollBar().setValue(y * vmax)

    def update_actions(self):
        self.ui.actionPoints.setEnabled(self.num_selected(geo.Point) == 2 and self.num_selected(geo.Line) == 0)
        self.ui.actionPointPoint.setEnabled(self.num_selected(geo.Point) == 2 and self.num_selected(geo.Line) == 0)
        self.ui.actionLineLine.setEnabled(self.num_selected(geo.Point) == 0 and self.num_selected(geo.Line) == 2)
        self.ui.actionLinePoint.setEnabled(self.num_selected(geo.Point) == 1 and self.num_selected(geo.Line) == 1)
        self.ui.actionPointPointLine.setEnabled(self.num_selected(geo.Point) == 2 and self.num_selected(geo.Line) == 1)
        self.ui.actionLinePointLine.setEnabled(self.num_selected(geo.Point) == 1 and self.num_selected(geo.Line) == 2)

    def add_lines(self, lines):
        for line in lines:
            for segment in self.segments:
                point = geoutil.intersect_line_segment(line, segment)
                if point:
                    self.intersections.append(point)

            for other_line in self.lines:
                point = geoutil.intersect_lines(line, other_line)
                if point:
                    self.intersections.append(point)

        self.lines.extend(lines)
        self.update_actions()
        self.ui.canvas.update()

    def add_line(self, line):
        self.add_lines([line])

    def on_action_zoom_in(self):
        self.zoom *= ZOOM_INCREMENT
        self.resize_canvas()

    def on_action_zoom_out(self):
        self.zoom /= ZOOM_INCREMENT
        self.resize_canvas()

    def on_action_points(self):
        line = geoutil.huzita_justin_1(self.selected[0], self.selected[1])
        self.selected.clear()
        self.add_line(line)

    def on_action_point_point(self):
        line = geoutil.huzita_justin_2(self.selected[0], self.selected[1])
        self.selected.clear()
        self.add_line(line)

    def on_action_line_line(self):
        lines = geoutil.huzita_justin_3(self.selected[0], self.selected[1])
        if lines:
            self.selected.clear()
            self.add_lines(lines)

    def on_action_line_point(self):
        for selected in self.selected:
            if isinstance(selected, geo.Point):
                point = selected
            elif isinstance(selected, geo.Line):
                line = selected

        line = geoutil.huzita_justin_4(point, line)
        self.selected.clear()
        self.add_line(line)

    def on_action_point_point_line(self):
        points = []
        for selected in self.selected:
            if isinstance(selected, geo.Point):
                points.append(selected)
            elif isinstance(selected, geo.Line):
                line = selected

        lines = geoutil.huzita_justin_5(points[0], points[1], line)
        if lines:
            self.selected.clear()
            self.add_lines(lines)

    def on_action_line_point_line(self):
        lines = []
        for selected in self.selected:
            if isinstance(selected, geo.Point):
                point = selected
            elif isinstance(selected, geo.Line):
                lines.append(selected)

        line = geoutil.huzita_justin_7(point, lines[0], lines[1])
        if line:
            self.selected.clear()
            self.add_line(line)
