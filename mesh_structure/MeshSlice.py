# -*- coding: utf-8 -*-

import numpy as np


class MeshSlice:

    def __init__(self, contour):
        self.contour = contour
    
    def slice_mesh(self, start_v, end_v, slice_edges):

        idx_e1 = 3 #np.where(self.contour==start_v)
        idx_e2 = 15 #np.where(self.contour==end_v)
        
        edge_list_1 = self.contour[idx_e1:idx_e2]    
        edge_list_1 = np.append(edge_list_1, slice_edges[::-1])

        edge_list_2 = self.contour[:idx_e1]
        edge_list_3 = self.contour[idx_e2:]
        edge_list_2 = np.append(edge_list_2, slice_edges)
        edge_list_2 = np.append(edge_list_2, edge_list_3)
        
        return edge_list_1, edge_list_2
        