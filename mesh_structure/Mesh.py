# -*- coding: utf-8 -*-

import numpy as np
from mesh_structure.MeshContour import MeshContour
from copy import copy

class Mesh:

    def __init__(self, vertex_list, edge_list, face_list):
        self.vertex_list = vertex_list
        self.edge_list = edge_list
        self.face_list = face_list
        self.lower_left_vertex = self.__get_lower_left_vertex()
        self.upper_left_vertex = self.__get_upper_left_vertex()
        self.upper_right_vertex = self.__get_upper_right_vertex()
        self.lower_right_vertex = self.__get_lower_right_vertex()
        self.contour = MeshContour(self.__create_mesh_contour(), self)

    def __get_lower_left_vertex(self):
        return self.vertex_list.get_vertex((0, 0))

    def __get_upper_left_vertex(self):
        return self.vertex_list.get_vertex((0, self.vertex_list.get_max_y()))

    def __get_upper_right_vertex(self):
        return self.vertex_list.get_vertex((self.vertex_list.get_max_x(),
                                            self.vertex_list.get_max_y()))

    def __get_lower_right_vertex(self):
        return self.vertex_list.get_vertex((self.vertex_list.get_max_x(), 0))

    def __create_mesh_contour(self):
        contour_vertices = np.empty(dtype=object, shape=0)

        contour_vertices = np.append(contour_vertices, self.__get_left_border())
        contour_vertices = np.append(contour_vertices, self.__get_top_border())
        contour_vertices = np.append(contour_vertices, self.__get_right_border())
        contour_vertices = np.append(contour_vertices, self.__get_bottom_border())

        new_contour_vertices = copy(contour_vertices)
        
        for v in new_contour_vertices:
            v = copy(v)
            v.is_border_vertex = True
            v.change_vertex_in_neighbours() 

        return new_contour_vertices

    def __get_top_border(self):
        border_vertices = np.empty(dtype=object, shape=0)
        current_edge = self.upper_left_vertex.right_edges.get_longest_edge()
        border_vertices = np.append(border_vertices, copy(current_edge.v1))
        while current_edge.v1.x < self.upper_right_vertex.x:
            if current_edge.v2.x < self.upper_right_vertex.x:
                try:
                    current_edge = current_edge.v2.right_edges.get_longest_edge()
                    border_vertices = np.append(border_vertices,
                                                copy(current_edge.v1))
                except ValueError:
                    continue
            else:
                break
        return border_vertices

    def __get_right_border(self):
        border_vertices = np.empty(dtype=object, shape=0)
        current_edge = self.upper_right_vertex.bottom_edges.get_longest_edge()
        border_vertices = np.append(border_vertices, copy(current_edge.v2))
        while current_edge.v2.y > self.lower_right_vertex.y:
            if current_edge.v1.y > self.lower_right_vertex.y:
                try:
                    current_edge = current_edge.v1.bottom_edges.get_longest_edge()
                    border_vertices = np.append(border_vertices,
                                                copy(current_edge.v2))
                except ValueError:
                    continue
            else:
                break
        return border_vertices

    def __get_bottom_border(self):
        border_vertices = np.empty(dtype=object, shape=0)
        current_edge = self.lower_right_vertex.left_edges.get_longest_edge()
        border_vertices = np.append(border_vertices, copy(current_edge.v2))
        while current_edge.v2.x > self.lower_left_vertex.x:
            if current_edge.v1.x > self.lower_left_vertex.x:
                try:
                    current_edge = current_edge.v1.left_edges.get_longest_edge()
                    border_vertices = np.append(border_vertices,
                                                copy(current_edge.v2))
                except ValueError:
                    continue
            else:
                break
        return border_vertices

    def __get_left_border(self):
        border_vertices = np.empty(dtype=object, shape=0)
        current_edge = self.lower_left_vertex.top_edges.get_longest_edge()
        border_vertices = np.append(border_vertices, copy(current_edge.v1))
        while current_edge.v1.y < self.upper_left_vertex.y:
            if current_edge.v2.y < self.upper_left_vertex.y:
                try:
                    current_edge = current_edge.v2.top_edges.get_longest_edge()
                    border_vertices = np.append(border_vertices,
                                                copy(current_edge.v1))
                except ValueError:
                    continue
            else:
                break
        return border_vertices
