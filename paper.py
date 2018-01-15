import geo
import geoutil

class Facet(object):
    def __init__(self, polygon):
        self.polygon = polygon

    def __repr__(self):
        return 'paper.Facet(%s)' % self.polygon

class Layer(object):
    def __init__(self, facets):
        self.facets = facets

    def __repr__(self):
        return 'paper.Layer(%s)' % self.facets

class Sheet(object):
    def __init__(self, polygon):
        facet = Facet(polygon)
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

    def fold(self, line):
        old_layers = []
        new_layers = []
        for layer in reversed(self.layers):
            old_facets = []
            new_facets = []
            new_layer = []
            for facet in layer.facets:
                (polygon0, polygon1, segment) = geoutil.polygon.split(facet.polygon, line)
                old_facets.append(facet)
                if polygon1:
                    new_facets.append(Facet(polygon1))
                if polygon0:
                    new_layer.append(Facet(geoutil.polygon.reflect(polygon0, line)))
            for facet in old_facets:
                layer.facets.remove(facet)
            layer.facets.extend(new_facets)
            if not layer.facets:
                old_layers.append(layer)
            if new_layer:
                new_layers.append(Layer(new_layer))
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
