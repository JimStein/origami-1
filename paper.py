import geo

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
