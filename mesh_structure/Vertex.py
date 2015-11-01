# -*- coding: utf-8 -*-

import bintrees as bt
import functools as f
from mesh_structure.EdgeIncident import EdgeIncident


@f.total_ordering
class Vertex:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edge_incident = EdgeIncident()
        self.face_incident_tree = bt.FastRBTree()

    def add_incident_edge(self, e):
        if e.v1 == self:
            v = e.v2
        else:
            v = e.v1

        if self.x == v.x:
            if self.y < v.y:
                key = (0, e.length)
            else:
                key = (2, e.length)
        else:
            if self.x < v.x:
                key = (1, e.length)
            else:
                key = (3, e.length)

        self.edge_incident.add_incident_edge(key, e)

    def get_max_top_edge(self):
        return self.edge_incident.get_max_top_edge()

    def get_max_right_edge(self):
        return self.edge_incident.get_max_right_edge()

    def get_max_bottom_edge(self):
        return self.edge_incident.get_max_bottom_edge()

    def get_max_left_edge(self):
        return self.edge_incident.get_max_left_edge()

    def top_edge_exists(self):
        return self.edge_incident.top_edge_exists()

    def right_edge_exists(self):
        return self.edge_incident.right_edge_exists()

    def bottom_edge_exists(self):
        return self.edge_incident.bottom_edge_exists()

    def left_edge_exists(self):
        return self.edge_incident.left_edge_exists()

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
