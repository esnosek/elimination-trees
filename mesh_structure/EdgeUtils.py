import bintrees as bt


class Edge:
    def __init__(self, v1, v2):
        # trzeba zadbac zeby v1 < v2
        self.v1 = v1
        self.v2 = v2
        self.length = self.__set_length()

    def __set_length(self):
        if (self.v1.x == self.v2.x):
            return abs(self.v1.y - self.v2.y)
        else:
            return abs(self.v1.x - self.v2.x)

    def __str__(self):
        return ("[" + str(self.v1.x) + ", " + str(self.v1.y) + "], [" +
                str(self.v2.x) + ", " + str(self.v2.y) + "]")

    def __eq__(self, other):
        return ((self.v1 == other.v1 and self.v2 == other.v2) and
                (self.v1 == other.v2 and self.v1 == other.v2))

    def __ne__(self, other):
        return not self.__eq__(other)


class SortedEdgeList:

    def __init__(self):
        self.edges = bt.FastRBTree()

    def add_edge(self, e):
        key = (e.v1.x, e.v1.y, e.v2.x, e.v2.y)
        self.edges.insert(key, e)
        if key in self.edges:
            return self.edges[key]
        else:
            self.edges.insert(key, e)
        return e

    def get_edge(self, key):
        return self.edges[key]


sorted_edge_list = SortedEdgeList()


def create_edge(v1, v2):
    global sorted_edge_list
    e = Edge(v1, v2)
    key = (v1.x, v1.y, v2.x, v2.y)
    if key in sorted_edge_list.edges:
        return sorted_edge_list.edges[key]
    else:
        v1.add_incident_edge(e)
        v2.add_incident_edge(e)
        sorted_edge_list.edges.insert(key, e)
    return e


class EdgeBunch:

    def __init__(self, direction):
        self.edge_incident = bt.FastRBTree()
        self.direction = direction

    def add_incident_edge(self, key, e):
        self.edge_incident.insert(key, e)

    def get_longest_edge(self):
        if self.edge_incident.is_empty():
            raise ValueError
        else:
            return self.edge_incident[max(self.edge_incident)]

    def get_shortest_edge(self):
        if self.edge_incident.is_empty():
            raise ValueError
        else:
            return self.edge_incident[min(self.edge_incident)]

    def is_empty(self):
        if len(self.edge_incident) == 0:
            return True
        else:
            return False

    def change_vertex(self, vertex):
        for key in self.edge_incident:
            edge = self.edge_incident[key]
            if edge.v1 == vertex:
                edge.v1 = vertex
            elif edge.v2 == vertex:
                edge.v2 = vertex
