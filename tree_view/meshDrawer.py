import matplotlib.pyplot as plt
import numpy as np


plt.figure(figsize=(16, 8))
counter = 1

def draw_tree_node(root_node):
    global counter
    fig, ax = plt.subplots(200,1)
    from algorithms.DivisionTree import TreeLeaf
    while root_node is not TreeLeaf:
        draw_contour_from_optimal_tree(root_node.contour, 'k', ax)
        counter += 1
        draw_tree_node(root_node.child1)
        draw_tree_node(root_node.child2)
    

def draw_contour_from_optimal_tree(vertex_list, colour, ax):
    global counter
    last_index = len(vertex_list) - 1
    for vertex in vertex_list:
        curr_index = np.where(vertex_list == vertex)[0][0]
        if curr_index == last_index:
            next_index = 0
        else:
            next_index = curr_index + 1
        v1 = vertex_list[curr_index]
        v2 = vertex_list[next_index]
        ax[counter].plot([v1.x, v2.x], [v1.y, v2.y], colour)
    plt.show()
        
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
    plt.axis([-2, 16 + 2, -2, 8 + 2])
    
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
 
def draw_slice(mesh, slice_vertices, colour):
    plt.axis([mesh.min_x, mesh.max_x , mesh.min_y , mesh.max_y ])
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
        
def draw_contour(mesh, vertex_list, colour):
    plt.axis([mesh.min_x, mesh.max_x, mesh.min_y, mesh.max_y])
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
    

def draw_slice_and_contour(mesh, tree_node, file_name='tmp.png'):
    for child in tree_node.children:
        draw_slice(mesh, child.path, 'r')
    draw_contour(mesh, tree_node.contour.contour, 'k')   
    plt.savefig(file_name)
    
def clear_tmp():
    import os, shutil
    folder = 'tmp'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except e:
            print(e)
    
def draw_tree(tree):
    
    leaf_id = 0    
    
    from ete3 import Tree, faces, TreeStyle
    
    # Loads an example tree
    nw = """
    (((Dme:0.008339,Dme:0.300613)1.000000:0.596401,
    (Cfa:0.640858,Hsa:0.753230)1.000000:0.182035)1.000000:0.106234,
    ((Dre:0.271621,Cfa:0.046042)1.000000:0.953250,
    (Hsa:0.061813,Mms:0.110769)1.000000:0.204419)1.000000:0.973467);
    """
    t = Tree(nw)
    
    # Create faces based on external images
    humanFace = faces.ImgFace("foo.png")#, width=500, height=500)
    
    def mylayout(node):
        if node.is_leaf():
            pass
        else:
    
            faces.add_face_to_node(humanFace, node, 1)
    
        if node.is_leaf() and node.name.startswith("Hsa"):
            node.img_style["bgcolor"] = "#9db0cf"
    
    # And, finally, Visualize the tree using my own layout function
    ts = TreeStyle()
    ts.layout_fn = mylayout
    t.show(tree_style = ts)
    


    
    
    

