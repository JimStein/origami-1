import geo
import geoutil

MAX_DISTANCE = 1000

def intersect(line0, line1):
    det = line0.normal.x * line1.normal.y - line0.normal.y * line1.normal.x
    xdet = line0.offset * line1.normal.y - line0.normal.y * line1.offset
    ydet = line0.normal.x * line1.offset - line0.offset * line1.normal.x

    if abs(xdet) < abs(MAX_DISTANCE * det) and abs(ydet) < abs(MAX_DISTANCE * det):
        x = xdet / det
        y = ydet / det
        return geo.Point(x, y)
    else:
        return None

def distance_to_point(line, point):
    offset = point.vector() * line.normal
    return abs(offset - line.offset)

def parallel(line, point):
    normal = line.normal
    offset = normal * point.vector()
    return geo.Line(normal, offset)

def perpendicular(line, point):
    normal = geoutil.vector.perpendicular(line.normal)
    offset = normal * point.vector()
    return geo.Line(normal, offset)

def from_point_normal(point, normal):
    offset = normal * point.vector()
    return geo.Line(normal, offset)

def from_points(point0, point1):
    normal = geoutil.vector.perpendicular(point1 - point0).normalize()
    return from_point_normal(point0, normal)

def from_segment(segment):
    return from_points(segment.start, segment.end)
