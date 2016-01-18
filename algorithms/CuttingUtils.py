# -*- coding: utf-8 -*-
from mesh_structure.Direction import Direction
from copy import copy

possible_paths = []
end_vertices_list = []
contour = None

def get_possible_paths(c):
    global possible_paths
    global end_vertices_list
    global contour
    contour = c
    possible_paths = []
    for index_start_v in range(len(contour)):
        for index_end_v in range(index_start_v + 1, len(contour)):
            start_v = contour[index_start_v]
            end_v = contour[index_end_v]
            end_vertices_list = [end_v]
            possible_directions = contour.get_possible_inside_directions(start_v)
            if len(possible_directions) > 0:
                for direction in possible_directions:
                    travel_vertex = travel_to_next_vertex(start_v, direction)
                    used_cross_vertices = [start_v]
                    find_path(travel_vertex, direction.get_oposite_direction(), used_cross_vertices)
    return possible_paths


def find_path(curr_v, arrival_direction, used_cross_vertices):
    global possible_paths
    global end_vertices_list
    global contour

    if curr_v in end_vertices_list:
        used_cross_vertices = copy_used_vertices_list_and_append(curr_v, used_cross_vertices)
        possible_paths.append(used_cross_vertices)    
        return True
        
    elif curr_v in used_cross_vertices or curr_v in contour:
        return False

    elif is_there_any_way(curr_v, arrival_direction):
        possible_travel_directions = get_possible_travel_directions(curr_v, arrival_direction)     
        used_cross_vertices = copy_used_vertices_list_and_append(curr_v, used_cross_vertices)
        is_curr_v_useful = False
        for direction in possible_travel_directions:
            travel_vertex = travel_to_next_vertex(curr_v, direction)
            if find_path(travel_vertex, direction.get_oposite_direction(), used_cross_vertices):
                is_curr_v_useful = True
        return is_curr_v_useful
    else:
        return False


def copy_used_vertices_list_and_append(vertex, used_vertices):
    used_vertices_copy = copy(used_vertices)
    used_vertices_copy.append(vertex)
    return used_vertices_copy


def travel_to_next_vertex(v, direction):
    travel_edge = v.get_longest_edge_in_direction(direction)
    travel_vertex = travel_edge.get_second_vertex_from_edge(v)
    return travel_vertex


def get_possible_travel_directions(v, arrival_direction):
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


def is_there_any_way(v, arrival_direction):
    global contour
    if v in contour:
        return False
    elif arrival_direction.get_oposite_direction() in v.get_existing_edge_directions():
        return True
    else:
        return False
