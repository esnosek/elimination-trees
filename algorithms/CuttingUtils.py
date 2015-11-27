# -*- coding: utf-8 -*-
from mesh_structure.Direction import Direction
from mesh_structure.Vertex import Vertex
from mesh_structure.Edge import Edge
from test import create_mesh
from copy import copy
import unittest
# wesja z longest

def get_possible_cuts(contour):
    possible_paths = []
    for point_a_idx in range(len(contour.contour)):
        for point_b_idx in range(point_a_idx + 1, len(contour.contour)):
            point_a = contour.contour[point_a_idx]
            point_b = contour.contour[point_b_idx]
            
            print(point_a)
            print(point_a.bottom_edges.edge_incident)            
            
            inside_direction = None
            if Direction.left and Direction.right in point_a.get_existing_edge_directions():
                if Direction.bottom in point_a.get_existing_edge_directions():
                    inside_direction = Direction.bottom
                elif Direction.top in point_a.get_existing_edge_directions():
                    inside_direction = Direction.top
            elif Direction.top and Direction.bottom in point_a.get_existing_edge_directions():
                if Direction.left in point_a.get_existing_edge_directions:
                    inside_direction = Direction.left
                elif Direction.right in point_a.get_existing_edge_directions():
                    inside_direction = Direction.right
            
            if inside_direction:
                used_cross_points = []
                find_path(point_a, [point_b], inside_direction, used_cross_points, possible_paths)
                
        return possible_paths


def find_path(current_point, end_point_list, arrival_direction, used_cross_points, possible_paths):

    if current_point in end_point_list:
        
        used_cross_points.append(current_point)
        possible_paths.append(used_cross_points)
        return True
    elif current_point in used_cross_points or current_point.is_border_vertex:

        return False

    elif is_there_any_way(current_point, arrival_direction): 
        possible_travel_directions = get_possible_directions(current_point, arrival_direction)
        if len(possible_travel_directions) > 1:
            used_cross_points = copy(used_cross_points)
            used_cross_points.append(current_point)
            
        is_current_useful = False

        for direction in possible_travel_directions:
            travel_edge = current_point.get_longest_edge_in_direction(direction) # longest
            travel_point = get_second_edge_point(current_point, travel_edge)

            if find_path(travel_point, end_point_list, get_oposite_direction(direction), used_cross_points.copy(), possible_paths):
                is_current_useful = True
     
        return is_current_useful

    else:
        return False

def get_second_edge_point(first_point, edge):
    if edge.v1 == first_point:
        return edge.v2
    else:
        return edge.v1

def get_oposite_direction(direction):
    if direction == Direction.bottom:
        return Direction.top
    elif direction == Direction.left:
        return Direction.right
    elif direction == Direction.top:
        return Direction.bottom
    else:
        return Direction.left 

def get_possible_directions(point, arrival_direction):
    
    possible_directions = point.get_existing_edge_directions()
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

def is_there_any_way(point, arrival_direction):
    if point.is_border_vertex:
         return False
    if get_oposite_direction(arrival_direction) in point.get_existing_edge_directions():
         return True


class CuttingTests(unittest.TestCase):

    def test_creating_mesh(self):
        pass
        test_vertex_a = Vertex(4, 4)
        test_vertex_b = Vertex(4, 4)
        self.assertEqual(test_vertex_a, test_vertex_b)
        
    def test_cut(self):
        return
        mesh = create_mesh()
        test_vertex_a = mesh.vertex_list.get_vertex((0, 2))
        test_vertex_b = mesh.vertex_list.get_vertex((0, 4))
        used_cross_points = []
        end_point_list = [test_vertex_b]
        possible_paths = []
        find_path(test_vertex_a, end_point_list, Direction.bottom, used_cross_points, possible_paths)
        for p in possible_paths:  
            print([str(v) for v in p])
            
    def test_all_possible_cuts(self):
        
        mesh = create_mesh()
        #print(len(mesh.contour.contour))
        #print([str(e) for e in mesh.contour.contour])
        possible_paths = get_possible_cuts(mesh.contour)
        for p in possible_paths:  
            print([str(v) for v in p])

if __name__ == '__main__':

    unittest.main()
        
        