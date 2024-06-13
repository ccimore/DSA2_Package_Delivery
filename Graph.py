
# Blueprint for Graph objects.  Creates Graph.
# O(1)time --- O(N)space
class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}

    # Adds vertex to graph
    # O(1)time --- O(N)space
    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    # Adds directed edge weight value for vertexes key to graph
    # O(1)time --- O(N)space
    def add_directed_edge(self, from_vertex, to_vertex, weight=1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight

    # Calls directed edge weight method for vertexes in both directions
    # O(1)time --- O(N)space
    def add_undirected_edge(self, vertex_a, vertex_b, weight=1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    # Retrieves edge weight value from vertexes key
    # O(1)time --- O(1)space
    def get_weight(self, vertex1, vertex2):
        weight = float(self.edge_weights[(vertex1, vertex2)])
        return weight
