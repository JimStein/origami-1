import geo

def distance_from_point(point0, point1):
    return (point1 - point0).magnitude()

def distance_from_point2(point0, point1):
    return (point1 - point0).magnitude2()

def reflect(point, line):
    offset = line.normal * (line.normal * point.vector() - line.offset)
    return point - offset * 2