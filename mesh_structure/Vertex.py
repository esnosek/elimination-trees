# -*- coding: utf-8 -*-

import bintrees as bt
import functools as f


@f.total_ordering
class Vertex:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edge_incident_tree = bt.FastRBTree()
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

        self.edge_incident_tree.insert(key, e)

    def get_max_top_edge(self):
        return self.__get_longest_edge(0)

    def get_max_right_edge(self):
        return self.__get_longest_edge(1)

    def get_max_bottom_edge(self):
        return self.__get_longest_edge(2)

    def get_max_left_edge(self):
        return self.__get_longest_edge(3)

    def top_edge_exists(self):
        return self.__edge_exists(0)

    def right_edge_exists(self):
        return self.__edge_exists(1)

    def bottom_edge_exists(self):
        return self.__edge_exists(2)

    def left_edge_exists(self):
        return self.__edge_exists(3)

    def __edge_exists(self, direction):
        tree_slice = bt.FastRBTree(self.edge_incident_tree[(direction, 0):
                                                           (direction + 1, 0)])
        if not tree_slice.is_empty():
            return False
        else:
            return True

    def add_incident_face(self, f):
        key = (f.level, f.id)
        self.face_incident_tree.insert(key, f)

    def __get_longest_edge(self, direction):
        tree_slice = bt.FastRBTree(self.edge_incident_tree[(direction, 0):
                                                           (direction + 1, 0)])
        if not tree_slice.is_empty():
            return tree_slice[max(tree_slice)]
        else:
            raise ValueError

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
