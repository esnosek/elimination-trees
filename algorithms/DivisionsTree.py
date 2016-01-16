# -*- coding: utf-8 -*-
import algorithms.CuttingUtils as cu
import numpy as np
import bintrees as bt
import unittest

all_countours = bt.FastRBTree()
root = None
root_contour_node = None
division_counter = 0
all_contour_counter = 0

def create_all_divisions_tree(mesh):
    global all_countours
    global root
    global root_contour_node
    root_contour_node = ContourNode(mesh.contour, None)
    all_countours[root_contour_node.contour.hash_key] = np.array([root_contour_node])
    root_contour_node.generate_all_children_division_nodes()
    root_contour_node.set_lowest_cost()
    return root_contour_node

def create_tree(parent_contour_node, parent_division_node):
    global all_countours
    global all_contour_counter
    
    if is_in_all_contours(parent_contour_node.contour):
        existing_contour_node = get_from_all_contours(parent_contour_node.contour)
        existing_contour_node.add_parent_division(parent_division_node)
        return existing_contour_node.lowest_cost
    else:
        all_contour_counter += 1
        perent_hash = parent_contour_node.contour.hash_key
        if perent_hash in all_countours:
            all_countours[perent_hash] = np.append(all_countours[perent_hash], parent_contour_node)
        else:
            all_countours[perent_hash] = np.array([parent_contour_node])
        return parent_contour_node.generate_all_children_division_nodes()

def get_from_all_contours(contour):
    contour_hash_key = contour.hash_key
    if contour_hash_key in all_countours:
        for contour_node in all_countours[contour_hash_key]:
            if contour_node.contour == contour:
                return contour_node
    return False
        
def is_in_all_contours(contour):
    contour_hash_key = contour.hash_key
    if contour_hash_key in all_countours:
        for contour_node in all_countours[contour_hash_key]:
            if contour_node.contour == contour:
                return True
    return False   
        
class TreeNode:
    
    def __init__(self, cost):
        self.children = []
        self.cost = cost
        
    def add_child(self, child1, child2, contour, path):
        self.children.append(TreeNodeChild(child1, child2, contour, path))

class TreeNodeChild:
    def __init__(self, child1, child2, contour, path):
        self.contour = contour
        self.child1 = child1
        self.child2 = child2
        self.path = path
        
class TreeLeaf:

    def __init__(self, contour, cost):
        self.contour = contour
        self.cost = cost
    
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

    def get_divisions_with_lowest_cost(self):
        lowest_divisions = np.empty(dtype=object, shape=0)
        for division in self.children_division_nodes:
            if self.lowest_cost == division.cost:
                lowest_divisions = np.append(lowest_divisions, division)
        return lowest_divisions
        
    def set_lowest_cost(self):
        costs = []
        for division in self.children_division_nodes:
            costs.append(division.cost)
        self.lowest_cost = min(costs)
        
    def get_cost(self):
        a = 1
        b = 9
        return self.cost(a, b)

    def generate_all_children_division_nodes(self):
        global division_counter
        lowest_cost = 9999999
        
        if not self.is_atomic_square(self.contour):
            possible_cuts = cu.get_possible_cuts(self.contour)
            for path in possible_cuts:
                division_counter += 1
                new_division_node = DivisionNode(path, self)
                self.add_children_division(new_division_node)
                cost_of_child_1 = create_tree(new_division_node.contour_node_1, new_division_node)
                cost_of_child_2 = create_tree(new_division_node.contour_node_2, new_division_node)
                new_division_node.contour_node_1.lowest_cost = cost_of_child_1
                new_division_node.contour_node_2.lowest_cost = cost_of_child_2
                zlaczenia_koszt = self.__dej_mi_zlaczenia_koszt(new_division_node)
                total_cost = cost_of_child_1 + cost_of_child_2 + zlaczenia_koszt
                new_division_node.cost = total_cost
                if total_cost < lowest_cost:
                    lowest_cost = total_cost
                
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
        if len(parent_contour) == 4:
            return True
        else:
            return False


class DivisionNode:

    def __init__(self, path, parent_contour_node):
        self.path = path
        self.parent_contour_node = parent_contour_node
        new_contour1, new_contour2 = parent_contour_node.contour.slice_contour(path)
        self.contour_node_1 = self.create_contour_node(new_contour1)
        self.contour_node_2 = self.create_contour_node(new_contour2)
        self.cost = None

    def create_contour_node(self, contour):
        if is_in_all_contours(contour):
            existing_contour_node = get_from_all_contours(contour)
            return existing_contour_node
        else:
            return ContourNode(contour, self)


class DivisionTreeTests(unittest.TestCase):

    def test_cut(self):
        pass

if __name__ == '__main__':
    unittest.main()
