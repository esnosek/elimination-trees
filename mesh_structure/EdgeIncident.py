# -*- coding: utf-8 -*-

import bintrees as bt


class EdgeIncident:

    def __init__(self):
        self.edge_incident_tree = bt.FastRBTree()

    def add_incident_edge(self, key, e):
        self.edge_incident_tree.insert(key, e)

    def get_max_top_edge(self):
        return self.__get_longest_edge(0)

    def get_max_right_edge(self):
        return self.__get_longest_edge(1)

    def get_max_bottom_edge(self):
        return self.__get_longest_edge(2)

    def get_max_left_edge(self):
        return self.__get_longest_edge(3)

    def __get_longest_edge(self, direction):
        tree_slice = bt.FastRBTree(self.edge_incident_tree[(direction, 0):
                                                           (direction + 1, 0)])
        if not tree_slice.is_empty():
            return tree_slice[max(tree_slice)]
        else:
            raise ValueError

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
