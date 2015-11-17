# -*- coding: utf-8 -*-

import numpy as np
from mesh_structure.Direction import Direction


class MeshContour:

    def __init__(self, contour):
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
            __add_vertices_beetween_two_vertex(prev_v, curr_v)
            if curr_index == last_index:
                break
            else:
                next_v = slice_vertices[curr_index + 1]
                dir1 = __get_vector_direction(prev_v, curr_v)
                dir2 = __get_vector_direction(curr_v, next_v)
                __remove_useless_edges_depending_on_neihbors_direction(curr_v,
                                                                       dir1,
                                                                       dir2)
                curr_index = curr_index + 1

    def __add_vertices_beetween_two_vertex(self, v1, v2):
        vector_direction = __get_vector_direction(v1, v2)
        if vector_direction == Direction.top:
            __add_vertices_from_top_directed_vector(v1, v2)
        if vector_direction == Direction.right:
            __add_vertices_from_right_directed_vector(v1, v2)
        if vector_direction == Direction.bottom:
            __add_vertices_from_bottom_directed_vector(v1, v2)
        if vector_direction == Direction.left:
            __add_vertices_from_left_directed_vector(v1, v2)

    def __get_vector_direction(self, v1, v2):
        if __is_direction_top(v1, v2):
            return Direction.top
        if __is_direction_right(v1, v2):
            return Direction.right
        if __is_direction_bottom(v1, v2):
            return Direction.bottom
        if __is_direction_left(v1, v2):
            return Direction.left

    def __is_direction_top(self, v1, v2):

    def __is_direction_right(self, v1, v2):

    def __is_direction_bottom(self, v1, v2):

    def __is_direction_left(self, v1, v2):

    def __add_vertices_from_top_directed_vector(self, v1, v2):

    def __add_vertices_from_right_directed_vector(self, v1, v2):

    def __add_vertices_from_bottom_directed_vector(self, v1, v2):

    def __add_vertices_from_left_directed_vector(self, v1, v2)

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

    def __remove_useless_edges_top_right():

    def __remove_useless_edges_top_left():

    def __remove_useless_edges_right_top():

    def __remove_useless_edges_right_right():

    def __remove_useless_edges_right_bottom():

    def __remove_useless_edges_bottom_right():

    def __remove_useless_edges_bottom_bottom():

    def __remove_useless_edges_bottom_left():

    def __remove_useless_edges_left_top():

    def __remove_useless_edges_left_bottom():

    def __remove_useless_edges_left_left():
