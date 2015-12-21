import matplotlib.pyplot as plt
import numpy as np

def draw_mesh_with_cutting_edge(mesh):
    plt.axis([-2, 16 + 2, -2, 8 + 2])

    for key in mesh.edge_list.edge_tree:
        edge = mesh.edge_list.edge_tree[key]
        plt.plot([edge.v1.x, edge.v2.x], [edge.v1.y, edge.v2.y], 'k')
    for edge in mesh.list1:
        plt.plot([edge.v1.x, edge.v2.x], [edge.v1.y, edge.v2.y], 'g')
    for edge in mesh.list2:
        plt.plot([edge.v1.x, edge.v2.x], [edge.v1.y, edge.v2.y], 'y')
    for edge in mesh.slice_edges:
        plt.plot([edge.v1.x, edge.v2.x], [edge.v1.y, edge.v2.y], 'r')
    plt.show()

def draw_mesh(mesh, depth_level):
    plt.axis([-2, 2048 + 2, -2, 2048 + 2])
    
    if depth_level == 0:
        for key in mesh.edge_list.edge_tree:
            edge = mesh.edge_list.edge_tree[key]
            plt.plot([edge.v1.x, edge.v2.x], [edge.v1.y, edge.v2.y], 'k')
    else:
        for key in mesh.face_list.face_tree:
            face = mesh.face_list.face_tree[key]
            for e in face.edge_list:
                if face.level <= depth_level:
                    plt.plot([e.v1.x, e.v2.x], [e.v1.y, e.v2.y], 'k')

def draw_slice_vertices_with_edges(slice_vertices, colour):
    plt.axis([-2, 16 + 2, -2, 8 + 2])
    for vertex in slice_vertices:
        for key in vertex.top_edges.edge_incident:
            e = vertex.top_edges.edge_incident[key]
            plt.plot([e.v1.x, e.v2.x], [e.v1.y, e.v2.y], colour)
        for key in vertex.bottom_edges.edge_incident:
            e = vertex.bottom_edges.edge_incident[key]
            plt.plot([e.v1.x, e.v2.x], [e.v1.y, e.v2.y], colour)
        for key in vertex.right_edges.edge_incident:
            e = vertex.right_edges.edge_incident[key]
            plt.plot([e.v1.x, e.v2.x], [e.v1.y, e.v2.y], colour)
        for key in vertex.left_edges.edge_incident:
            e = vertex.left_edges.edge_incident[key]
            plt.plot([e.v1.x, e.v2.x], [e.v1.y, e.v2.y], colour)
 
def draw_slice(slice_vertices, colour):
    plt.axis([-2, 16 + 2, -2, 8 + 2])
    last_index = len(slice_vertices) - 1
    curr_index = 0
    for vertex in slice_vertices:
        if curr_index == last_index:
            break
        next_index = curr_index + 1
        v1 = slice_vertices[curr_index]
        v2 = slice_vertices[next_index]
        plt.plot([v1.x, v2.x], [v1.y, v2.y], colour)
        curr_index = curr_index + 1
        
def draw_contour(vertex_list, colour):
    plt.axis([-2, 16 + 2, -2, 8 + 2])
    last_index = len(vertex_list) - 1
    for vertex in vertex_list:
        curr_index = np.where(vertex_list == vertex)[0][0]
        if curr_index == last_index:
            next_index = 0
        else:
            next_index = curr_index + 1
        v1 = vertex_list[curr_index]
        v2 = vertex_list[next_index]
        plt.plot([v1.x, v2.x], [v1.y, v2.y], colour)
