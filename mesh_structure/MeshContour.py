# -*- coding: utf-8 -*-

import numpy as np
from mesh_structure.Direction import Direction

class MeshContour:

    def __init__(self, contour, mesh):
        self.mesh = mesh
        self.contour = contour
        self.__remove_useless_vertex()
        self.contour_index = self.__create_contour_index()
        self.max_x = self.__get_max_x()
        self.min_x = self.__get_min_x()
        self.max_y = self.__get_max_y()
        self.min_y = self.__get_min_y()        
        self.hash_key = self.__set_hash_key()
        
    def __getitem__(self, index):
        return self.contour[index % len(self.contour)]

    def __contains__(self, v):
        return (v.x, v.y) in self.contour_index
        
    def __len__(self):
        return len(self.contour)
        
    def __eq__(self, other):
        return True if self.contour_index == other.contour_index else False
        
    def __str__(self):
        to_str = ""
        for v in self.contour:
            to_str += str(v)
        return to_str

    def __remove_useless_vertex(self):
        vertex_to_remove = []
        for v in self.contour:
            index_v = np.where(self.contour == v)[0][0]
            prev_v = self[index_v - 1]
            next_v = self[index_v + 1]
            inside_directions =  self.__get_inside_directions(prev_v,v,next_v)
            if len(inside_directions) != 1:
                continue
            existing_directions = v.get_existing_edge_directions()
            possible_directions = list(set(inside_directions).intersection(existing_directions))
            if len(possible_directions) == 0:
                vertex_to_remove.append(v)
        for v in vertex_to_remove:
            index_v = np.where(self.contour == v)[0][0]
            self.contour = np.delete(self.contour, index_v)

    def __create_contour_index(self):
        contour_index = {}
        for v in self.contour:
            contour_index[(v.x, v.y)] = v
        return contour_index
        
    def __set_hash_key(self):
        min_el = min(self.contour)
        max_el = max(self.contour)
        c_x_sum = 0
        c_y_sum = 0
        for el in self.contour:
            c_x_sum += el.x
            c_y_sum += el.y
        hash_key = hash(((min_el.x, min_el.y), (c_x_sum, c_y_sum), (max_el.x, max_el.y)))  
        return hash_key

    def __get_max_x(self):
        max_x = self.contour[0].x
        for v in self.contour:
            if v.x > max_x:
                max_x = v.x
        return max_x

    def __get_min_x(self):
        min_x = self.contour[0].x
        for v in self.contour:
            if v.x < min_x:
                min_x = v.x
        return min_x

    def __get_max_y(self):
        max_y = self.contour[0].y
        for v in self.contour:
            if v.y > max_y:
                max_y = v.y
        return max_y

    def __get_min_y(self):
        min_y = self.contour[0].y
        for v in self.contour:
            if v.y < min_y:
                min_y = v.y
        return min_y
        
    def is_atomic_square(self):
        if len(self.contour) == 4:
            return True
        return False

    def get_possible_inside_directions(self, v):
        index_v = np.where(self.contour == v)[0][0]
        prev_v = self[index_v - 1]
        next_v = self[index_v + 1]
        inside_directions =  self.__get_inside_directions(prev_v, v, next_v)
        existing_directions = v.get_existing_edge_directions()
        possible_directions = list(set(inside_directions).intersection(existing_directions))
        return possible_directions
            
    def slice_contour(self, path):
        new_path = self.__add_missing_vertices(path)
        contour1, contour2 = self.__create_new_contours(new_path)
        return contour1, contour2

    def __add_missing_vertices(self, path):
        new_path = np.empty(dtype=object, shape=0)
        last_index = len(path) - 1
        curr_index = 1
        prev_v = path[curr_index - 1]
        curr_v = path[curr_index]
        new_path = np.append(new_path, prev_v)
        while True:
            prev_v = path[curr_index - 1]
            curr_v = path[curr_index]
            new_path = self.__add_vertices_beetween_two_vertex(new_path, prev_v, curr_v)
            new_path = np.append(new_path, curr_v)
            if curr_index == last_index:
                break
            else:
                curr_index = curr_index + 1
        return new_path 

    def __create_new_contours(self, path):
        start_v = path[0]
        end_v = path[len(path) - 1]
        index_start_v = np.where(self.contour == start_v)[0][0]
        index_end_v = np.where(self.contour == end_v)[0][0]
        countour_part_1 = self.contour[index_start_v + 1:index_end_v]
        new_contour_1 = np.append(countour_part_1, path[::-1])
        countour_part_2 = self.contour[:(index_start_v)]
        countour_part_3 = self.contour[(index_end_v + 1):]
        countour_part_2 = np.append(countour_part_2, path)
        new_contour_2 = np.append(countour_part_2, countour_part_3)  
        return MeshContour(new_contour_1, self.mesh), MeshContour(new_contour_2, self.mesh) 
                
    def __add_vertices_beetween_two_vertex(self, list, v1, v2):
        vector_direction = self.__get_vector_direction(v1, v2)
        if vector_direction == Direction.top:
            list = self.__add_vertices_from_top_directed_vector(list, v1, v2)
        if vector_direction == Direction.right:
            list = self.__add_vertices_from_right_directed_vector(list, v1, v2)
        if vector_direction == Direction.bottom:
            list = self.__add_vertices_from_bottom_directed_vector(list, v1, v2)
        if vector_direction == Direction.left:
            list = self.__add_vertices_from_left_directed_vector(list, v1, v2)
        return list

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

    def __add_vertices_from_top_directed_vector(self, list, v1, v2):
        # krawedz skierowana w gore, wiec v1 < v2
        vertices_beetween = self.mesh.sorted_vertex_lists.x_sorted[(v1.x, v1.y):(v2.x, v2.y)]
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                list = np.append(list,  vertex)
        return list

    def __add_vertices_from_right_directed_vector(self, list, v1, v2):
        # krawedz skierowana w prawo, wiec v1 < v2
        vertices_beetween = self.mesh.sorted_vertex_lists.y_sorted[(v1.y, v1.x):(v2.y, v2.x)]
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                list = np.append(list,  vertex)
        return list

    def __add_vertices_from_bottom_directed_vector(self, list, v1, v2):
        # krawedz skierowana w dół, wiec v1 > v2
        vertices_beetween = self.mesh.sorted_vertex_lists.x_sorted[(v2.x, v2.y):(v1.x, v1.y)]
        size_of_slice_vertices = list.size
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                list = np.insert(list, size_of_slice_vertices, vertex)
        return list

    def __add_vertices_from_left_directed_vector(self, list, v1, v2):
        # krawedz skierowana w lewo, wiec v1 > v2
        vertices_beetween = self.mesh.sorted_vertex_lists.y_sorted[(v2.y, v2.x):(v1.y, v1.x)]
        size_of_slice_vertices = list.size
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                list = np.insert(list, size_of_slice_vertices, vertex)
        return list

    def __get_inside_directions(self, prev_v, curr_v, next_v):
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
        