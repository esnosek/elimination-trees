import numpy as np


def create_optimal_elimination_tries(contour_node):
    if contour_node.contour.is_atomic_square():
        return OptimalTreeLeaf(contour_node.contour, contour_node.lowest_cost)
    lowest_cost_divisions = contour_node.get_divisions_with_lowest_cost()
    optimal_tree_contour_node = OptimalTreeContourNode(contour_node.lowest_cost)
    counter = 0
    for division in lowest_cost_divisions:
        child_1 = create_optimal_elimination_tries(division.contour_node_1)
        child_2 = create_optimal_elimination_tries(division.contour_node_2)
        optimal_tree_contour_node.add_child(child_1, child_2, contour_node.contour, division.path)
        children1 = child_1.optimal_tree_counter
        children2 = child_2.optimal_tree_counter
        counter += children1 * children2
    optimal_tree_contour_node.optimal_tree_counter = counter
    return optimal_tree_contour_node


class OptimalTreeContourNode:

    def __init__(self, cost):
        self.children = np.empty(dtype=object, shape=0)
        self.cost = cost
        self.optimal_tree_counter = 0

    def add_child(self, child1, child2, contour, path):
        self.children = np.append(self.children, OptimalTreeDivisionNode(child1, child2, contour, path))


class OptimalTreeDivisionNode:

    def __init__(self, child1, child2, contour, path):
        self.contour = contour
        self.child1 = child1
        self.child2 = child2
        self.path = path


class OptimalTreeLeaf:

    def __init__(self, contour, cost):
        self.optimal_tree_counter = 1
        self.contour = contour
        self.cost = cost
