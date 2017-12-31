import geo

import math

MAX_DISTANCE = 1000
ORIGIN = geo.Point(0, 0)

def is_point_within_segment(point, segment):
    length2 = segment.length2()
    length2a = (point - segment.start).magnitude2()
    length2b = (point - segment.end).magnitude2()
    return (length2a < length2 and length2b < length2)

def intersect_lines(a, b):
    det = a.normal.x * b.normal.y - a.normal.y * b.normal.x
    xdet = a.offset * b.normal.y - a.normal.y * b.offset
    ydet = a.normal.x * b.offset - a.offset * b.normal.x

    if abs(xdet) < abs(MAX_DISTANCE * det) and abs(ydet) < abs(MAX_DISTANCE * det):
        x = xdet / det
        y = ydet / det
        return geo.Point(x, y)
    else:
        return None

def intersect_line_segment(line, segment):
    point = intersect_lines(line, segment.line())
    if point and is_point_within_segment(point, segment):
        return point
    else:
        return None

def vector(point):
    return point - ORIGIN

def perpendicular_vector(vector):
    return geo.Vector(vector.y, -vector.x)

def distance_to_line(point, line):
    offset = vector(point) * line.normal
    return abs(offset - line.offset)

def parallel_line(line, point):
    normal = line.normal
    offset = normal * vector(point)
    return geo.Line(normal, offset)

def perpendicular_line(line, point):
    normal = perpendicular_vector(line.normal)
    offset = normal * vector(point)
    return geo.Line(normal, offset)

def line_from_points(point0, point1):
    return geo.Segment(point0, point1).line()

def line_from_point_normal(point, normal):
    offset = normal * vector(point)
    return geo.Line(normal, offset)

def huzita_justin_1(point0, point1):
    return line_from_points(point0, point1)

def huzita_justin_2(point0, point1):
    normal = point1 - point0
    offset = (normal * vector(point0) + normal * vector(point1)) / 2
    return geo.Line(normal, offset)

def huzita_justin_3(line0, line1):
    theta0 = math.atan2(line0.normal.y, line0.normal.x)
    theta1 = math.atan2(line1.normal.y, line1.normal.x)
    theta = (theta0 + theta1) / 2

    cos = math.cos(theta)
    sin = math.sin(theta)
    lines = []
    for normal in (geo.Vector(cos, sin), geo.Vector(-sin, cos)):
        if abs(line0.offset) > abs(MAX_DISTANCE * (line0.normal * normal)):
            continue
        if abs(line1.offset) > abs(MAX_DISTANCE * (line1.normal * normal)):
            continue

        t0 = line0.offset / (line0.normal * normal)
        t1 = line1.offset / (line1.normal * normal)
        offset = (t0 + t1) / 2
        lines.append(geo.Line(normal, offset))

    return lines

def huzita_justin_4(point, line):
    return perpendicular_line(line, point)

def huzita_justin_5(point0, point1, line):
    radius = point1 - point0
    perp = perpendicular_line(line, point0)
    start = intersect_lines(perp, line)
    offset = start - point0
    disc = radius.magnitude2() - offset.magnitude2()

    lines = []
    if disc == 0:
        lines.append(huzita_justin_2(start, point1))
    elif disc > 0:
        d = math.sqrt(disc)
        direction = perpendicular_vector(line.normal)

        p = start + direction * d
        lines.append(huzita_justin_2(p, point1))

        p = start - direction * d
        lines.append(huzita_justin_2(p, point1))

    return lines

def huzita_justin_7(point, line0, line1):
    parallel = parallel_line(line0, point)
    intersection = intersect_lines(parallel, line1)
    if intersection:
        return huzita_justin_2(point, intersection)
    else:
        return None
