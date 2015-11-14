# -*- coding: utf-8 -*-

import numpy as np


class MeshContour:

    def __init__(self, contour):
        self.contour = contour

    def slice_contour(self, start_v, end_v, slice_edges):

        index_e1 = np.where(self.contour == start_v)
        index_e2 = np.where(self.contour == end_v)

        edge_list_1 = self.contour[index_e1:index_e2]
        edge_list_1 = np.append(edge_list_1, slice_edges[::-1])

        edge_list_2 = self.contour[:index_e1]
        edge_list_3 = self.contour[index_e2:]
        edge_list_2 = np.append(edge_list_2, slice_edges)
        edge_list_2 = np.append(edge_list_2, edge_list_3)

        return edge_list_1, edge_list_2
