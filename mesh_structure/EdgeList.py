# -*- coding: utf-8 -*-

from mesh_structure.Edge import Edge
import bintrees as bt


class EdgeList:

    def __init__(self):
        self.edge_tree = bt.FastRBTree()

    def create_edge(self, v1, v2):
        e = Edge(v1, v2)
        key = (v1.x, v1.y, v2.x, v2.y)
        if key in self.edge_tree:
            return self.edge_tree[key]
        else:
            v1.add_incident_edge(e)
            v2.add_incident_edge(e)
            self.edge_tree.insert(key, e)
        return e

    def add_edge(self, e):
        key = (e.v1.x, e.v1.y, e.v2.x, e.v2.y)
        self.edge_tree.insert(key, e)
        if key in self.edge_tree:
            return self.edge_tree[key]
        else:
            self.edge_tree.insert(key, e)
        return e

    def get_edge(self, key):
        return self.edge_tree[key]
