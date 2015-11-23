# -*- coding: utf-8 -*-

import numpy as np
from mesh_structure.Direction import Direction
from copy import deepcopy

class MeshContour:

    def __init__(self, contour, mesh):
        self.mesh = mesh
        self.contour = contour
        self.slice_vertices_1 = np.empty(dtype=object, shape=0)
        self.slice_vertices_2 = np.empty(dtype=object, shape=0)

    def slice_contour(self, slice_vertices):
        last_index = slice_vertices.size - 1
        curr_index = 1
        prev_v = slice_vertices[curr_index - 1]
        self.slice_vertices_1 = np.append(self.slice_vertices_1, deepcopy(prev_v))
        self.slice_vertices_2 = np.append(self.slice_vertices_2, deepcopy(prev_v))
        # __remove_edges_from_first_vertex()
        while True:
            prev_v = slice_vertices[curr_index - 1]
            curr_v = slice_vertices[curr_index]
            self.__add_vertices_beetween_two_vertex(prev_v, curr_v)
            self.slice_vertices_1 = np.append(self.slice_vertices_1, deepcopy(curr_v))
            self.slice_vertices_2 = np.append(self.slice_vertices_2, deepcopy(curr_v))
            if curr_index == last_index:
                break
            else:
                next_v = slice_vertices[curr_index + 1]
                self.__remove_useless_edges_depending_on_neihbors_direction(prev_v, curr_v, next_v)
                curr_index = curr_index + 1

        # __remove_edges_from_last_vertex()

        print("pierwsza lista: ")
        for v in self.slice_vertices_1:
            print(v)
        print("druga lista: ")
        for v in self.slice_vertices_2:
            print(v)

    def __add_vertices_beetween_two_vertex(self, v1, v2):
        vector_direction = self.__get_vector_direction(v1, v2)
        if vector_direction == Direction.top:
            self.__add_vertices_from_top_directed_vector(v1, v2)
        if vector_direction == Direction.right:
            self.__add_vertices_from_right_directed_vector(v1, v2)
        if vector_direction == Direction.bottom:
            self.__add_vertices_from_bottom_directed_vector(v1, v2)
        if vector_direction == Direction.left:
            self.__add_vertices_from_left_directed_vector(v1, v2)

    def __get_vector_direction(self, v1, v2):
        if self.__is_direction_top(v1, v2):
            return Direction.top
        if self.__is_direction_right(v1, v2):
            return Direction.right
        if self.__is_direction_bottom(v1, v2):
            return Direction.bottom
        if self.__is_direction_left(v1, v2):
            return Direction.left

    def __is_direction_top(self, v1, v2):
        if v1.x == v2.x and v1.y < v2.y:
            return True
        return False

    def __is_direction_right(self, v1, v2):
        if v1.x < v2.x and v1.y == v2.y:
            return True
        return False

    def __is_direction_bottom(self, v1, v2):
        if v1.x == v2.x and v1.y > v2.y:
            return True
        return False

    def __is_direction_left(self, v1, v2):
        if v1.x > v2.x and v1.y == v2.y:
            return True
        return False

    def __add_vertices_from_top_directed_vector(self, v1, v2):
        # krawedz skierowana w gore, wiec v1 < v2
        vertices_beetween = self.mesh.vertex_list.vertex_tree[(v1.x, v1.y):(v2.x, v2.y)]
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                if not vertex.left_edges.is_empty():
                    self.slice_vertices_1 = np.append(self.slice_vertices_1,  vertex)
                if not vertex.right_edges.is_empty():
                    self.slice_vertices_2 = np.append(self.slice_vertices_2, vertex)

    def __add_vertices_from_right_directed_vector(self, v1, v2):
        # krawedz skierowana w prawo, wiec v1 < v2
        vertices_beetween = self.mesh.vertex_list.vertex_tree_y_sorted[(v1.y, v1.x):(v2.y, v2.x)]
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                if not vertex.top_edges.is_empty():
                    self.slice_vertices_1 = np.append(self.slice_vertices_1,  vertex)
                if not vertex.bottom_edges.is_empty():
                    self.slice_vertices_2 = np.append(self.slice_vertices_2, vertex)

    def __add_vertices_from_bottom_directed_vector(self, v1, v2):
        # krawedz skierowana w dół, wiec v1 > v2
        vertices_beetween = self.mesh.vertex_list.vertex_tree[(v2.x, v2.y):(v1.x, v1.y)]
        size_of_slice_vertices_1 = self.slice_vertices_1.size
        size_of_slice_vertices_2 = self.slice_vertices_2.size
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                if not vertex.right_edges.is_empty():
                    self.slice_vertices_1 = np.insert(self.slice_vertices_1, size_of_slice_vertices_1, vertex)
                if not vertex.left_edges.is_empty():
                    self.slice_vertices_2 = np.insert(self.slice_vertices_2, size_of_slice_vertices_2, vertex)

    def __add_vertices_from_left_directed_vector(self, v1, v2):
        # krawedz skierowana w lewo, wiec v1 > v2
        vertices_beetween = self.mesh.vertex_list.vertex_tree_y_sorted[(v2.y, v2.x):(v1.y, v1.x)]
        size_of_slice_vertices_1 = self.slice_vertices_1.size
        size_of_slice_vertices_2 = self.slice_vertices_2.size
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                if not vertex.bottom_edges.is_empty():
                    self.slice_vertices_1 = np.insert(self.slice_vertices_1, size_of_slice_vertices_1, vertex)
                if not vertex.top_edges.is_empty():
                    self.slice_vertices_2 = np.insert(self.slice_vertices_2, size_of_slice_vertices_2, vertex)

    def __remove_useless_edges_depending_on_neihbors_direction(self, prev_v, curr_v, next_v):
        dir1 = self.__get_vector_direction(prev_v, curr_v)
        dir2 = self.__get_vector_direction(curr_v, next_v)
        v_from_list_1 = self.slice_vertices_1[self.slice_vertices_1.size - 1]
        v_from_list_2 = self.slice_vertices_2[self.slice_vertices_2.size - 1]
        if dir1 == Direction.top and dir2 == Direction.top:
            self.__remove_edges_from_vertex_beetwen_top_and_top_vectors(v_from_list_1, v_from_list_2)
        if dir1 == Direction.top and dir2 == Direction.right:
            self.__remove_edges_from_vertex_beetwen_top_and_right_vectors(v_from_list_1, v_from_list_2)
        if dir1 == Direction.top and dir2 == Direction.left:
            self.__remove_edges_from_vertex_beetwen_top_and_left_vectors(v_from_list_1, v_from_list_2)
        if dir1 == Direction.right and dir2 == Direction.top:
            self.__remove_edges_from_vertex_beetwen_right_and_top_vectors(v_from_list_1, v_from_list_2)
        if dir1 == Direction.right and dir2 == Direction.right:
            self.__remove_edges_from_vertex_beetwen_right_and_right_vectors(v_from_list_1, v_from_list_2)
        if dir1 == Direction.right and dir2 == Direction.bottom:
            self.__remove_edges_from_vertex_beetwen_right_and_bottom_vectors(v_from_list_1, v_from_list_2)
        if dir1 == Direction.bottom and dir2 == Direction.right:
            self.__remove_edges_from_vertex_beetwen_bottom_and_right_vectors(v_from_list_1, v_from_list_2)
        if dir1 == Direction.bottom and dir2 == Direction.bottom:
            self.__remove_edges_from_vertex_beetwen_bottom_and_bottom_vectors(v_from_list_1, v_from_list_2)
        if dir1 == Direction.bottom and dir2 == Direction.left:
            self.__remove_edges_from_vertex_beetwen_bottom_and_left_vectors(v_from_list_1, v_from_list_2)
        if dir1 == Direction.left and dir2 == Direction.top:
            self.__remove_edges_from_vertex_beetwen_left_and_top_vectors(v_from_list_1, v_from_list_2)
        if dir1 == Direction.left and dir2 == Direction.bottom:
            self.__remove_edges_from_vertex_beetwen_left_and_bottom_vectors(v_from_list_1, v_from_list_2)
        if dir1 == Direction.left and dir2 == Direction.left:
            self.__remove_edges_from_vertex_beetwen_left_and_left_vectors(v_from_list_1, v_from_list_2)

    def __remove_edges_from_vertex_beetwen_top_and_top_vectors(self, v1, v2):
        v1.remove_right_edges()
        v2.remove_left_edges()

    def __remove_edges_from_vertex_beetwen_top_and_right_vectors(self, v1, v2):
        v2.remove_top_edges()
        v2.remove_left_edges()

    def __remove_edges_from_vertex_beetwen_top_and_left_vectors(self, v1, v2):
        v1.remove_top_edges()
        v1.remove_right_edges()

    def __remove_edges_from_vertex_beetwen_right_and_top_vectors(self, v1, v2):
        v1.remove_bottom_edges()
        v1.remove_right_edges()

    def __remove_edges_from_vertex_beetwen_right_and_right_vectors(self, v1, v2):
        v1.remove_bottom_edges()
        v2.remove_top_edges()

    def __remove_edges_from_vertex_beetwen_right_and_bottom_vectors(self, v1, v2):
        v2.remove_top_edges()
        v2.remove_right_edges()

    def __remove_edges_from_vertex_beetwen_bottom_and_right_vectors(self, v1, v2):
        v1.remove_bottom_edges()
        v1.remove_left_edges()

    def __remove_edges_from_vertex_beetwen_bottom_and_bottom_vectors(self, v1, v2):
        v1.remove_left_edges()
        v2.remove_right_edges()

    def __remove_edges_from_vertex_beetwen_bottom_and_left_vectors(self, v1, v2):
        v2.remove_bottom_edges()
        v2.remove_right_edges()

    def __remove_edges_from_vertex_beetwen_left_and_top_vectors(self, v1, v2):
        v2.remove_bottom_edges()
        v2.remove_left_edges()

    def __remove_edges_from_vertex_beetwen_left_and_bottom_vectors(self, v1, v2):
        v1.remove_top_edges()
        v1.remove_left_edges()

    def __remove_edges_from_vertex_beetwen_left_and_left_vectors(self, v1, v2):
        v1.remove_top_edges()
        v2.remove_bottom_edges()
