
# Source: WGU C950 - Webinar 3 - How to Dijkstra - Complete Python Code pdf
# Blueprint for Vertex objects
# O(1) time --- O(1)space
class Vertex:
    def __init__(self, label):
        self.label = label
        self.distance = float('inf')
        self.previous_vertex = None
