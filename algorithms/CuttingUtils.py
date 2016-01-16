# -*- coding: utf-8 -*-
from mesh_structure.Direction import Direction
from copy import copy


def get_possible_cuts(contour):
    possible_paths = []
    for point_a_idx in range(len(contour.contour)):
        for point_b_idx in range(point_a_idx + 1, len(contour.contour)):
            point_a = contour.contour[point_a_idx]
            point_b = contour.contour[point_b_idx]
            
            inside_directions =  contour.get_inside_directions(contour[point_a_idx - 1],
                                                               point_a, 
                                                               contour[point_a_idx + 1])
                                                               
            existing_directions = point_a.get_existing_edge_directions()
            
            possible_directions = list(set(inside_directions).intersection(existing_directions))
            
            if len(inside_directions) > 0:
                for d in possible_directions:
                    inside_edge = point_a.get_longest_edge_in_direction(d)
                    used_cross_points = [point_a]
                    second_point_a = inside_edge.get_second_edge_vertex(point_a)

                    find_path(second_point_a, [point_b], d.get_oposite_direction(), used_cross_points, possible_paths, contour.contour_index)

               
    return possible_paths


def find_path(current_point, end_point_list, arrival_direction, used_cross_points, possible_paths, contour_index):

    if current_point in end_point_list:
        used_cross_points = copy_used_points_list_and_append(current_point, used_cross_points)
        possible_paths.append(used_cross_points)    
        return True
        
    elif current_point in used_cross_points or (current_point.x, current_point.y) in contour_index:
        return False

    elif is_there_any_way(current_point, arrival_direction, contour_index):
        
        possible_travel_directions = get_possible_directions(current_point, arrival_direction)     
        used_cross_points = copy_used_points_list_and_append(current_point, used_cross_points)
            
        is_current_useful = False

        for direction in possible_travel_directions:

            travel_point = travel_to_next_point(current_point, direction)

            if find_path(travel_point, end_point_list, direction.get_oposite_direction(), used_cross_points, possible_paths, contour_index):
                is_current_useful = True

        return is_current_useful

    else:
        return False
        
def copy_used_points_list_and_append(point, used_points):
    used_points_copy = copy(used_points)
    used_points_copy.append(point)
    return used_points_copy


def travel_to_next_point(current_point, direction):
    travel_edge = current_point.get_longest_edge_in_direction(direction)
    travel_point = travel_edge.get_second_edge_vertex(current_point)
    return travel_point


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


def is_there_any_way(point, arrival_direction, contour_index):
    if (point.x, point.y) in contour_index:
        return False
    elif arrival_direction.get_oposite_direction() in point.get_existing_edge_directions():
        return True
    else:
        return False
