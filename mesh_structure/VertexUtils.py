from mesh_structure.EdgeUtils import EdgeBunch
from mesh_structure.Direction import Direction
import bintrees as bt


class SortedVertexLists:

    def __init__(self):
        self.x_sorted = bt.FastRBTree()
        self.y_sorted = bt.FastRBTree()

    def __str__(self):
        s = ""
        for key in self.x_sorted:
            vertex = self.x_sorted[key]
            s = s + str(vertex) + "\n"
        return s
        
    def get_vertices_beetween_from_x_sorted(self, v1, v2):
        return self.x_sorted[(v1.x, v1.y):(v2.x, v2.y)]        

    def get_vertices_beetween_from_y_sorted(self, v1, v2):
        return self.y_sorted[(v1.y, v1.x):(v2.y, v2.x)] 
        
    def get_vertex(self, x, y):
        key = (x, y)
        return self.x_sorted[key]

    def get_max_x(self):
        return max(self.x_sorted)[0]

    def get_max_y(self):
        return max(self.y_sorted)[0]


class Vertex:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.top_edges = EdgeBunch(Direction.top)
        self.right_edges = EdgeBunch(Direction.right)
        self.bottom_edges = EdgeBunch(Direction.bottom)
        self.left_edges = EdgeBunch(Direction.left)

    def get_existing_edge_directions(self):
        existing_directions = []
        if not (self.top_edges is None or self.top_edges.is_empty()):
            existing_directions.append(Direction.top)
        if not (self.right_edges is None or self.right_edges.is_empty()):
            existing_directions.append(Direction.right)
        if not (self.bottom_edges is None or self.bottom_edges.is_empty()):
            existing_directions.append(Direction.bottom)
        if not (self.left_edges is None or self.left_edges.is_empty()):
            existing_directions.append(Direction.left)
        return existing_directions

    def get_shortest_edge_in_direction(self, direction):
        if direction == Direction.top:
            return self.top_edges.get_shortest_edge()
        elif direction == Direction.right:
            return self.right_edges.get_shortest_edge()
        elif direction == Direction.bottom:
            return self.bottom_edges.get_shortest_edge()
        elif direction == Direction.left:
            return self.left_edges.get_shortest_edge()

    def get_longest_edge_in_direction(self, direction):
        if direction == Direction.top:
            return self.top_edges.get_longest_edge()
        elif direction == Direction.right:
            return self.right_edges.get_longest_edge()
        elif direction == Direction.bottom:
            return self.bottom_edges.get_longest_edge()
        elif direction == Direction.left:
            return self.left_edges.get_longest_edge()

    def add_incident_edge(self, e):
        if e.v1 == self:
            v = e.v2
        else:
            v = e.v1

        if self.x == v.x:
            if self.y < v.y:
                self.__add_top_edge(e)
            else:
                self.__add_bottom_edge(e)
        else:
            if self.x < v.x:
                self.__add_right_edge(e)
            else:
                self.__add_left_edge(e)

    def __add_top_edge(self, e):
        self.top_edges.add_incident_edge(e)

    def __add_right_edge(self, e):
        self.right_edges.add_incident_edge(e)

    def __add_bottom_edge(self, e):
        self.bottom_edges.add_incident_edge(e)

    def __add_left_edge(self, e):
        self.left_edges.add_incident_edge(e)

    def __str__(self):
        s = ("[" + str(self.x) + ", " + str(self.y) + "]")
        return s

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if self.x < other.x:
            return True
        elif self.x > other.x:
            return False
        elif self.y < other.y:
            return True
        elif self.y > other.y:
            return False
        return False
