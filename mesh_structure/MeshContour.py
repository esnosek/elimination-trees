# -*- coding: utf-8 -*-

import numpy as np
from mesh_structure.Direction import Direction, VectorDirection

class MeshContour:

    def __init__(self, contour):
        self.contour = contour
        self.contour_index = None
        self.hash_key = None
        self.__remove_useless_vertex()
        self.__create_contour_index()  
        self.__set_hash_key()
        
    def __getitem__(self, index):
        return self.contour[index % len(self.contour)]

    def __contains__(self, v):
        key = (v.x, v.y)
        return key in self.contour_index
        
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
            index_v = self.get_index_of(v)
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
            index_v = self.get_index_of(v)
            self.contour = np.delete(self.contour, index_v)

    def __create_contour_index(self):
        contour_index = {}
        for v in self.contour:
            contour_index[(v.x, v.y)] = v
        self.contour_index = contour_index
        
    def __set_hash_key(self):
        min_el = min(self.contour)
        max_el = max(self.contour)
        c_x_sum = 0
        c_y_sum = 0
        for el in self.contour:
            c_x_sum += el.x
            c_y_sum += el.y
        self.hash_key = hash(((min_el.x, min_el.y), (c_x_sum, c_y_sum), (max_el.x, max_el.y)))  

    def is_atomic_square(self):
        if len(self.contour) == 4:
            return True
        return False

    def get_index_of(self, v):
        return np.where(self.contour == v)[0][0]        
  
    def get_vertices_beetween(self, index_1, index_2):
        return self.contour[index_1:index_2]
        
    def get_possible_inside_directions(self, v):
        index_v = np.where(self.contour == v)[0][0]
        prev_v = self[index_v - 1]
        next_v = self[index_v + 1]
        inside_directions =  self.__get_inside_directions(prev_v, v, next_v)
        existing_directions = v.get_existing_edge_directions()
        possible_directions = list(set(inside_directions).intersection(existing_directions))
        return possible_directions
            

    def __get_inside_directions(self, prev_v, curr_v, next_v):
        dir1 = VectorDirection().get_vector_direction(prev_v, curr_v)
        dir2 = VectorDirection().get_vector_direction(curr_v, next_v)
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
        