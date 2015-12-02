# -*- coding: utf-8 -*-
from mesh_structure.Direction import Direction
from mesh_structure.Vertex import Vertex
from mesh_structure.Edge import Edge
from test import create_mesh
import copy
import unittest
import random
from mesh_structure.MeshContour import MeshContour
import tree_view.meshDrawer as md
# wesja z longest

def get_possible_cuts(contour):
    possible_paths = []
    for point_a_idx in range(len(contour.contour)):
        for point_b_idx in range(point_a_idx + 1, len(contour.contour)):
            point_a = contour.contour[point_a_idx]
            point_b = contour.contour[point_b_idx]
            
           # print(str(point_a), str(point_b))
            #print(point_a.bottom_edges.edge_incident)            
            
            inside_direction = None
            if Direction.left in point_a.get_existing_edge_directions() and Direction.right in point_a.get_existing_edge_directions():
                if Direction.bottom in point_a.get_existing_edge_directions():
                    inside_direction = Direction.bottom
                elif Direction.top in point_a.get_existing_edge_directions():
                    inside_direction = Direction.top
            elif Direction.top in point_a.get_existing_edge_directions() and Direction.bottom in point_a.get_existing_edge_directions():
                if Direction.left in point_a.get_existing_edge_directions():
                    inside_direction = Direction.left
                elif Direction.right in point_a.get_existing_edge_directions():
                    inside_direction = Direction.right
            #print(point_a, inside_direction, point_a.get_existing_edge_directions())
            if inside_direction:
                inside_edge = point_a.get_longest_edge_in_direction(inside_direction)
                used_cross_points = [point_a]
                second_point_a = get_second_edge_point(point_a, inside_edge)
                #try:
                find_path(second_point_a, [point_b], get_oposite_direction(inside_direction), used_cross_points, possible_paths)
                
                #except:
                 #   print("ilosc tras " + str(len(possible_paths)))
                
    return possible_paths


def find_path(current_point, end_point_list, arrival_direction, used_cross_points, possible_paths):
    #print("ilosc tras " + str(len(possible_paths)))
    if current_point in end_point_list:
        
        used_cross_points.append(current_point)
        
        possible_paths.append(used_cross_points)
        
        #print(used_cross_points[-1].get_existing_edge_directions())
        return True
    elif current_point in used_cross_points or current_point.is_border_vertex:

        return False

    elif is_there_any_way(current_point, arrival_direction):

        possible_travel_directions = get_possible_directions(current_point, arrival_direction)
        if len(possible_travel_directions) > 1:
            cross_points = list(used_cross_points)
            
            
            cross_points.append(current_point)
            
        is_current_useful = False

        for direction in possible_travel_directions:
            travel_edge = current_point.get_longest_edge_in_direction(direction) # longest
            travel_point = get_second_edge_point(current_point, travel_edge)

            if find_path(travel_point, end_point_list, get_oposite_direction(direction), cross_points, possible_paths):
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
    
    possible_directions = list(point.get_existing_edge_directions())
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
        test_vertex_a = mesh.vertex_list.get_vertex((4, 0))
        test_vertex_b = mesh.vertex_list.get_vertex((16, 4))
        used_cross_points = []
        end_point_list = [test_vertex_b]
        possible_paths = []
        find_path(test_vertex_a, end_point_list, Direction.bottom, used_cross_points, possible_paths)

            
    def test_all_possible_cuts(self):
        return
        mesh = create_mesh()
        possible_paths = get_possible_cuts(mesh.contour)
            
        print("ilosc tras " + str(len(possible_paths)))
        
        
        
    def test_slice(self):
        mesh = create_mesh()
        possible_paths = get_possible_cuts(mesh.contour)
        random_index = random.randint(0,len(possible_paths)-1)
        random_path = possible_paths[random_index]
        contour1, contour2 = mesh.contour.slice_contour(random_path)

        #md.draw_slice_vertices_with_edges(contour1)
        #md.draw_slice_vertices_with_edges(contour2)
        
        md.draw_contour(contour1, 'k')
        md.draw_contour(contour2, 'r')
        md.draw_slice(random_path, 'g')
        
    def test_copy(self):
        return
        mesh = create_mesh()
        possible_paths = get_possible_cuts(mesh.contour)
        random_index = random.randint(0,len(possible_paths)-1)
        random_path = possible_paths[random_index]
        #print(str(random_path[0]), random_path[0].get_existing_edge_directions())
        point = mesh.vertex_list.get_vertex((random_path[0].x, random_path[0].y))    
        point2 = mesh.vertex_list.get_vertex((random_path[1].x, random_path[1].y))
        point3 = mesh.vertex_list.get_vertex((random_path[2].x, random_path[2].y))
        point_list = [point, point2]
        point_list2 = list(point_list)
        print(point_list[0].get_existing_edge_directions())
        print(point_list2[0].get_existing_edge_directions())
        #point_list[0].bottom_edges.edge_incident.clear()
        point_list2.append(point3)
        print(len(point_list))
        print(len(point_list2))
        
if __name__ == '__main__':
    unittest.main()
        
        