import bintrees as bt


class Edge:
    def __init__(self, v1, v2):
        if v1 < v2:
            self.v1 = v1
            self.v2 = v2
        else:
            self.v1 = v2
            self.v2 = v1
        self.length = self.__set_length()

    def get_second_vertex_from_edge(self, first_vertex):
        if self.v1 == first_vertex:
            return self.v2
        else:
            return self.v1

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

    def __getitem__(self, e):
        key = (e.v1.x, e.v1.y, e.v2.x, e.v2.y)
        return self.edges[key]
        
    def __contains__(self, e):
        key = (e.v1.x, e.v1.y, e.v2.x, e.v2.y)
        return key in self.edges

class EdgeBunch:

    def __init__(self, direction):
        self.edge_incident = bt.FastRBTree()
        self.direction = direction

    def add_incident_edge(self, e):
        key = (self.direction, e.length)
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
