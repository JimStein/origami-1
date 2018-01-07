import math

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'geo.Point(%s, %s)' % (self.x, self.y)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, vector):
        return Point(self.x + vector.x, self.y + vector.y)

    def __sub__(self, other):
        if isinstance(other, Point):
            return Vector(self.x - other.x, self.y - other.y)
        else:
            return Point(self.x - other.x, self.y - other.y)

    def vector(self):
        return self - Point(0, 0)

class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'geo.Vector(%s, %s)' % (self.x, self.y)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        else:
            return Vector(self.x * other, self.y * other)

    def __div__(self, other):
        return Vector(self.x / other, self.y / other)

    def __truediv__(self, other):
        return self.__div__(other)

    def __neg__(self):
        return self * -1

    def magnitude2(self):
        return self * self

    def magnitude(self):
        return math.sqrt(self.magnitude2())

    def normalize(self):
        return self / self.magnitude()

class Line(object):
    def __init__(self, normal, offset):
        self.normal = normal
        self.offset = offset

    def __repr__(self):
        return 'geo.Line(%s, %s)' % (self.normal, self.offset)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.normal == other.normal and self.offset == other.offset

    def __hash__(self):
        return hash((self.normal, self.offset))

class Segment(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return 'geo.Segment(%s, %s)' % (self.start, self.end)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash((self.start, self.end))

    def points(self):
        return [self.start, self.end]

    def length(self):
        return (self.end - self.start).magnitude()

    def length2(self):
        return (self.end - self.start).magnitude2()

class Polygon(object):
    def __init__(self, points):
        self.points = points

    def __repr__(self):
        return 'geo.Polygon(%s)' % self.points

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.points == other.points

    def __hash__(self):
        return hash(self.points)

    def segments(self):
        last_point = self.points[-1]
        segments = []
        for point in self.points:
            segments.append(Segment(last_point, point))
            last_point = point
        return segments