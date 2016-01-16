import time
import mesh_structure.VertexUtils as vu
import mesh_structure.EdgeUtils as eu
import mesh_structure.Mesh as m
import numpy as np
import algorithms.DivisionTree as dt
import tree_view.meshDrawer as md

fileName = "mesh_tests/edge"


def create_mesh(fileName=fileName):
    mesh = load_file(fileName)
    mesh = add_points(mesh)
    return create_mesh_structure(mesh)


def find_all_divisions_tree(mesh):
    dt.start(mesh)


def load_file(path):
    return np.loadtxt(path, dtype='int', skiprows=2)


def add_points(mesh):
    mesh = np.append(mesh, mesh[:, [2, 5]], 1)
    mesh = np.append(mesh, mesh[:, [4, 3]], 1)
    return mesh[:, np.array([0, 1, 2, 3, 6, 7, 4, 5, 8, 9])]


def create_mesh_structure(mesh):
    for row in mesh:
        v1 = vu.create_vertex(row[2], row[3])
        v2 = vu.create_vertex(row[4], row[5])
        v3 = vu.create_vertex(row[6], row[7])
        v4 = vu.create_vertex(row[8], row[9])
        eu.create_edge(v1, v2)  # kolejnosc wazna: v1 < v2
        eu.create_edge(v1, v4)  # kolejnosc wazna: v1 < v4
        eu.create_edge(v2, v3)  # kolejnosc wazna: v2 < v3
        eu.create_edge(v4, v3)  # kolejnosc wazna: v4 < v3

    return m.Mesh(vu.sorted_vertex_lists, eu.sorted_edge_list)


start_time = int(round(time.time() * 100000))

mesh = create_mesh(fileName)
find_all_divisions_tree(mesh)

print("")
print("wszystkie kontury: ", dt.all_contour_counter)
print("unikalne hashcody: ", len(dt.all_countours))
print("wszystkie podziały ", dt.division_counter)
print("optymalne drzewa ", dt.optimal_tree_counter)

dt.clear_tmp()
tree_string = dt.create_tree_string(mesh, dt.root)
tree_string += ';'
md.draw_tree(tree_string)

end_time = int(round(time.time() * 100000))
print('czas: ' + str((end_time - start_time)/100000) + 's')
