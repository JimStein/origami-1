import math

import geo
import geoutil

MAX_DISTANCE = 1000

def O1(point0, point1):
    return geoutil.line.from_points(point0, point1)

def O2(point0, point1):
    normal = (point1 - point0).normalize()
    line0 = geoutil.line.from_point_normal(point0, normal)
    line1 = geoutil.line.from_point_normal(point1, normal)
    offset = (line0.offset + line1.offset) / 2
    return geo.Line(normal, offset)

def O3(line0, line1):
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

def O4(point, line):
    return geoutil.line.perpendicular(line, point)

def O5(point0, point1, line):
    radius = point1 - point0
    perp = geoutil.line.perpendicular(line, point0)
    start = geoutil.line.intersect(perp, line)
    offset = start - point0
    disc = radius.magnitude2() - offset.magnitude2()

    lines = []
    if disc == 0:
        lines.append(O2(start, point1))
    elif disc > 0:
        d = math.sqrt(disc)
        direction = geoutil.vector.perpendicular(line.normal)

        p = start + direction * d
        lines.append(O2(p, point1))

        p = start - direction * d
        lines.append(O2(p, point1))

    return lines

def O7(point, line0, line1):
    parallel = geoutil.line.parallel(line0, point)
    intersection = geoutil.line.intersect(parallel, line1)
    if intersection:
        return O2(point, intersection)
    else:
        return None
