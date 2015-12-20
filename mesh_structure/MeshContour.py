# -*- coding: utf-8 -*-

import numpy as np
from mesh_structure.Direction import Direction
import tree_view.meshDrawer as md
from numpy import mean

class MeshContour:

    def __init__(self, contour, mesh):
        self.mesh = mesh
        self.contour = contour
        self.contour_index = self.__create_contour_index()
        self.slice_vertices = np.empty(dtype=object, shape=0)

    def __create_contour_index(self):
        contour_index = {}
        for v in self.contour:
            contour_index[(v.x, v.y)] = v
        return contour_index

    def __getitem__(self,index):
        if index == len(self.contour):
            index = 0
        elif index == -1:
            index = len(self.contour) - 1
        return self.contour[index]

    def __len__(self):
        return len(self.contour)
        
    def __eq__(self, other):   
        return True if self.contour_index == other.contour_index else False
        
    def __str__(self):
        to_str = ""
        for v in self.contour:
            to_str += str(v)
        
        return to_str
        
    def get_center(self):
        return tuple(map(mean, zip(*self.contour)))
        
    def slice_contour(self, slice_vertices):
        self.slice_vertices = np.empty(dtype=object, shape=0)
        last_index = len(slice_vertices) - 1
        curr_index = 1
        prev_v = slice_vertices[curr_index - 1]
        curr_v = slice_vertices[curr_index]
        self.slice_vertices = np.append(self.slice_vertices, prev_v)
        while True:
            prev_v = slice_vertices[curr_index - 1]
            curr_v = slice_vertices[curr_index]
            self.__add_vertices_beetween_two_vertex(prev_v, curr_v)
            self.slice_vertices = np.append(self.slice_vertices, curr_v)
            if curr_index == last_index:
                break
            else:
                curr_index = curr_index + 1
            
        contour1, contour2 = self.__slice_contour()
        return MeshContour(contour1, self.mesh), MeshContour(contour2, self.mesh) 
                
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
                self.slice_vertices = np.append(self.slice_vertices,  vertex)

    def __add_vertices_from_right_directed_vector(self, v1, v2):
        # krawedz skierowana w prawo, wiec v1 < v2
        vertices_beetween = self.mesh.vertex_list.vertex_tree_y_sorted[(v1.y, v1.x):(v2.y, v2.x)]
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                self.slice_vertices = np.append(self.slice_vertices,  vertex)

    def __add_vertices_from_bottom_directed_vector(self, v1, v2):
        # krawedz skierowana w dół, wiec v1 > v2
        vertices_beetween = self.mesh.vertex_list.vertex_tree[(v2.x, v2.y):(v1.x, v1.y)]
        size_of_slice_vertices = self.slice_vertices.size
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                self.slice_vertices = np.insert(self.slice_vertices, size_of_slice_vertices, vertex)

    def __add_vertices_from_left_directed_vector(self, v1, v2):
        # krawedz skierowana w lewo, wiec v1 > v2
        vertices_beetween = self.mesh.vertex_list.vertex_tree_y_sorted[(v2.y, v2.x):(v1.y, v1.x)]
        size_of_slice_vertices = self.slice_vertices.size
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                self.slice_vertices = np.insert(self.slice_vertices, size_of_slice_vertices, vertex)

    def get_inside_directions(self, prev_v, curr_v, next_v):
        dir1 = self.__get_vector_direction(prev_v, curr_v)
        dir2 = self.__get_vector_direction(curr_v, next_v)
        if dir1 == Direction.top and dir2 == Direction.top:
            return self.__get_inside_directions_from_vertex_beetwen_top_and_top_vectors()
        if dir1 == Direction.top and dir2 == Direction.right:
            return self.__get_inside_directions_from_vertex_beetwen_top_and_right_vectors()
        if dir1 == Direction.top and dir2 == Direction.left:
            return self.__get_inside_directions_from_vertex_beetwen_top_and_left_vectors()
        if dir1 == Direction.right and dir2 == Direction.top:
            return self.__get_inside_directions_from_vertex_beetwen_right_and_top_vectors()
        if dir1 == Direction.right and dir2 == Direction.right:
            return self.__get_inside_directions_from_vertex_beetwen_right_and_right_vectors()
        if dir1 == Direction.right and dir2 == Direction.bottom:
            return self.__get_inside_directions_from_vertex_beetwen_right_and_bottom_vectors()
        if dir1 == Direction.bottom and dir2 == Direction.right:
            return self.__get_inside_directions_from_vertex_beetwen_bottom_and_right_vectors()
        if dir1 == Direction.bottom and dir2 == Direction.bottom:
            return self.__get_inside_directions_from_vertex_beetwen_bottom_and_bottom_vectors()
        if dir1 == Direction.bottom and dir2 == Direction.left:
            return self.__get_inside_directions_from_vertex_beetwen_bottom_and_left_vectors()
        if dir1 == Direction.left and dir2 == Direction.top:
            return self.__get_inside_directions_from_vertex_beetwen_left_and_top_vectors()
        if dir1 == Direction.left and dir2 == Direction.bottom:
            return self.__get_inside_directions_from_vertex_beetwen_left_and_bottom_vectors()
        if dir1 == Direction.left and dir2 == Direction.left:
            return self.__get_inside_directions_from_vertex_beetwen_left_and_left_vectors()

    def __get_inside_directions_from_vertex_beetwen_top_and_top_vectors(self):
        return [Direction.right]

    def __get_inside_directions_from_vertex_beetwen_top_and_right_vectors(self):
        return []

    def __get_inside_directions_from_vertex_beetwen_top_and_left_vectors(self):
        return [Direction.top, Direction.right]

    def __get_inside_directions_from_vertex_beetwen_right_and_top_vectors(self):
        return [Direction.bottom, Direction.right]

    def __get_inside_directions_from_vertex_beetwen_right_and_right_vectors(self):
        return [Direction.bottom]

    def __get_inside_directions_from_vertex_beetwen_right_and_bottom_vectors(self):
        return []

    def __get_inside_directions_from_vertex_beetwen_bottom_and_right_vectors(self):
        return [Direction.bottom, Direction.left]

    def __get_inside_directions_from_vertex_beetwen_bottom_and_bottom_vectors(self):
        return [Direction.left]

    def __get_inside_directions_from_vertex_beetwen_bottom_and_left_vectors(self):
        return []

    def __get_inside_directions_from_vertex_beetwen_left_and_top_vectors(self):
        return []

    def __get_inside_directions_from_vertex_beetwen_left_and_bottom_vectors(self):
        return [Direction.top, Direction.left]

    def __get_inside_directions_from_vertex_beetwen_left_and_left_vectors(self):
        return [Direction.top]
    
    def __slice_contour(self):
        start_v = self.slice_vertices[0]
        end_v = self.slice_vertices[self.slice_vertices.size - 1]
        index_start_v = np.where(self.contour == start_v)[0][0]
        index_end_v = np.where(self.contour == end_v)[0][0]
        countour_part_1 = self.contour[index_start_v + 1:index_end_v]
        new_contour_1 = np.append(countour_part_1, self.slice_vertices[::-1])
        countour_part_2 = self.contour[:(index_start_v)]
        countour_part_3 = self.contour[(index_end_v + 1):]
        countour_part_2 = np.append(countour_part_2, self.slice_vertices)
        new_contour_2 = np.append(countour_part_2, countour_part_3)
        return new_contour_1, new_contour_2      
        
        
        
        
        
        
        
        