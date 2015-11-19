# -*- coding: utf-8 -*-

import bintrees as bt


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

    def is_empty(self):
        if self.edge_incident.is_empty():
            return True
        else:
            return False
