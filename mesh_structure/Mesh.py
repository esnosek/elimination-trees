# -*- coding: utf-8 -*-

import numpy as np


class Mesh:

    def __init__(self, vertex_list, edge_list, face_list):
        self.vertex_list = vertex_list
        self.edge_list = edge_list
        self.face_list = face_list
        self.max_x = self.vertex_list.get_max_x()
        self.max_y = self.vertex_list.get_max_y()
        self.min_x = 0
        self.min_y = 0
        self.contour = self.__create_mesh_contour()

    def is_slicable_top(self, v):
        condition = (lambda v1: v1.y < self.max_y)
        get_max_edge = (lambda v1: v1.get_edges_incident().get_max_top_edge())
        return self.__break_on_trough(v, get_max_edge, condition)

    def is_slicable_right(self, v):
        condition = (lambda v1: v1.x < self.max_x)
        get_max_edge = (lambda v1: v1.get_edges_incident().get_max_right_edge())
        return self.__break_on_trough(v, get_max_edge, condition)

    def is_slicable_bottom(self, v):
        condition = (lambda v1: v1.y > self.min_y)
        get_max_edge = (lambda v1: v1.get_edges_incident().get_max_bottom_edge())
        return self.__break_on_trough(v, get_max_edge, condition)

    def is_slicable_left(self, v):
        condition = (lambda v1: v1.x > self.min_x)
        get_max_edge = (lambda v1: v1.get_edges_incident().get_max_left_edge())
        return self.__break_on_trough(v, get_max_edge, condition)

    def is_slicable_horizontally(self, v):
        return self.is_slicable_right(v) and self.is_slicable_left(v)

    def is_slicable_vertically(self, v):
        return self.is_slicable_top(v) and self.is_slicable_bottom(v)

    def get_slice_edges(self, v1, v2):
        if v1 < v2:
            start_v = v1
            end_v = v2
        else:
            start_v = v2
            end_v = v1

        if v1.x == v2.x:
            if v1.y < v2.y:
                return self.__get_top_slice(start_v, end_v)
            else:
                return self.__get_bottom_slice(end_v, start_v)
        else:
            if v1.x < v2.x:
                return self.__get_right_slice(start_v, end_v)
            else:
                return self.__get_left_slice(end_v, start_v)

    def __get_bottom_slice(self, start_v, end_v):
        condition = (lambda start_v, end_v: start_v.y > end_v.y)
        get_edge = (lambda v: v.bottom_edges.get_longest_edge())
        return self.__get_slice2(start_v, end_v, get_edge, condition)

    def __get_left_slice(self, start_v, end_v):
        condition = (lambda start_v, end_v: start_v.x > end_v.x)
        get_edge = (lambda v: v.left_edges.get_longest_edge())
        return self.__get_slice2(start_v, end_v, get_edge, condition)

    def __get_right_slice(self, start_v, end_v):
        condition = (lambda start_v, end_v: start_v.x < end_v.x)
        get_edge = (lambda v: v.right_edges.get_longest_edge())
        return self.__get_slice(start_v, end_v, get_edge, condition)

    def __get_top_slice(self, start_v, end_v):
        condition = (lambda start_v, end_v: start_v.y < end_v.y)
        get_edge = (lambda v: v.top_edges.get_longest_edge())
        return self.__get_slice(start_v, end_v, get_edge, condition)

    def __get_slice(self, start_v, end_v, get_edge, condition):
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

    def __get_slice2(self, start_v, end_v, get_edge, condition):
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

    def __break_on_trough(self, current_v, get_max_edge, condition):
        while condition(current_v):
            try:
                max_edge = get_max_edge(current_v)
            except ValueError:
                return False
            if max_edge.v1 != current_v:
                current_v = max_edge.v1
            else:
                current_v = max_edge.v2
        return True

    def __create_mesh_contour(self):
        contour_edges_list = np.empty(dtype=object, shape=0)
        v1 = self.vertex_list.get_vertex((0, 0))
        v2 = self.vertex_list.get_vertex((0, self.max_y))
        v3 = self.vertex_list.get_vertex((self.max_x, self.max_y))
        v4 = self.vertex_list.get_vertex((self.max_x, 0))
        contour_edges_list = np.append(contour_edges_list,
                                       self.get_slice_edges(v1, v2))
        contour_edges_list = np.append(contour_edges_list,
                                       self.get_slice_edges(v2, v3))
        contour_edges_list = np.append(contour_edges_list,
                                       self.get_slice_edges(v3, v4))
        contour_edges_list = np.append(contour_edges_list,
                                       self.get_slice_edges(v4, v1))
        return contour_edges_list
