# -*- coding: utf-8 -*-
from mesh_structure.Direction import Direction, VectorDirection
from mesh_structure.MeshContour import MeshContour
from copy import copy
import numpy as np


class PathsFinder:


    def __init__(self, contour):
        self.possible_paths = []
        self.end_vertices_list = []
        self.contour = contour

    def get_possible_paths(self):
        for index_start_v in range(len(self.contour)):
            for index_end_v in range(index_start_v + 1, len(self.contour)):
                start_v = self.contour[index_start_v]
                end_v = self.contour[index_end_v]
                self.end_vertices_list = [end_v]
                possible_directions = self.contour.get_possible_inside_directions(start_v)
                if len(possible_directions) > 0:
                    for direction in possible_directions:
                        travel_vertex = self.travel_to_next_vertex(start_v, direction)
                        used_cross_vertices = [start_v]
                        self.find_path(travel_vertex, direction.get_oposite_direction(), used_cross_vertices)
        return self.possible_paths
    
    
    def find_path(self, v, arrival_direction, used_cross_vertices):
        if v in self.end_vertices_list:
            used_cross_vertices = self.copy_used_vertices_list_and_append(v, used_cross_vertices)
            self.possible_paths.append(used_cross_vertices)    
            return True
            
        elif v in used_cross_vertices or v in self.contour:
            return False
    
        elif self.is_there_any_way(v, arrival_direction):
            possible_travel_directions = self.get_possible_travel_directions(v, arrival_direction)     
            used_cross_vertices = self.copy_used_vertices_list_and_append(v, used_cross_vertices)
            is_curr_v_useful = False
            for direction in possible_travel_directions:
                travel_vertex = self.travel_to_next_vertex(v, direction)
                if self.find_path(travel_vertex, direction.get_oposite_direction(), used_cross_vertices):
                    is_curr_v_useful = True
            return is_curr_v_useful
        else:
            return False
    
    
    def copy_used_vertices_list_and_append(self, vertex, used_vertices):
        used_vertices_copy = copy(used_vertices)
        used_vertices_copy.append(vertex)
        return used_vertices_copy
    
    
    def travel_to_next_vertex(self, v, direction):
        travel_edge = v.get_longest_edge_in_direction(direction)
        travel_vertex = travel_edge.get_second_vertex_from_edge(v)
        return travel_vertex
    
    
    def get_possible_travel_directions(self, v, arrival_direction):
        possible_directions = list(v.get_existing_edge_directions())
        if arrival_direction in [Direction.bottom, Direction.top]:
            if (Direction.left in possible_directions) and (Direction.right not in possible_directions):
                possible_directions.remove(Direction.left)
            elif (Direction.left not in possible_directions) and (Direction.right in possible_directions):
                possible_directions.remove(Direction.right)
        elif arrival_direction in [Direction.left, Direction.right]:
            if (Direction.top in possible_directions) and (Direction.bottom not in possible_directions):
                possible_directions.remove(Direction.top)
            elif (Direction.top not in possible_directions) and (Direction.bottom in possible_directions):         
                possible_directions.remove(Direction.bottom)
        if arrival_direction in possible_directions:
            possible_directions.remove(arrival_direction)
        return possible_directions
    
    
    def is_there_any_way(self, v, arrival_direction):
        if v in self.contour:
            return False
        elif arrival_direction.get_oposite_direction() in v.get_existing_edge_directions():
            return True
        else:
            return False

class ContourSlice:


    def __init__(self, contour, path):
        self.contour = contour
        self.path = self.__add_missing_vertices(path)

    def slice_contour(self):
        contour1, contour2 = self.__create_new_contours()
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

    def __create_new_contours(self):
        start_v = self.path[0]
        end_v = self.path[len(self.path) - 1]
        index_start_v = np.where(self.contour.contour == start_v)[0][0]
        index_end_v = np.where(self.contour.contour == end_v)[0][0]
        countour_part_1 = self.contour.contour[index_start_v + 1:index_end_v]
        new_contour_1 = np.append(countour_part_1, self.path[::-1])
        countour_part_2 = self.contour.contour[:(index_start_v)]
        countour_part_3 = self.contour.contour[(index_end_v + 1):]
        countour_part_2 = np.append(countour_part_2, self.path)
        new_contour_2 = np.append(countour_part_2, countour_part_3)  
        return MeshContour(new_contour_1, self.contour.mesh), MeshContour(new_contour_2, self.contour.mesh) 
                
    def __add_vertices_beetween_two_vertex(self, list, v1, v2):
        vector_direction = VectorDirection().get_vector_direction(v1, v2)
        if vector_direction == Direction.top:
            list = self.__add_vertices_from_top_directed_vector(list, v1, v2)
        if vector_direction == Direction.right:
            list = self.__add_vertices_from_right_directed_vector(list, v1, v2)
        if vector_direction == Direction.bottom:
            list = self.__add_vertices_from_bottom_directed_vector(list, v1, v2)
        if vector_direction == Direction.left:
            list = self.__add_vertices_from_left_directed_vector(list, v1, v2)
        return list
        

    def __add_vertices_from_top_directed_vector(self, list, v1, v2):
        # krawedz skierowana w gore, wiec v1 < v
        vertices_beetween = self.contour.mesh.sorted_vertex_lists.get_vertices_beetween_from_x_sorted(v1, v2)
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                list = np.append(list,  vertex)
        return list

    def __add_vertices_from_right_directed_vector(self, list, v1, v2):
        # krawedz skierowana w prawo, wiec v1 < v2
        vertices_beetween = self.contour.mesh.sorted_vertex_lists.get_vertices_beetween_from_y_sorted(v1, v2)
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                list = np.append(list,  vertex)
        return list

    def __add_vertices_from_bottom_directed_vector(self, list, v1, v2):
        # krawedz skierowana w dół, wiec v1 > v2
        vertices_beetween = self.contour.mesh.sorted_vertex_lists.get_vertices_beetween_from_x_sorted(v2, v1)
        size_of_slice_vertices = list.size
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                list = np.insert(list, size_of_slice_vertices, vertex)
        return list

    def __add_vertices_from_left_directed_vector(self, list, v1, v2):
        # krawedz skierowana w lewo, wiec v1 > v2
        vertices_beetween = self.contour.mesh.sorted_vertex_lists.get_vertices_beetween_from_y_sorted(v2, v1)
        size_of_slice_vertices = list.size
        for key in vertices_beetween:
            vertex = vertices_beetween[key]
            if vertex != v1 and vertex != v2:
                list = np.insert(list, size_of_slice_vertices, vertex)
        return list