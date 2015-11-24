# -*- coding: utf-8 -*-
from mesh_structure.Direction import Direction

# todo
# zrobić graf z wierzchołkami prowadzącymi do celu

def get_possible_cuts(start_a, point_b):
	pass

# wersja ze wszystkimi punktami po drodze (dźubdźająca)
def find_way(current_point, end_point, arrival_direction):
	
	if current_point == end_point:
		return True
	elif is_there_any_way(current_point, arrival_edge): 
		possible_travel_directions = get_possible_directions(current_point, arrival_direction)

		is_current_useful = False

		for direction in possible_travel_directions:
			travel_edge = current_point.get_shortest_edge_in_direction(direction)
			travel_point = get_second_point_from_edge(current_point, travel_edge)

			if find_way(travel_point, end_point, direction):
				is_current_useful = True

		return is_current_useful
		
	else:
		return False

def get_second_point_from_edge(first_point, edge):
	if edge.v1 == first_point:
		return edge.v2
	else:
		return edge.v1

def get_possible_directions(point, arrival_direction):
	possible_directions = point.get_existing_edge_directions()
	if arrival_direction in possible_directions:
		possible_directions.remove(arrival_direction)
	return possible_directions

def is_there_any_way(point, arrival_edge):
	# jeżeli dotarliśmy do krawędzi to nie mam drogi dalej
	if point.is_border_vertex:
		return False

	#arrived_point to ten koniec krawędzi do którego przychodzimy
	if arrival_edge.v1 == point:
		arrived_point = arrival_edge.v1
		left_point = arrival_edge.v2
	else:
		arrived_point = arrival_edge.v2
		left_point = arrival_edge.v1

	# przyszliśmy pionowo
	if arrived_point.x == left_point.x:
		# z góry
		if left_point.y > arrived_point.y:
			# jeżeli rzyszliśmy z góry i nie możemy iść w dół to nie ma drogi
			if arrived_point.bottom_edges.is_empty():
				return False
			else:
				return True
		# z dołu
		else:
			if arrived_point.top_edges.is_empty():
				return False
			else:
				return True
	# przyszliśmy poziomo
	else:
		# z lewej
		if left_point.x < arrived_point.x:
			# jeżeli przyszliśmy z lewej i nie możemy iść w prawo to nie ma drogi
			if arrived_point.right_edges.is_empty():
				return False
			else:
				return True
		# z prawej
		else:
			if arrived_point.left_edges.is_empty():
				return False
			else:
				return True





