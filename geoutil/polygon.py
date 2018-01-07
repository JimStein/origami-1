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
    last_point = polygon.points[-1]
    last_parity = point_parity(last_point, line)

    for point in polygon.points:
        parity = point_parity(point, line)
        if parity == 0:
            points[0].append(point)
            points[1].append(point)
            segment_points.append(point)
        else:
            if last_parity != 0 and parity != last_parity:
                polygon_line = geoutil.line.from_points(last_point, point)
                intersection = geoutil.line.intersect(line, polygon_line)
                points[0].append(intersection)
                points[1].append(intersection)
                segment_points.append(intersection)
            idx = 0 if parity == -1 else 1
            points[idx].append(point)
        last_point = point
        last_parity = parity

    return (geo.Polygon(points[0]), geo.Polygon(points[1]), geo.Segment(*segment_points))

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