import numpy as np
import mesh_structure.MeshContour as MeshContour
import mesh_structure.VertexUtils as VertexUtils
import mesh_structure.EdgeUtils as EdgeUtils
import bintrees


class Mesh:

    def __init__(self,):
        self.sorted_vertex_lists = VertexUtils.SortedVertexLists()
        self.sorted_edge_list = EdgeUtils.SortedEdgeList()
        self.all_countour_nodes = bintrees.FastRBTree()
        self.contour = None

    def create_vertex(self, x, y):
        v = VertexUtils.Vertex(x, y)
        key_x = (x, y)
        key_y = (y, x)
        if key_x in self.sorted_vertex_lists.x_sorted:
            return self.sorted_vertex_lists.x_sorted[key_x]
        else:
            self.sorted_vertex_lists.x_sorted.insert(key_x, v)
            self.sorted_vertex_lists.y_sorted.insert(key_y, v)
        return v

    def create_edge(self, v1, v2):
        e = EdgeUtils.Edge(v1, v2)
        if e in self.sorted_edge_list:
            return self.sorted_edge_list[e]
        else:
            v1.add_incident_edge(e)
            v2.add_incident_edge(e)
            self.sorted_edge_list.add_edge(e)
        return e

    def create_mesh_contour(self):
        contour_vertices = np.empty(dtype=object, shape=0)
        contour_vertices = np.append(contour_vertices, self.__get_left_border())
        contour_vertices = np.append(contour_vertices, self.__get_top_border())
        contour_vertices = np.append(contour_vertices, self.__get_right_border())
        contour_vertices = np.append(contour_vertices, self.__get_bottom_border())
        self.contour = MeshContour.MeshContour(contour_vertices, self)

    def get_all_contour_nodes_count(self):
        counter = 0
        for perent_hash in self.all_countour_nodes:
            counter += len(self.all_countour_nodes[perent_hash])
        return counter

    def add_to_all_contour_nodes(self, contour_node):
        perent_hash = contour_node.contour.hash_key
        if perent_hash in self.all_countour_nodes:
            self.all_countour_nodes[perent_hash] = np.append(self.all_countour_nodes[perent_hash], contour_node)
        else:
            self.all_countour_nodes[perent_hash] = np.array([contour_node])

    def get_from_all_contour_nodes(self, contour):
        contour_hash_key = contour.hash_key
        if contour_hash_key in self.all_countour_nodes:
            for contour_node in self.all_countour_nodes[contour_hash_key]:
                if contour_node.contour == contour:
                    return contour_node
        return False

    def is_in_all_contour_nodes(self, contour):
        contour_hash_key = contour.hash_key
        if contour_hash_key in self.all_countour_nodes:
            for contour_node in self.all_countour_nodes[contour_hash_key]:
                if contour_node.contour == contour:
                    return True
        return False

    def __get_lower_left_vertex(self):
        return self.sorted_vertex_lists.get_vertex(0, 0)

    def __get_upper_left_vertex(self):
        return self.sorted_vertex_lists.get_vertex(0, self.sorted_vertex_lists.get_max_y())

    def __get_upper_right_vertex(self):
        return self.sorted_vertex_lists.get_vertex(self.sorted_vertex_lists.get_max_x(),
                                                    self.sorted_vertex_lists.get_max_y())

    def __get_lower_right_vertex(self):
        return self.sorted_vertex_lists.get_vertex(self.sorted_vertex_lists.get_max_x(), 0)

    def __get_top_border(self):
        border_vertices = np.empty(dtype=object, shape=0)
        current_edge = self.__get_upper_left_vertex().right_edges.get_longest_edge()
        border_vertices = np.append(border_vertices, current_edge.v1)
        upper_right_vertex = self.__get_upper_right_vertex()
        while current_edge.v1.x < upper_right_vertex.x:
            if current_edge.v2.x < upper_right_vertex.x:
                try:
                    current_edge = current_edge.v2.right_edges.get_longest_edge()
                    border_vertices = np.append(border_vertices,
                                                current_edge.v1)
                except ValueError:
                    continue
            else:
                break
        return border_vertices

    def __get_right_border(self):
        border_vertices = np.empty(dtype=object, shape=0)
        current_edge = self.__get_upper_right_vertex().bottom_edges.get_longest_edge()
        border_vertices = np.append(border_vertices, current_edge.v2)
        lower_right_vertex = self.__get_lower_right_vertex()
        while current_edge.v2.y > lower_right_vertex.y:
            if current_edge.v1.y > lower_right_vertex.y:
                try:
                    current_edge = current_edge.v1.bottom_edges.get_longest_edge()
                    border_vertices = np.append(border_vertices, current_edge.v2)
                except ValueError:
                    continue
            else:
                break
        return border_vertices

    def __get_bottom_border(self):
        border_vertices = np.empty(dtype=object, shape=0)
        current_edge = self.__get_lower_right_vertex().left_edges.get_longest_edge()
        border_vertices = np.append(border_vertices, current_edge.v2)
        lower_left_vertex = self.__get_lower_left_vertex()
        while current_edge.v2.x > lower_left_vertex.x:
            if current_edge.v1.x > lower_left_vertex.x:
                try:
                    current_edge = current_edge.v1.left_edges.get_longest_edge()
                    border_vertices = np.append(border_vertices,
                                                current_edge.v2)
                except ValueError:
                    continue
            else:
                break
        return border_vertices

    def __get_left_border(self):
        border_vertices = np.empty(dtype=object, shape=0)
        current_edge = self.__get_lower_left_vertex().top_edges.get_longest_edge()
        border_vertices = np.append(border_vertices, current_edge.v1)
        upper_left_vertex = self.__get_upper_left_vertex()
        while current_edge.v1.y < upper_left_vertex.y:
            if current_edge.v2.y < upper_left_vertex.y:
                try:
                    current_edge = current_edge.v2.top_edges.get_longest_edge()
                    border_vertices = np.append(border_vertices,
                                                current_edge.v1)
                except ValueError:
                    continue
            else:
                break
        return border_vertices
