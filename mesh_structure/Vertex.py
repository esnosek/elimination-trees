# -*- coding: utf-8 -*-

import bintrees as bt
import functools as f
from mesh_structure.EdgeBunch import EdgeBunch
from mesh_structure.Direction import Direction


@f.total_ordering
class Vertex:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.top_edges = EdgeBunch(Direction.top)
        self.right_edges = EdgeBunch(Direction.right)
        self.bottom_edges = EdgeBunch(Direction.bottom)
        self.left_edges = EdgeBunch(Direction.left)
        self.face_incident_tree = bt.FastRBTree()

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
        else: 
            direction == Direction.left
            return self.left_edges.get_shortest_edge()

    def get_longest_edge_in_direction(self, direction):
        if direction == Direction.top:
            return self.top_edges.get_longest_edge()
        elif direction == Direction.right:
            return self.right_edges.get_longest_edge()
        elif direction == Direction.bottom:
            return self.bottom_edges.get_longest_edge()
        else: 
            direction == Direction.left
            return self.left_edges.get_longest_edge()
            
    def add_incident_edge(self, edge):
        if edge.v1 == self:
            v = edge.v2
        else:
            v = edge.v1

        if self.x == v.x:
            if self.y < v.y:
                self.add_top_edge(edge)
            else:
                self.add_bottom_edge(edge)
        else:
            if self.x < v.x:
                self.add_right_edge(edge)
            else:
                self.add_left_edge(edge)

    def add_top_edge(self, edge):
        key = (Direction.top, edge.length)
        self.top_edges.add_incident_edge(key, edge)

    def add_right_edge(self, edge):
        key = (Direction.right, edge.length)
        self.right_edges.add_incident_edge(key, edge)

    def add_bottom_edge(self, edge):
        key = (Direction.bottom, edge.length)
        self.bottom_edges.add_incident_edge(key, edge)

    def add_left_edge(self, edge):
        key = (Direction.left, edge.length)
        self.left_edges.add_incident_edge(key, edge)

    def remove_top_edges(self):
        del self.top_edges

    def remove_right_edges(self):
        del self.right_edges

    def remove_bottom_edges(self):
        del self.bottom_edges

    def remove_left_edges(self):
        del self.left_edges
        
    def add_incident_face(self, f):
        key = (f.level, f.id)
        self.face_incident_tree.insert(key, f)

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
