import geo
import geoutil

class Facet(object):
    def __init__(self, polygon, parity):
        self.polygon = polygon
        self.parity = parity

    def __repr__(self):
        return 'paper.Facet(%s)' % self.polygon

    def split(self, line):
        (polygon0, polygon1, segment) = geoutil.polygon.split(self.polygon, line)
        facet0 = None
        facet1 = None
        if polygon0:
            facet0 = Facet(polygon0, self.parity)
        if polygon1:
            facet1 = Facet(polygon1, self.parity)
        return (facet0, facet1, segment)

    def reflect(self, line):
        return Facet(geoutil.polygon.reflect(self.polygon, line), 1 - self.parity)

class Layer(object):
    def __init__(self, facets):
        self.facets = facets

    def __repr__(self):
        return 'paper.Layer(%s)' % self.facets

class Sheet(object):
    def __init__(self, polygon):
        facet = Facet(polygon, 1)
        layer = Layer([facet])

        self.layers = [layer]
        self.segments = polygon.segments()
        self.points = polygon.points

    def __str__(self):
        ret = 'paper.Sheet\n'
        idx = 0
        for layer in self.layers:
            ret += ' Layer %s:\n' % idx
            idx += 1
            for facet in layer.facets:
                ret += '  %s\n' % facet.polygon
        return ret

    def split_facet(self, facet, line):
        polygon_points = facet.polygon.points
        points = geoutil.polygon.intersect_line(facet.polygon, line)
        offset = 0
        for (point, idx) in points:
            polygon_points.insert(idx + offset, point)
            offset += 1
        facet = Facet(geo.Polygon(polygon_points), facet.parity)
        return facet.split(line)

    def fold(self, line):
        old_layers = []
        new_layers = []
        for layer in reversed(self.layers):
            old_facets = []
            new_facets = []
            new_layer = []
            for facet in layer.facets:
                (facet0, facet1, segment) = self.split_facet(facet, line)
                old_facets.append(facet)
                if facet1:
                    new_facets.append(facet1)
                if facet0:
                    new_layer.append(facet0)
            for facet in old_facets:
                layer.facets.remove(facet)
            layer.facets.extend(new_facets)
            if not layer.facets:
                old_layers.append(layer)
            if new_layer:
                reflected = []
                for facet in new_layer:
                    facet = facet.reflect(line)
                    reflected.append(facet)
                new_layers.append(Layer(reflected))
        for layer in old_layers:
            self.layers.remove(layer)
        self.layers.extend(new_layers)
        segments = set()
        points = set()
        for layer in self.layers:
            for facet in layer.facets:
                for segment in facet.polygon.segments():
                    segments.add(segment)
                    points.add(segment.start)
                    points.add(segment.end)
        self.segments = list(segments)
        self.points = list(points)
