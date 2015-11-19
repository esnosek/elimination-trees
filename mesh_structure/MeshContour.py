# -*- coding: utf-8 -*-

import numpy as np
from mesh_structure.Direction import Direction


class MeshContour:

    def __init__(self, contour, mesh):
        self.mesh = mesh
        self.contour = contour
        self.slice_vertices_1 = np.empty(dtype=object, shape=0)
        self.slice_vertices_2 = np.empty(dtype=object, shape=0)

    def slice_contour(self, slice_vertices):
        last_index = slice_vertices.size - 1
        curr_index = 1
        while True:
            prev_v = slice_vertices[curr_index - 1]
            curr_v = slice_vertices[curr_index]
            self.slice_vertices_1 = np.append(self.slice_vertices_1, prev_v)
            self.slice_vertices_2 = np.append(self.slice_vertices_2, prev_v)
            self.__add_vertices_beetween_two_vertex(prev_v, curr_v)
            if curr_index == last_index:
                break
            else:
                next_v = slice_vertices[curr_index + 1]
                dir1 = self.__get_vector_direction(prev_v, curr_v)
                dir2 = self.__get_vector_direction(curr_v, next_v)
                self.__remove_useless_edges_depending_on_neihbors_direction(curr_v, dir1, dir2)
                curr_index = curr_index + 1
        self.slice_vertices_1 = np.append(self.slice_vertices_1, slice_vertices[last_index])
        self.slice_vertices_2 = np.append(self.slice_vertices_2, slice_vertices[last_index])
        print("pierwsza lista: ")
        for v in self.slice_vertices_1:
            print(v)
        print("druga lista: ")
        for v in self.slice_vertices_2:
            print(v)

    def __add_vertices_beetween_two_vertex(self, v1, v2):
        vector_direction = self.__get_vector_direction(v1, v2)
        if vector_direction == Direction.top:
            print("top")
            self.__add_vertices_from_top_directed_vector(v1, v2)
        if vector_direction == Direction.right:
            print("right")
            self.__add_vertices_from_right_directed_vector(v1, v2)
        if vector_direction == Direction.bottom:
            print("bottom")
            self.__add_vertices_from_bottom_directed_vector(v1, v2)
        if vector_direction == Direction.left:
            print("left")
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
        vertices_beetween = self.mesh.vertex_list.vertex_tree[(v1.x, v1.y):(v2.x, v2.y)]
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                if not vertex.left_edges.is_empty():
                    self.slice_vertices_1 = np.append(self.slice_vertices_1,  vertex)
                if not vertex.right_edges.is_empty():
                    self.slice_vertices_2 = np.append(self.slice_vertices_2, vertex)

    def __add_vertices_from_right_directed_vector(self, v1, v2):
        pass

    def __add_vertices_from_bottom_directed_vector(self, v1, v2):
        # krawedz skierowana w dół, wiec wiemy, że v1 > v2
        vertices_beetween = self.mesh.vertex_list.vertex_tree[(v2.x, v2.y):(v1.x, v1.y)]
        size_of_slice_vertices_1 = self.slice_vertices_1.size
        size_of_slice_vertices_2 = self.slice_vertices_2.size
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                if not vertex.left_edges.is_empty():
                    self.slice_vertices_1 = np.insert(self.slice_vertices_1, size_of_slice_vertices_1, vertex)
                if not vertex.right_edges.is_empty():
                    self.slice_vertices_2 = np.insert(self.slice_vertices_2, size_of_slice_vertices_2, vertex)

    def __add_vertices_from_left_directed_vector(self, v1, v2):
        pass

    def __remove_useless_edges_depending_on_neihbors_direction(v, dir1, dir2):
        if dir1 == Direction.top and dir2 == Direction.top:
            __remove_useless_edges_top_top()
        if dir1 == Direction.top and dir2 == Direction.right:
            __remove_useless_edges_top_right()
        if dir1 == Direction.top and dir2 == Direction.left:
            __remove_useless_edges_top_left()
        if dir1 == Direction.right and dir2 == Direction.top:
            __remove_useless_edges_right_top()
        if dir1 == Direction.right and dir2 == Direction.right:
            __remove_useless_edges_right_right()
        if dir1 == Direction.right and dir2 == Direction.bottom:
            __remove_useless_edges_right_bottom()
        if dir1 == Direction.bottom and dir2 == Direction.right:
            __remove_useless_edges_bottom_right()
        if dir1 == Direction.bottom and dir2 == Direction.bottom:
            __remove_useless_edges_bottom_bottom()
        if dir1 == Direction.bottom and dir2 == Direction.left:
            __remove_useless_edges_bottom_left()
        if dir1 == Direction.left and dir2 == Direction.top:
            __remove_useless_edges_left_top()
        if dir1 == Direction.left and dir2 == Direction.bottom:
            __remove_useless_edges_left_bottom()
        if dir1 == Direction.left and dir2 == Direction.left:
            __remove_useless_edges_left_left()

    def __remove_useless_edges_top_top():
        pass

    def __remove_useless_edges_top_right():
        pass

    def __remove_useless_edges_top_left():
        pass

    def __remove_useless_edges_right_top():
        pass

    def __remove_useless_edges_right_right():
        pass

    def __remove_useless_edges_right_bottom():
        pass

    def __remove_useless_edges_bottom_right():
        pass

    def __remove_useless_edges_bottom_bottom():
        pass

    def __remove_useless_edges_bottom_left():
        pass

    def __remove_useless_edges_left_top():
        pass

    def __remove_useless_edges_left_bottom():
        pass

    def __remove_useless_edges_left_left():
        pass
