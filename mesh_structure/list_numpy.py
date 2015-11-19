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


def visit_face(self, face):
    self.visited_list = np.append(self.visited_list, face)
    for edge in face.edge_list:
        if (edge not in self.visited_edge) and (edge not in self.contour):
            self.visited_edge = np.append(self.visited_edge, edge)
            for f_key in edge.face_incident:
                next_face = edge.face_incident[f_key]
                if (next_face != face) and (next_face not in self.visited_list):
                    self.visit_face(next_face)


def depth_first_search(self):
    first_edge = self.contour[0]
    first_face = min(first_edge.face_incident)
    first_face = first_edge.face_incident[first_face]
    self.visit_face(first_face)


def test_slice(mesh):
    v1 = mesh.vertex_list.get_vertex((12, 8))
    v2 = mesh.vertex_list.get_vertex((12, 4))
    v3 = mesh.vertex_list.get_vertex((8, 4))
    v4 = mesh.vertex_list.get_vertex((4, 4))
    v5 = mesh.vertex_list.get_vertex((4, 0))
    slice_vertices = np.empty(dtype=object, shape=0)
    slice_vertices = np.append(slice_vertices, v1)
    slice_vertices = np.append(slice_vertices, v2)
    slice_vertices = np.append(slice_vertices, v3)
    slice_vertices = np.append(slice_vertices, v4)
    slice_vertices = np.append(slice_vertices, v5)

    v21 = mesh.vertex_list.get_vertex((6, 0))
    v22 = mesh.vertex_list.get_vertex((6, 4))
    slice_vertices2 = np.empty(dtype=object, shape=0)
    slice_vertices2 = np.append(slice_vertices2, v21)
    slice_vertices2 = np.append(slice_vertices2, v22)
    mesh.contour.slice_contour(slice_vertices2)


def slice_contour(self, start_v, end_v, slice_edges):
    index_e1 = np.where(self.contour == start_v)
    index_e2 = np.where(self.contour == end_v)

    edge_list_1 = self.contour[index_e1:index_e2]
    edge_list_1 = np.append(edge_list_1, slice_edges[::-1])

    edge_list_2 = self.contour[:index_e1]
    edge_list_3 = self.contour[index_e2:]
    edge_list_2 = np.append(edge_list_2, slice_edges)
    edge_list_2 = np.append(edge_list_2, edge_list_3)

    return edge_list_1, edge_list_2
