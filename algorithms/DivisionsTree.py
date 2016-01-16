# -*- coding: utf-8 -*-
import algorithms.CuttingUtils as cu
import numpy as np
import bintrees as bt
import sys

all_countours = bt.FastRBTree()
division_counter = 0
all_contour_counter = 0


def create_all_divisions_tree(mesh):
    root_contour_node = create_root_contour_node(mesh)
    generate_all_children_division_nodes(root_contour_node)
    return root_contour_node


def create_root_contour_node(mesh):
    root_contour_node = ContourNode(mesh.contour, None)
    add_to_all_contours(root_contour_node)
    return root_contour_node


def generate_all_children_division_nodes(contour_node):
    lowest_cost = sys.maxsize
    if not contour_node.contour.is_atomic_square():
        possible_cuts = cu.get_possible_cuts(contour_node.contour)
        for path in possible_cuts:
            lowest_cost = create_new_division_node(path, contour_node, lowest_cost)
        contour_node.set_lowest_cost(lowest_cost)
        return lowest_cost
    else:
        return get_leaf_cost()


def create_new_division_node(path, parent_contour_node, lowest_cost):
    global division_counter
    division_counter += 1
    new_division_node = DivisionNode(path, parent_contour_node)
    parent_contour_node.add_children_division(new_division_node)
    cost_of_child_1 = create_low_level_tree(new_division_node.contour_node_1, new_division_node)
    cost_of_child_2 = create_low_level_tree(new_division_node.contour_node_2, new_division_node)
    new_division_node.contour_node_1.lowest_cost = cost_of_child_1
    new_division_node.contour_node_2.lowest_cost = cost_of_child_2
    zlaczenia_koszt = dej_mi_zlaczenia_koszt(new_division_node)
    total_cost = cost_of_child_1 + cost_of_child_2 + zlaczenia_koszt
    new_division_node.cost = total_cost
    if total_cost < lowest_cost:
        lowest_cost = total_cost
    return lowest_cost


def create_low_level_tree(parent_contour_node, parent_division_node):
    if is_in_all_contours(parent_contour_node.contour):
        existing_contour_node = get_from_all_contours(parent_contour_node.contour)
        existing_contour_node.add_parent_division(parent_division_node)
        return existing_contour_node.lowest_cost
    else:
        add_to_all_contours(parent_contour_node)
        return generate_all_children_division_nodes(parent_contour_node)


def add_to_all_contours(contour_node):
    global all_countours
    global all_contour_counter
    all_contour_counter += 1
    perent_hash = contour_node.contour.hash_key
    if perent_hash in all_countours:
        all_countours[perent_hash] = np.append(all_countours[perent_hash], contour_node)
    else:
        all_countours[perent_hash] = np.array([contour_node])


def dej_mi_zlaczenia_koszt(division_node):
    a = 2*len(division_node.path) - 3
    b = 2 * len(division_node.parent_contour_node.contour) + a
    zlaczenia_koszt = cost(a, b)
    return zlaczenia_koszt


def get_leaf_cost():
    a = 1
    b = 9
    return cost(a, b)


def cost(a, b):
    return a * (6*b**2 - 6*a*b + 6*b + 2*a**2 - 3*a + 1) / 6


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

    def set_lowest_cost(self, lowest_cost):
        self.lowest_cost = lowest_cost


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
