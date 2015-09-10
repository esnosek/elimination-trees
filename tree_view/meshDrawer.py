import matplotlib.pyplot as plt


def draw_mesh_with_cutting_edge(mesh):
    plt.axis([-2, mesh.max_x + 2, -2, mesh.max_y + 2])

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
    plt.axis([-2, mesh.max_x + 2, -2, mesh.max_y + 2])
    
    if depth_level == 0:
        for key in mesh.edge_list.edge_tree:
            edge = mesh.edge_list.edge_tree[key]
            plt.plot([edge.v1.x, edge.v2.x], [edge.v1.y, edge.v2.y], 'k')
    else:
        for key in mesh.face_list.face_tree:
            face = mesh.face_list.face_tree[key]
            for e in face.edge_list:
                if face.level < depth_level:
                    plt.plot([e.v1.x, e.v2.x], [e.v1.y, e.v2.y], 'k')