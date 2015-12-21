# -*- coding: utf-8 -*-

import numpy as np
from mesh_structure.Direction import Direction
import tree_view.meshDrawer as md
from numpy import mean
import sys

licznik_chujowek = 1

class MeshContour:

    def __init__(self, contour, mesh):
        if type(self.__is_atomic_square(contour)) is int:
            print("kontur")
            print([str(v) for v in contour])        
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            sys.exit()
        self.mesh = mesh
        self.contour = contour
        self.contour_index = self.__create_contour_index()
        self.center = tuple(np.average(np.array(list(self.contour_index.keys())).astype(int), axis=0))
        #print(type(self.center))

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
        new_slice_vertices = np.empty(dtype=object, shape=0)
        last_index = len(slice_vertices) - 1
        curr_index = 1
        prev_v = slice_vertices[curr_index - 1]
        curr_v = slice_vertices[curr_index]
        new_slice_vertices = np.append(new_slice_vertices, prev_v)
        while True:
            prev_v = slice_vertices[curr_index - 1]
            curr_v = slice_vertices[curr_index]
            new_slice_vertices = self.__add_vertices_beetween_two_vertex(new_slice_vertices, prev_v, curr_v)
            new_slice_vertices = np.append(new_slice_vertices, curr_v)
            if curr_index == last_index:
                break
            else:
                curr_index = curr_index + 1
        
        contour1, contour2 = self.__slice_contour(new_slice_vertices)
        return MeshContour(contour1, self.mesh), MeshContour(contour2, self.mesh) 
                
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
        vertices_beetween = self.mesh.vertex_list.vertex_tree[(v1.x, v1.y):(v2.x, v2.y)]
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                list = np.append(list,  vertex)
        return list

    def __add_vertices_from_right_directed_vector(self, list, v1, v2):
        # krawedz skierowana w prawo, wiec v1 < v2
        vertices_beetween = self.mesh.vertex_list.vertex_tree_y_sorted[(v1.y, v1.x):(v2.y, v2.x)]
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                list = np.append(list,  vertex)
        return list

    def __add_vertices_from_bottom_directed_vector(self, list, v1, v2):
        # krawedz skierowana w dół, wiec v1 > v2
        vertices_beetween = self.mesh.vertex_list.vertex_tree[(v2.x, v2.y):(v1.x, v1.y)]
        size_of_slice_vertices = list.size
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                list = np.insert(list, size_of_slice_vertices, vertex)
        return list

    def __add_vertices_from_left_directed_vector(self, list, v1, v2):
        # krawedz skierowana w lewo, wiec v1 > v2
        vertices_beetween = self.mesh.vertex_list.vertex_tree_y_sorted[(v2.y, v2.x):(v1.y, v1.x)]
        size_of_slice_vertices = list.size
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                list = np.insert(list, size_of_slice_vertices, vertex)
        return list

    def get_inside_directions(self, prev_v, curr_v, next_v):
        global licznik_chujowek
        
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
        
        return None
        
        licznik_chujowek += 1
        if licznik_chujowek > 20:
            sys.exit()

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
    
    def __slice_contour(self, new_slice_vertices):
        start_v = new_slice_vertices[0]
        end_v = new_slice_vertices[len(new_slice_vertices) - 1]
        index_start_v = np.where(self.contour == start_v)[0][0]
        index_end_v = np.where(self.contour == end_v)[0][0]
        countour_part_1 = self.contour[index_start_v + 1:index_end_v]
        new_contour_1 = np.append(countour_part_1, new_slice_vertices[::-1])
        countour_part_2 = self.contour[:(index_start_v)]
        countour_part_3 = self.contour[(index_end_v + 1):]
        countour_part_2 = np.append(countour_part_2, new_slice_vertices)
        new_contour_2 = np.append(countour_part_2, countour_part_3)

        first_vertex_1 = new_contour_1[0]        
        last_vertex_1 = new_contour_1[len(new_contour_1) - 1]
        first_vertex_2 = new_contour_2[0]        
        last_vertex_2 = new_contour_2[len(new_contour_2) - 1]
        new_contour_1 = self.__add_vertices_beetween_two_vertex(new_contour_1, last_vertex_1, first_vertex_1)
        new_contour_2 = self.__add_vertices_beetween_two_vertex(new_contour_2, last_vertex_2, first_vertex_2)

        
        if type(self.__is_atomic_square(new_contour_1)) is int:
            print("kontur")
            print([str(v) for v in self.contour])        
            print("ciecie")
            print([str(v) for v in new_slice_vertices])
            print("kontur1")
            print([str(v) for v in new_contour_1])
            print("kontur2")
            print([str(v) for v in new_contour_2])
            print("----------------------------------------------")
        if type(self.__is_atomic_square(new_contour_2)) is int:
            print("kontur")
            print([str(v) for v in self.contour])        
            print("ciecie")
            print([str(v) for v in new_slice_vertices])
            print("kontur1")
            print([str(v) for v in new_contour_1])
            print("kontur2")
            print([str(v) for v in new_contour_2])
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        if type(self.__is_atomic_square(new_contour_1)) is int:
            sys.exit()
        if type(self.__is_atomic_square(new_contour_2)) is int:
            sys.exit()
            
        return new_contour_1, new_contour_2      
 
    def __is_atomic_square(self, parent_contour):
        for v in parent_contour:
            index_curr_v = np.where(parent_contour == v)[0][0]
            index_prev_v = index_curr_v - 1
            index_next_v = index_curr_v + 1
            if index_next_v > len(parent_contour) - 1:
                index_next_v = 0
            prev_v = parent_contour[index_prev_v]
            next_v = parent_contour[index_next_v]
            inside_directions = self.get_inside_directions(prev_v, v, next_v)
            if not type(inside_directions) is list:
                return 1
            existing_directions = v.get_existing_edge_directions()
            possible_directions = list(set(inside_directions).intersection(existing_directions))
            if len(possible_directions) > 0:
                return False
        return True
       
        
        
        
        
        
        
        