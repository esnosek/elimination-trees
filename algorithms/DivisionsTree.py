# -*- coding: utf-8 -*-
import algorithms.CuttingUtils as CuttingUtils
import numpy as np
import sys

class DivisionsTree:
    
    def __init__(self, mesh):
        self.mesh = mesh
        self.root_contour_node = None
        
    def create_all_divisions_tree(self):
        self.root_contour_node = self.create_root_contour_node()
        self.generate_all_children_division_nodes(self.root_contour_node)
        return self.root_contour_node
    
    
    def create_root_contour_node(self):
        root_contour_node = ContourNode(self.mesh.contour, None)
        self.mesh.add_to_all_contour_nodes(root_contour_node)
        return root_contour_node
    
    
    def generate_all_children_division_nodes(self, contour_node):
        lowest_cost = sys.maxsize
        if not contour_node.contour.is_atomic_square():
            cu = CuttingUtils.PathsFinder(contour_node.contour)
            possible_cuts = cu.get_possible_paths()
            for path in possible_cuts:
                lowest_cost = self.create_new_division_node(path, contour_node, lowest_cost)
            contour_node.set_lowest_cost(lowest_cost)
            counter = 0
            for d in contour_node.children_division_nodes:
                counter += d.all_divisions_tree_counter
            contour_node.all_divisions_tree_counter = counter
            return lowest_cost
        else:
            contour_node.all_divisions_tree_counter = 1
            return self.get_leaf_cost()
    
    
    def create_new_division_node(self, path, parent_contour_node, lowest_cost):
        new_division_node = DivisionNode(self.mesh, path, parent_contour_node)
        parent_contour_node.add_children_division(new_division_node)
        cost_of_child_1 = self.create_low_level_tree(new_division_node.contour_node_1, new_division_node)
        cost_of_child_2 = self.create_low_level_tree(new_division_node.contour_node_2, new_division_node)
        new_division_node.contour_node_1.lowest_cost = cost_of_child_1
        new_division_node.contour_node_2.lowest_cost = cost_of_child_2
        new_division_node.all_divisions_tree_counter = new_division_node.contour_node_1.all_divisions_tree_counter * new_division_node.contour_node_2.all_divisions_tree_counter
        zlaczenia_koszt = self.dej_mi_zlaczenia_koszt(new_division_node)
        total_cost = cost_of_child_1 + cost_of_child_2 + zlaczenia_koszt
        new_division_node.cost = total_cost
        if total_cost < lowest_cost:
            lowest_cost = total_cost
        return lowest_cost
    
    
    def create_low_level_tree(self, parent_contour_node, parent_division_node):
        if self.mesh.is_in_all_contour_nodes(parent_contour_node.contour):
            existing_contour_node = self.mesh.get_from_all_contour_nodes(parent_contour_node.contour)
            existing_contour_node.add_parent_division(parent_division_node)
            return existing_contour_node.lowest_cost
        else:
            self.mesh.add_to_all_contour_nodes(parent_contour_node)
            return self.generate_all_children_division_nodes(parent_contour_node)
    
    
    def dej_mi_zlaczenia_koszt(self, division_node):
        a = 2*len(division_node.path) - 3
        b = 2 * len(division_node.parent_contour_node.contour) + a
        zlaczenia_koszt = self.cost(a, b)
        return zlaczenia_koszt
    
    
    def get_leaf_cost(self):
        a = 1
        b = 9
        return self.cost(a, b)
    
    
    def cost(self, a, b):
        return a * (6*b**2 - 6*a*b + 6*b + 2*a**2 - 3*a + 1) / 6


class ContourNode:

    def __init__(self, contour, parent_division_node):
        self.contour = contour
        self.children_division_nodes = np.empty(dtype=object, shape=0)
        self.parent_division_nodes = np.empty(dtype=object, shape=0)
        self.add_parent_division(parent_division_node)
        self.lowest_cost = None
        self.all_divisions_tree_counter = 0

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

    def set_lowest_cost(self, lowest_cost):
        self.lowest_cost = lowest_cost


class DivisionNode:

    def __init__(self, mesh, path, parent_contour_node):
        self.path = path
        self.parent_contour_node = parent_contour_node
        cs = CuttingUtils.ContourSlice(parent_contour_node.contour, path)
        new_contour1, new_contour2 = cs.slice_contour()
        self.contour_node_1 = self.create_contour_node(mesh, new_contour1)
        self.contour_node_2 = self.create_contour_node(mesh, new_contour2)
        self.cost = None
        self.all_divisions_tree_counter = 0

    def create_contour_node(self, mesh, contour):
        if mesh.is_in_all_contour_nodes(contour):
            existing_contour_node = mesh.get_from_all_contour_nodes(contour)
            return existing_contour_node
        else:
            return ContourNode(contour, self)
