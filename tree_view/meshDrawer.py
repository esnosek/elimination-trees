import matplotlib.pyplot as plt
import numpy as np
from ete3 import Tree, faces, TreeStyle


plt.figure(figsize=(6,6))
counter = 1

used_vertices = {}
contour = None


def draw_tree_node(root_node):
    global counter
    fig, ax = plt.subplots(200, 1)
    from algorithms.DivisionTree import TreeLeaf
    while root_node is not TreeLeaf:
        draw_contour_from_optimal_tree(root_node.contour, 'k', ax)
        counter += 1
        draw_tree_node(root_node.child1)
        draw_tree_node(root_node.child2)


def draw_mesh(mesh, colour, file_name):
    for key in mesh.edge_list.edges:
        edge = mesh.edge_list.edges[key]
        plt.plot([edge.v1.x, edge.v2.x], [edge.v1.y, edge.v2.y], colour)
    plt.savefig(file_name)


def draw_contour_from_optimal_tree(vertex_list, colour, ax):
    global counter
    last_index = len(vertex_list) - 1
    for vertex in vertex_list:
        curr_index = np.where(vertex_list == vertex)[0][0]
        if curr_index == last_index:
            next_index = 0
        else:
            next_index = curr_index + 1
        v1 = vertex_list[curr_index]
        v2 = vertex_list[next_index]
        ax[counter].plot([v1.x, v2.x], [v1.y, v2.y], colour)
    plt.show()


def draw_leaf(mesh, tree_leaf, file_name, cost):
    plt.clf()
    #plt.axis([mesh.min_x, mesh.max_x, mesh.min_y, mesh.max_y])
    plt.xlabel(int(cost), fontsize=110)
    plt.gcf().subplots_adjust(bottom=0.30)
    draw_mesh(mesh, 'k', "do_usuniecia")
    draw_contour(tree_leaf.contour, 'k')
    plt.savefig(file_name)


def draw_contour_with_interior_and_slice(mesh, tree_node_child, file_name, cost):
    plt.clf()
    #plt.axis([mesh.min_x, mesh.max_x, mesh.min_y, mesh.max_y])
    plt.xlabel(int(cost), fontsize=110)
    plt.gcf().subplots_adjust(bottom=0.30)
    draw_mesh(mesh, 'k', "do_usuniecia")
    draw_contour(tree_node_child.contour, 'k')
    draw_contour_interior(tree_node_child.contour, 'k')
    draw_slice(tree_node_child.path, 'r')
    plt.savefig(file_name)


def draw_contour_with_interior_and_slice_from_division_node(mesh, division_node, file_name):
    plt.clf()
    draw_mesh(mesh, 'k', "do_usuniecia")
    draw_contour(division_node.parent_contour_node.contour, 'k')
    draw_contour_interior(division_node.parent_contour_node.contour, 'k')
    draw_slice(division_node.path, 'r')
    plt.savefig(file_name)


def draw_slice(slice_vertices, colour):
    last_index = len(slice_vertices) - 1
    curr_index = 0
    for vertex in slice_vertices:
        if curr_index == last_index:
            break
        next_index = curr_index + 1
        v1 = slice_vertices[curr_index]
        v2 = slice_vertices[next_index]
        plt.plot([v1.x, v2.x], [v1.y, v2.y], colour, linewidth=4.0)
        curr_index = curr_index + 1


def draw_contour(contour, colour):
    last_index = len(contour) - 1
    for vertex in contour.contour:
        curr_index = np.where(contour.contour == vertex)[0][0]
        if curr_index == last_index:
            next_index = 0
        else:
            next_index = curr_index + 1
        v1 = contour[curr_index]
        v2 = contour[next_index]
        plt.plot([v1.x, v2.x], [v1.y, v2.y], colour, linewidth=4.0)


def draw_contour_interior(contour, colour):
    global used_vertices
    used_vertices = {}

    for v in contour.contour:
        used_vertices[(v.x, v.y)] = False
    for v in contour.contour:
        visit_node(v, contour, colour)


def visit_node(v, contour, colour):
    global used_vertices

    used_vertices[(v.x, v.y)] = True
    if v in contour.contour:
        index_curr_v = np.where(contour.contour == v)[0][0]
        prev_v = contour[index_curr_v - 1]
        next_v = contour[index_curr_v + 1]
        inside_directions = contour.get_inside_directions(prev_v, v, next_v)
        existing_directions = v.get_existing_edge_directions()
        possible_directions = list(set(inside_directions).intersection(existing_directions))
    else:
        possible_directions = v.get_existing_edge_directions()
    for direction in possible_directions:
        edge = v.get_shortest_edge_in_direction(direction)
        if edge.v1 == v:
            v2 = edge.v2
        else:
            v2 = edge.v1
        plt.plot([v.x, v2.x], [v.y, v2.y], colour, linewidth=2.0)
        if not (v2.x, v2.y) in used_vertices:
            visit_node(v2, contour, colour)


def draw_slice_and_contour(mesh, tree_node, file_name='tmp.png'):
    for child in tree_node.children:
        draw_slice(mesh, child.path, 'r')
    draw_contour(mesh, tree_node.contour.contour, 'k')
    plt.savefig(file_name)


def draw_table():
    plt.axis([0, 9, 0, 9])
    i = 1
    while i <= 9:
        plt.plot([i,i], [0,9], 'k', linewidth=2.0)
        plt.plot([0,9], [i,i], 'k', linewidth=2.0)
        i += 1
    plt.savefig("tabelka.png")


def draw_tree(tree_string):
    
    t = Tree(tree_string, format=8)
    
    def mylayout(node):
        #if node.name != 'L':
        file = 'tmp/%s.png' % node.name
        new_face = faces.ImgFace(file)
        new_face.rotable = True
        new_face.rotation = -90
        #new_face.margin_top = 50
        new_face.margin_left = 15
        faces.add_face_to_node(new_face, node, column=0 , position='branch-top')
        
    ts = TreeStyle()
    ts.rotation = 90
    ts.layout_fn = mylayout
    t.show(tree_style = ts)
    


    
    
    

