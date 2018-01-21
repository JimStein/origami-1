import geo
import geoutil

MIN_DISTANCE = .001

def point_parity(point, line):
    distance = point.vector() * line.normal - line.offset
    if abs(distance) < MIN_DISTANCE:
        return 0
    return int(distance / abs(distance))

def split(polygon, line):
    points = ([], [])
    segment_points = []
    segment_idxs = [-1, -1]
    last_point = polygon.points[-1]
    last_parity = point_parity(last_point, line)

    for point in polygon.points:
        parity = point_parity(point, line)
        if parity == 0:
            idx = 0 if last_parity == -1 else 1
            segment_idxs[idx] = len(points[idx])

            points[0].append(point)
            points[1].append(point)
            segment_points.append(point)
        else:
            idx = 0 if parity == -1 else 1
            points[idx].append(point)
        last_parity = parity

    polygon0 = None
    polygon1 = None
    segment = None
    if len(segment_points) == 2:
        segment = geo.Segment(segment_points[0], segment_points[1])
    if len(points[0]) > 2:
        polygon0 = geo.Polygon(points[0])
    if len(points[1]) > 2:
        polygon1 = geo.Polygon(points[1])

    return (polygon0, polygon1, segment, segment_idxs)

def intersect_line(polygon, line):
    points = []
    idx = 0
    last_point = polygon.points[-1]
    last_parity = point_parity(last_point, line)

    for point in polygon.points:
        parity = point_parity(point, line)
        if parity != 0 and last_parity != 0 and parity != last_parity:
            polygon_line = geoutil.line.from_points(last_point, point)
            intersection = geoutil.line.intersect(line, polygon_line)
            points.append((intersection, idx))
        idx += 1
        last_point = point
        last_parity = parity
    return points

def intersects_line(polygon, line):
    last_point = polygon.points[-1]
    first_parity = point_parity(last_point, line)
    for point in polygon.points:
        parity = point_parity(point, line)
        if first_parity == 0:
            first_parity = parity
        if parity != 0 and parity != first_parity:
            return True
        last_point = point
    return False

def reflect(polygon, line):
    points = [geoutil.point.reflect(point, line) for point in polygon.points]
    return geo.Polygon(points)
