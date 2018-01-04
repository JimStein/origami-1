import geoutil

def is_point_within(segment, point):
    length2 = segment.length2()
    length2a = (point - segment.start).magnitude2()
    length2b = (point - segment.end).magnitude2()
    return (length2a < length2 and length2b < length2)

def intersect_line(segment, line):
    point = geoutil.line.intersect(line, geoutil.line.from_segment(segment))
    if point and is_point_within(segment, point):
        return point
    else:
        return None



