# -*- coding: utf-8 -*-

import bintrees as bt
import numpy as np


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