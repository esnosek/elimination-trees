# -*- coding: utf-8 -*-
import algorithms.CuttingUtils as cu
import numpy as np
from test import create_mesh
import bintrees as bt
import unittest
import tree_view.meshDrawer as md

all_countours = bt.FastRBTree()
optimal_tree_nodes = bt.FastRBTree()
counter = 0
all_contour_counter = 1
ilosc_rozwiazan = 1
root = None
root_contour_node = None

def start(mesh):
    global all_countours
    global root
    global root_contour_node
    root_contour_node = ContourNode(mesh.contour, None)
    all_countours[root_contour_node.contour.hash_key] = np.array([root_contour_node])
    cost = root_contour_node.generate_all_children_division_nodes()
    #print(cost, [str(v) for v in root_optimal_tree.path])
    print(cost)
    root_contour_node.set_lowest_cost()
    root = create_optimal_tree(root_contour_node)
    md.draw_slice_and_contour(root)

def create_optimal_tree(contour_node):
    if contour_node.is_atomic_square(contour_node.contour):
        return TreeLeaf(contour_node.contour)
    contour_node.set_lowest_cost()
    for division in contour_node.children_division_nodes:
        print(contour_node.lowest_cost, division.cost)
        if contour_node.lowest_cost == division.cost:
            print(division.contour_node_1.contour)
            print(division.contour_node_2.contour)
            tree_node_1 = create_optimal_tree(division.contour_node_1)
            tree_node_2 = create_optimal_tree(division.contour_node_2)
            return TreeNode(contour_node.contour, division.path, tree_node_1, tree_node_2)
            break
    print("---------------")

 
def create_tree(parent_contour_node, parent_division_node):
    global all_countours
    global all_contour_counter
    
    if is_in_all_contours(parent_contour_node):
        existing_contour_node = get_from_all_contours(parent_contour_node)
        existing_contour_node.add_parent_division(parent_division_node)
    else:
        all_contour_counter += 1
        perent_hash = parent_contour_node.contour.hash_key
        if perent_hash in all_countours:
            all_countours[perent_hash] = np.append(all_countours[perent_hash], parent_contour_node)
        else:
            all_countours[perent_hash] = np.array([parent_contour_node])
            return parent_contour_node.generate_all_children_division_nodes()

def is_in_optimal_tree_nodes(contour_node):
    contour_hash_key = contour_node.contour.hash_key
    if contour_hash_key in optimal_tree_nodes:
        for tree_node in optimal_tree_nodes[contour_hash_key]:
            if tree_node.contour == contour_node.contour:
                return True
    return False
    
def get_from_optimal_tree_nodes(contour_node):
    contour_hash_key = contour_node.contour.hash_key
    if contour_hash_key in optimal_tree_nodes:
        for tree_node in optimal_tree_nodes[contour_hash_key]:
            if tree_node.contour == contour_node.contour:
                return tree_node
    return False
         
def is_in_all_contours(contour_node):
    contour_hash_key = contour_node.contour.hash_key
    if contour_hash_key in all_countours:
        for c in all_countours[contour_hash_key]:
            if c == contour_node:
                return True
    return False
    
def get_from_all_contours(contour_node):
    contour_hash_key = contour_node.contour.hash_key
    if contour_hash_key in all_countours:
        for c in all_countours[contour_hash_key]:
            if c == contour_node:
                return c
    return False

class TreeNode:
    
    def __init__(self, contour, path, child1, child2):
        self.contour = contour
        self.path = path
        self.child1 = child1
        self.child2 = child2

class TreeLeaf:

    def __init__(self, contour):
        self.contour = contour
    
class ContourNode:

    def __init__(self, contour, parent_division_node):
        self.contour = contour
        self.children_division_nodes = np.empty(dtype=object, shape=0)
        self.parent_division_nodes = np.empty(dtype=object, shape=0)
        self.add_parent_division(parent_division_node)
        self.lowest_cost = None

    def __eq__(self, other):
        return self.contour == other.contour

    def add_parent_division(self, parent_division_node):
        self.parent_division_nodes = np.append(self.parent_division_nodes, parent_division_node)

    def add_children_division(self, children_division_node):
        self.children_division_nodes = np.append(self.children_division_nodes, children_division_node)
        
    def set_lowest_cost(self):
        lowest_cost = 999999999
        for division in self.children_division_nodes:
            if division.cost < lowest_cost:
                lowest_cost = division.cost
        self.lowest_cost = lowest_cost
        
    def get_cost(self):
        a = 1
        b = 9
        return self.cost(a, b)

    def generate_all_children_division_nodes(self):
        global optimal_tree_nodes
        global counter
        global ilosc_rozwiazan
        lowest_cost = 9999999
        
        if not self.is_atomic_square(self.contour):
            possible_cuts = cu.get_possible_cuts(self.contour)
            for path in possible_cuts:
                new_division_node = DivisionNode(path, self)
                self.add_children_division(new_division_node)
                new_division_node.contour_node_1.lowest_cost = create_tree(new_division_node.contour_node_1, new_division_node)
                new_division_node.contour_node_2.lowest_cost = create_tree(new_division_node.contour_node_2, new_division_node)
                zlaczenia_koszt = self.__dej_mi_zlaczenia_koszt(new_division_node)
                new_division_node.cost = zlaczenia_koszt
                if zlaczenia_koszt < lowest_cost:
                    lowest_cost = zlaczenia_koszt
                    lowest_division_node = new_division_node
            return lowest_cost
        else:
            return self.get_cost()

    def __dej_mi_zlaczenia_koszt(self, division_node):
        a = 2*len(division_node.path) - 3
        b = 2 * len(division_node.parent_contour_node.contour) + a
        cost = self.cost(a, b)
        return cost
        
    def cost(self, a, b):
        return a * (6*b**2 - 6*a*b + 6*b + 2*a**2 - 3*a + 1) / 6

    def is_atomic_square(self, parent_contour):
        for v in parent_contour.contour:
            index_curr_v = np.where(parent_contour.contour == v)[0][0]
            prev_v = parent_contour[index_curr_v - 1]
            next_v = parent_contour[index_curr_v + 1]
            inside_directions = parent_contour.get_inside_directions(prev_v, v, next_v)
            existing_directions = v.get_existing_edge_directions()
            possible_directions = list(set(inside_directions).intersection(existing_directions))
            if len(possible_directions) > 0:
                return False
        return True


class DivisionNode:

    def __init__(self, path, parent_contour_node):
        self.path = path
        self.parent_contour_node = parent_contour_node
        new_contour1, new_contour2 = parent_contour_node.contour.slice_contour(path)
        self.contour_node_1 = ContourNode(new_contour1, self)
        self.contour_node_2 = ContourNode(new_contour2, self)
        self.cost = None

class DivisionTreeTests(unittest.TestCase):

    def test_cut(self):
        global all_countours
        mesh = create_mesh()
        start(mesh)
        print("ilość unikalnych hashcodów: ", len(all_countours))
        print("ilosc wszystkich kontorów: ", all_contour_counter)

if __name__ == '__main__':
    unittest.main()
