import algorithms.DivisionsTree as dt

optimal_tree_counter = 1


def create_optimal_elimination_tries(contour_node):
    global optimal_tree_counter
    if contour_node.is_atomic_square(contour_node.contour):
        return dt.TreeLeaf(contour_node.contour, contour_node.lowest_cost)
    lowest_cost_divisions = contour_node.get_divisions_with_lowest_cost()
    tree_node = dt.TreeNode(contour_node.lowest_cost)
    optimal_tree_counter = optimal_tree_counter + len(lowest_cost_divisions)-1
    for division in lowest_cost_divisions:
        child_1 = create_optimal_elimination_tries(division.contour_node_1)
        child_2 = create_optimal_elimination_tries(division.contour_node_2)
        tree_node.add_child(child_1, child_2, contour_node.contour, division.path)
    return tree_node
