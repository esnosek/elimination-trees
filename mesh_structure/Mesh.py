# -*- coding: utf-8 -*-

import numpy as np
from mesh_structure.MeshContour import MeshContour


class Mesh:

    def __init__(self, vertex_list, edge_list, face_list):
        self.vertex_list = vertex_list
        self.edge_list = edge_list
        self.face_list = face_list
        self.lower_left_vertex = self.__get_lower_left_vertex()
        self.upper_left_vertex = self.__get_upper_left_vertex()
        self.upper_right_vertex = self.__get_upper_right_vertex()
        self.lower_right_vertex = self.__get_lower_right_vertex()
        self.contour = MeshContour(self.__create_mesh_contour())

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
        contour_edges = np.empty(dtype=object, shape=0)

        contour_edges = np.append(contour_edges, self.__get_left_border())
        contour_edges = np.append(contour_edges, self.__get_top_border())
        contour_edges = np.append(contour_edges, self.__get_right_border())
        contour_edges = np.append(contour_edges, self.__get_bottom_border())

        return contour_edges

    def __get_top_border(self):
        start_v = self.upper_left_vertex
        end_v = self.upper_right_vertex
        condition = (lambda start_v, end_v: start_v.x < end_v.x)
        get_edge = (lambda v: v.right_edges.get_longest_edge())
        slice_edges = np.empty(dtype=object, shape=0)
        edge = get_edge(start_v)
        slice_edges = np.append(slice_edges, edge)
        fl = True
        while condition(edge.v1, end_v) and fl:
            if condition(edge.v2, end_v):
                try:
                    edge = get_edge(edge.v2)
                except ValueError:
                    continue
                slice_edges = np.append(slice_edges, edge)
            else:
                fl = False

        return slice_edges

    def __get_right_border(self):
        start_v = self.upper_right_vertex
        end_v = self.lower_right_vertex
        condition = (lambda start_v, end_v: start_v.y > end_v.y)
        get_edge = (lambda v: v.bottom_edges.get_longest_edge())
        slice_edges = np.empty(dtype=object, shape=0)
        edge = get_edge(start_v)
        slice_edges = np.append(slice_edges, edge)
        fl = True
        while condition(edge.v2, end_v) and fl:
            if condition(edge.v1, end_v):
                try:
                    edge = get_edge(edge.v1)
                except ValueError:
                    continue
                slice_edges = np.append(slice_edges, edge)
            else:
                fl = False

        return slice_edges

    def __get_bottom_border(self):
        start_v = self.lower_right_vertex
        end_v = self.lower_left_vertex
        condition = (lambda start_v, end_v: start_v.x > end_v.x)
        get_edge = (lambda v: v.left_edges.get_longest_edge())
        slice_edges = np.empty(dtype=object, shape=0)
        edge = get_edge(start_v)
        slice_edges = np.append(slice_edges, edge)
        fl = True
        while condition(edge.v2, end_v) and fl:
            if condition(edge.v1, end_v):
                try:
                    edge = get_edge(edge.v1)
                except ValueError:
                    continue
                slice_edges = np.append(slice_edges, edge)
            else:
                fl = False

        return slice_edges

    def __get_left_border(self):
        start_v = self.lower_left_vertex
        end_v = self.upper_left_vertex
        condition = (lambda start_v, end_v: start_v.y < end_v.y)
        get_edge = (lambda v: v.top_edges.get_longest_edge())
        slice_edges = np.empty(dtype=object, shape=0)
        edge = get_edge(start_v)
        slice_edges = np.append(slice_edges, edge)
        fl = True
        while condition(edge.v1, end_v) and fl:
            if condition(edge.v2, end_v):
                try:
                    edge = get_edge(edge.v2)
                except ValueError:
                    continue
                slice_edges = np.append(slice_edges, edge)
            else:
                fl = False

        return slice_edges
