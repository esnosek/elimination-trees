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

    def add_incident_edge(self, edge):
        if edge.v1 == self:
            v = edge.v2
        else:
            v = edge.v1

        if self.x == v.x:
            if self.y < v.y:
                self.__add_top_edge(edge)
            else:
                self.__add_bottom_edge(edge)
        else:
            if self.x < v.x:
                self.__add_right_edge(edge)
            else:
                self.__add_left_edge(edge)

    def __add_top_edge(self, edge):
        key = (Direction.top, edge.length)
        self.top_edges.add_incident_edge(key, edge)

    def __add_right_edge(self, edge):
        key = (Direction.right, edge.length)
        self.right_edges.add_incident_edge(key, edge)

    def __add_bottom_edge(self, edge):
        key = (Direction.bottom, edge.length)
        self.bottom_edges.add_incident_edge(key, edge)

    def __add_left_edge(self, edge):
        key = (Direction.left, edge.length)
        self.left_edges.add_incident_edge(key, edge)

    def add_incident_face(self, f):
        key = (f.level, f.id)
        self.face_incident_tree.insert(key, f)

    def __str__(self):
        s = ("[" + str(self.x) + ", " + str(self.y) + "]") + "\n"
        for key in self.edge_incident_tree:
            edge = self.edge_incident_tree[key]
            s = s + ("    " + str(edge)) + "\n"
        for face in self.face_incident_tree:
            s = s + ("        " + str(face)) + "\n"
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
