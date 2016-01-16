import numpy as np

optimal_tree_counter = 1


def create_optimal_elimination_tries(contour_node):
    global optimal_tree_counter
    if contour_node.contour.is_atomic_square():
        return OptimalTreeLeaf(contour_node.contour, contour_node.lowest_cost)
    lowest_cost_divisions = contour_node.get_divisions_with_lowest_cost()
    optimal_tree_contour_node = OptimalTreeContourNode(contour_node.lowest_cost)
    for division in lowest_cost_divisions:
        child_1 = create_optimal_elimination_tries(division.contour_node_1)
        child_2 = create_optimal_elimination_tries(division.contour_node_2)
        optimal_tree_contour_node.add_child(child_1, child_2, contour_node.contour, division.path)
    return optimal_tree_contour_node


class OptimalTreeContourNode:

    def __init__(self, cost):
        self.children = np.empty(dtype=object, shape=0)
        self.cost = cost

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
        self.contour = contour
        self.cost = cost
