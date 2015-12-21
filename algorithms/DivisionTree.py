# -*- coding: utf-8 -*-
import algorithms.CuttingUtils as cu
import numpy as np
from test import create_mesh
import bintrees as bt
import unittest
import tree_view.meshDrawer as md

all_countours = bt.FastRBTree()
counter = 0
all_contour_counter = 1


def start(mesh):
    global all_countours
    root = ContourNode(mesh.contour, None)
    all_countours[hash(root.contour.center)] = [root]
    
    root.generate_all_children_division_nodes()


def create_tree(parent_contour_node, parent_division_node):
    global all_countours
    global all_contour_counter
    
    if is_in_all_contours(parent_contour_node):
        existing_contour_node = get_from_all_contours(parent_contour_node)
        existing_contour_node.add_parent_division(parent_division_node)
    else:
        all_contour_counter += 1
        perent_hash = hash(parent_contour_node.contour.center)
        if perent_hash in all_countours:
            all_countours[perent_hash].append(parent_contour_node)
        else:
            all_countours[perent_hash] = [parent_contour_node]
            
        parent_contour_node.generate_all_children_division_nodes()
        
def is_in_all_contours(contour_node):
    contour_hash_key = hash(contour_node.contour.center)
    if contour_hash_key in all_countours:
        for c in all_countours[contour_hash_key]:
            if c == contour_node:
                return True
    return False
    
def get_from_all_contours(contour_node):
    contour_hash_key = hash(contour_node.contour.center)
    if contour_hash_key in all_countours:
        for c in all_countours[contour_hash_key]:
            if c == contour_node:
                return c
    return False


class ContourNode:
    def __init__(self, contour, parent_division_node):
        self.contour = contour
        self.children_division_nodes = np.empty(dtype=object, shape=0)
        self.parent_division_nodes = np.empty(dtype=object, shape=0)
        self.add_parent_division(parent_division_node)

    def add_parent_division(self, parent_division_node):
        self.parent_division_nodes = np.append(self.parent_division_nodes, parent_division_node)

    def add_children_division(self, children_division_node):
        self.children_division_nodes = np.append(self.children_division_nodes, children_division_node)

    def generate_all_children_division_nodes(self):
        global counter
        if not self.__is_atomic_square(self.contour):
            possible_cuts = cu.get_possible_cuts(self.contour)
            for path in possible_cuts:
                new_division_node = DivisionNode(path, self)
                self.add_children_division(new_division_node)
                create_tree(new_division_node.contour_node_1, new_division_node)
                create_tree(new_division_node.contour_node_2, new_division_node)
        else:
            counter = counter + 1
            print(counter)
            for v in self.contour.contour:
                print(v)

    def __is_atomic_square(self, parent_contour):
        for v in parent_contour.contour:
            index_curr_v = np.where(parent_contour.contour == v)[0][0]
            index_prev_v = index_curr_v - 1
            index_next_v = index_curr_v + 1
            prev_v = parent_contour[index_prev_v]
            next_v = parent_contour[index_next_v]
            inside_directions = parent_contour.get_inside_directions(prev_v, v, next_v)
            existing_directions = v.get_existing_edge_directions()
            possible_directions = list(set(inside_directions).intersection(existing_directions))
            if len(possible_directions) > 0:
                return False
        return True

    def __eq__(self, other):
        return self.contour == other.contour


class DivisionNode:
    def __init__(self, path, parent_contour_node):
        self.parent_contour_node = parent_contour_node
        new_contour1, new_contour2 = parent_contour_node.contour.slice_contour(path)
        self.contour_node_1 = ContourNode(new_contour1, self)
        self.contour_node_2 = ContourNode(new_contour2, self)

class DivisionTreeTests(unittest.TestCase):

    def test_cut(self):
        global all_countours
        mesh = create_mesh()
        start(mesh)
        print(len(all_countours))
        print(all_contour_counter)

if __name__ == '__main__':
    unittest.main()
