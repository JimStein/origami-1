import geo

def distance_from_point(point0, point1):
    return (point1 - point0).magnitude()

def distance_from_point2(point0, point1):
    return (point1 - point0).magnitude2()