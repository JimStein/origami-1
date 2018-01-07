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

    def split(self, line):
        for layer in self.layers:
            old_facets = []
            new_facets = []
            for facet in layer.facets:
                if geoutil.polygon.intersects_line(facet.polygon, line):
                    (polygon0, polygon1) = geoutil.polygon.split(facet.polygon, line)
                    old_facets.append(facet)
                    new_facets.extend([Facet(polygon0), Facet(polygon1)])
                    self.segments.extend(polygon0.segments())
                    self.points.extend(polygon0.points)
            for facet in old_facets:
                layer.facets.remove(facet)
            layer.facets.extend(new_facets)