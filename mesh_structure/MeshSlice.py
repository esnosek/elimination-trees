# -*- coding: utf-8 -*-

import numpy as np


class MeshSlice:

    def __init__(self, contour):
        self.contour = contour
        self.visited_list = np.empty(dtype=object, shape=0)
        self.visited_edge = np.empty(dtype=object, shape=0)
        self.max_x = self.get_max_x()
        self.max_y = self.get_max_y()
        self.min_x = self.get_min_x()
        self.min_y = self.get_min_y()

    def get_max_x(self, contour):
        max = -1
        for edge in contour:
            if edge.v1.x > max:
                max = edge.v1.x
            if edge.v2.x > max:
                max = edge.v2.x
        return max
        
    def get_max_y(self, contour):
        max = -1
        for edge in contour:
            if edge.v1.y > max:
                max = edge.v1.y
            if edge.v2.y > max:
                max = edge.v2.y
        return max

    def get_min_x(self, contour):
        min = 100000
        for edge in contour:
            if edge.v1.x < min:
                min = edge.v1.x
            if edge.v2.x < min:
                max = edge.v2.x
        return min   
        
    def get_min_y(self, contour):
        min = 100000
        for edge in contour:
            if edge.v1.y < min:
                min = edge.v1.y
            if edge.v2.y < min:
                max = edge.v2.y
        return min  

    def slice(self, contour):
        if(contour.size > 4):
            slice_edges = np.empty(dtype=object, shape=0)
            for edge in contour:
                v2 = self.is_slicable_top(edge.v1, contour)
                if not v2:
                    v2 = self.is_slicable_bottom(edge.v1, contour)
                if not v2:
                    v2 = self.is_slicable_left(edge.v1, contour)
                if not v2:
                    v2 = self.is_slicable_right(edge.v1, contour)
                if not v2:
                    slice_edges = self.get_slice_edges(v2, edge.v1)
                if slice_edges:
                    list1, list2 = self.slice_mesh(v2, edge.v1, slice_edges)
                    slice(list1)
                    slice(list2)
            

    def test(self):
        self.slice(self.contour)

    def slice_mesh(self, start_v, end_v, slice_edges):

        idx_e1 = np.where(self.contour==start_v)
        idx_e2 = np.where(self.contour==end_v)

        edge_list_1 = self.contour[idx_e1:idx_e2]
        edge_list_1 = np.append(edge_list_1, slice_edges[::-1])

        edge_list_2 = self.contour[:idx_e1]
        edge_list_3 = self.contour[idx_e2:]
        edge_list_2 = np.append(edge_list_2, slice_edges)
        edge_list_2 = np.append(edge_list_2, edge_list_3)

        return edge_list_1, edge_list_2

    def is_slicable_top(self, v, contour):
        condition = (lambda v1: v1.y < self.get_max_y(contour))
        get_max_edge = (lambda v1: v1.get_edges_incident().get_max_top_edge())
        return self.__break_on_trough(v, get_max_edge, condition)

    def is_slicable_right(self, v, contour):
        condition = (lambda v1: v1.x < self.get_max_x(contour))
        get_max_edge = (lambda v1: v1.get_edges_incident().get_max_right_edge())
        return self.__break_on_trough(v, get_max_edge, condition)

    def is_slicable_bottom(self, v, contour):
        condition = (lambda v1: v1.y > self.get_min_y(contour))
        get_max_edge = (lambda v1: v1.get_edges_incident().get_max_bottom_edge())
        return self.__break_on_trough(v, get_max_edge, condition)

    def is_slicable_left(self, v, contour):
        condition = (lambda v1: v1.x > self.get_min_x(contour))
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
        get_edge = (lambda v: v.get_edges_incident().get_max_bottom_edge())
        return self.__get_slice2(start_v, end_v, get_edge, condition)

    def __get_left_slice(self, start_v, end_v):
        condition = (lambda start_v, end_v: start_v.x > end_v.x)
        get_edge = (lambda v: v.get_edges_incident().get_max_left_edge())
        return self.__get_slice2(start_v, end_v, get_edge, condition)

    def __get_right_slice(self, start_v, end_v):
        condition = (lambda start_v, end_v: start_v.x < end_v.x)
        get_edge = (lambda v: v.get_edges_incident().get_max_right_edge())
        return self.__get_slice(start_v, end_v, get_edge, condition)

    def __get_top_slice(self, start_v, end_v):
        condition = (lambda start_v, end_v: start_v.y < end_v.y)
        get_edge = (lambda v: v.get_edges_incident().get_max_top_edge())
        return self.__get_slice(start_v, end_v, get_edge, condition)

    def __get_slice(self, start_v, end_v, get_edge, condition):
        slice_edges = np.empty(dtype=object, shape=0)
        edge = get_edge(start_v)
        slice_edges = np.append(slice_edges, edge)
        fl = True
        while condition(edge.v1, end_v) and fl:
            if condition(edge.v2, end_v):
                edge = get_edge(edge.v2)
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
                edge = get_edge(edge.v1)
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
        return current_v