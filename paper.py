import geo
import geoutil

class Facet(object):
    def __init__(self, polygon, parity):
        self.polygon = polygon
        self.parity = parity
        self.neighbors = [None] * len(polygon.points)

    def __repr__(self):
        return 'paper.Facet(%s)' % self.polygon

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

    def split_facet_edge(self, facet, point, idx):
        points = facet.polygon.points
        neighbors = facet.neighbors
        points.insert(idx, point)
        facet.neighbors.insert(idx, None)
        facet.polygon = geo.Polygon(points)
        for neighbor in neighbors[idx + 1:]:
            if neighbor:
                (neighbor_facet, neighbor_idx) = neighbor
                (neighbor_facet2, neighbor_idx2) = neighbor_facet.neighbors[neighbor_idx]
                neighbor_facet.neighbors[neighbor_idx] = (neighbor_facet2, neighbor_idx2 + 1)

    def split_facet_edges(self, facet, line):
        polygon_points = facet.polygon.points
        neighbors = facet.neighbors
        points = geoutil.polygon.intersect_line(facet.polygon, line)
        offset = 0
        for (point, idx) in points:
            neighbor = facet.neighbors[idx + offset]
            self.split_facet_edge(facet, point, idx + offset)
            if neighbor:
                (neighbor_facet, neighbor_idx) = neighbor
                self.split_facet_edge(neighbor_facet, point, neighbor_idx)
                if facet.polygon.points[idx + offset] == neighbor_facet.polygon.points[neighbor_idx]:
                    facet.neighbors[idx + offset] = (neighbor_facet, neighbor_idx)
                    facet.neighbors[idx + offset + 1] = (neighbor_facet, neighbor_idx + 1)
                    neighbor_facet.neighbors[neighbor_idx] = (facet, idx + offset)
                    neighbor_facet.neighbors[neighbor_idx + 1] = (facet, idx + offset + 1)
                else:
                    facet.neighbors[idx + offset] = (neighbor_facet, neighbor_idx + 1)
                    facet.neighbors[idx + offset + 1] = (neighbor_facet, neighbor_idx)
                    neighbor_facet.neighbors[neighbor_idx] = (facet, idx + offset + 1)
                    neighbor_facet.neighbors[neighbor_idx + 1] = (facet, idx + offset)
            offset += 1
        facet.polygon = geo.Polygon(polygon_points)
        facet.neighbors = neighbors

    def split_facet(self, facet, line):
        (polygon0, polygon1, segment, idxs, mappings) = geoutil.polygon.split(facet.polygon, line)
        facet0 = None
        facet1 = None
        if polygon0:
            facet0 = Facet(polygon0, facet.parity)
            facet0.neighbors = [facet.neighbors[idx] for idx in mappings[0]]
        if polygon1:
            facet1 = Facet(polygon1, facet.parity)
            facet1.neighbors = [facet.neighbors[idx] for idx in mappings[1]]
        if facet0 and facet1:
            facet0.neighbors[idxs[0]] = (facet1, idxs[1])
            facet1.neighbors[idxs[1]] = (facet0, idxs[0])

        return (facet0, facet1, segment)

    def fold(self, line):
        old_layers = []
        new_layers = []
        for layer in reversed(self.layers):
            old_facets = []
            new_facets = []
            new_layer = []
            for facet in layer.facets:
                self.split_facet_edges(facet, line)
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
