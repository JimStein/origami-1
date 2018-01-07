import geo
import geoutil

class Facet(object):
    def __init__(self, polygon):
        self.polygon = polygon

class Layer(object):
    def __init__(self, facets):
        self.facets = facets

class Sheet(object):
    def __init__(self, polygon):
        facet = Facet(polygon)
        layer = Layer([facet])

        self.layers = [layer]
        self.segments = polygon.segments()
        self.points = polygon.points

    def fold(self, line):
        new_layers = []
        for layer in reversed(self.layers):
            old_facets = []
            new_facets = []
            new_layer = []
            for facet in layer.facets:
                if geoutil.polygon.intersects_line(facet.polygon, line):
                    (polygon0, polygon1, segment) = geoutil.polygon.split(facet.polygon, line)
                    old_facets.append(facet)
                    new_facets.append(Facet(polygon0))
                    new_layer.append(Facet(geoutil.polygon.reflect(polygon1, line)))
            for facet in old_facets:
                layer.facets.remove(facet)
            layer.facets.extend(new_facets)
            new_layers.append(Layer(new_layer))
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
