# -*- coding: utf-8 -*-
from mesh_structure.Direction import Direction
from mesh_structure.Vertex import Vertex
from mesh_structure.Edge import Edge
from test import create_mesh
import copy
import unittest
# todo
# zrobić graf z wierzchołkami prowadzącymi do celu

def get_possible_cuts(start_a, point_b):
    pass

# wersja ze wszystkimi punktami po drodze (dźubdźająca)
def find_way(current_point, end_point_list, arrival_direction, used_cross_points):
    
    if current_point in end_point_list or current_point in used_cross_points:
        return True
     
  
    elif is_there_any_way(current_point, arrival_direction): 
        possible_travel_directions = get_possible_directions(current_point, arrival_direction)

        if len(possible_travel_directions) > 1:
            used_cross_points.append(current_point)
            used_cross_points = copy.copy(used_cross_points)
                
        is_current_useful = False

        for direction in possible_travel_directions:
            travel_edge = current_point.get_shortest_edge_in_direction(direction) # longest
            travel_point = get_second_edge_point(current_point, travel_edge)

            if find_way(travel_point, end_point_list, direction, used_cross_points.copy()):
                is_current_useful = True
     
#        tutaj dodawanie do  end_point_list
#        if current_is_useful:
            # pakowanie do listy

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
    elif arrival_direction in [Direction.top, Direction.bottom]:
        if (Direction.top in possible_directions) and (Direction.bottom not in possible_directions):
            possible_directions.remove(Direction.top)
        elif (Direction.top not in possible_directions) and (Direction.bottom in possible_directions):
            possible_directions.remove(Direction.bottom)

    # tego ifa nie powiino być ale jest, zawsze remove
    if arrival_direction in possible_directions:
        possible_directions.remove(arrival_direction)
    return possible_directions

def is_there_any_way(point, arrival_direction):
    # jeżeli dotarliśmy do krawędzi to nie mam drogi dalej
    if point.is_border_vertex:
         return False
    if get_oposite_direction(arrival_direction) in point.get_existing_edge_directions():
         return True


class CuttingTests(unittest.TestCase):

    def test_creating_mesh(self):
        mesh = create_mesh()    
        test_vertex_a = Vertex(4, 2)
        test_vertex_b = Vertex(4, 2)
        self.assertEqual(test_vertex_a, test_vertex_b)
    
        
if __name__ == '__main__':
    unittest.main()
        
        