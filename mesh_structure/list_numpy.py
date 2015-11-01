# -*- coding: utf-8 -*-

import numpy as np
from mesh_structure.VertexList import VertexList
from mesh_structure.EdgeList import EdgeList
from mesh_structure.FaceList import FaceList
from mesh_structure.Mesh import Mesh


def load_file(path):
    return np.loadtxt(path, dtype='int', skiprows=2)


def add_points(mesh):
    mesh = np.append(mesh, mesh[:, [2, 5]], 1)
    mesh = np.append(mesh, mesh[:, [4, 3]], 1)
    return mesh[:, np.array([0, 1, 2, 3, 6, 7, 4, 5, 8, 9])]


def get_max_x(mesh):
    return np.amax(mesh[:, [2, 4, 6, 8]])


def get_max_y(mesh):
    return np.amax(mesh[:, [3, 5, 7, 9]])


def create_mesh_structure(mesh):
    vertex_list = VertexList()
    edge_list = EdgeList()
    face_list = FaceList()
    for row in mesh:
        v1 = vertex_list.create_vertex(row[2], row[3])
        v2 = vertex_list.create_vertex(row[4], row[5])
        v3 = vertex_list.create_vertex(row[6], row[7])
        v4 = vertex_list.create_vertex(row[8], row[9])
        e1 = edge_list.create_edge(v1, v2)  # kolejnosc wazna: v1 < v2
        e2 = edge_list.create_edge(v1, v4)  # kolejnosc wazna: v1 < v4
        e3 = edge_list.create_edge(v2, v3)  # kolejnosc wazna: v2 < v3
        e4 = edge_list.create_edge(v4, v3)  # kolejnosc wazna: v4 < v3

        v_list = np.array([v1, v2, v3, v4])
        e_list = np.array([e1, e2, e3, e4])
        face_list.create_face(row[0], row[1], v_list, e_list)

    return Mesh(vertex_list, edge_list, face_list)
