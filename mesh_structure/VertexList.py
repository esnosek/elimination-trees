# -*- coding: utf-8 -*-

from mesh_structure.Vertex import Vertex
import bintrees as bt
import numpy as np


class VertexList:

    def __init__(self):
        self.vertex_tree = bt.FastRBTree()
        self.vertex_tree_y_sorted = bt.FastRBTree()

    def __str__(self):
        s = ""
        for key in self.vertex_tree:
            vertex = self.vertex_tree[key]
            s = s + str(vertex) + "\n"
        return s

    def create_vertex(self, x, y):
        v = Vertex(x, y)
        key_x = (x, y)
        key_y = (y, x)
        if key_x in self.vertex_tree:
            return self.vertex_tree[key_x]
        else:
            self.vertex_tree.insert(key_x, v)
            self.vertex_tree_y_sorted.insert(key_y, v)
        return v

    def get_values(self, column):
        list = np.array([], dtype=int)
        for k in self.vertex_tree.keys():
            list = np.append(list, k[column])
        return list

    def get_vertex(self, key):
        return self.vertex_tree[key]

    def get_max_x(self):
        return max(self.vertex_tree)[0]

    def get_max_y(self):
        return max(self.vertex_tree_y_sorted)[0]
