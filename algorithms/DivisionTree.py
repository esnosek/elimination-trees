# -*- coding: utf-8 -*-
import bintrees as bt
import algorithms.CuttingUtils as cu
import numpy as np
from test import create_mesh
import unittest
import tree_view.meshDrawer as md
import sys

class DivisionTree:
    def __init__(self):
        self.all_countours = bt.FastRBTree()
    
    def start(self, mesh):
        root = Node(mesh.contour, None, None)
        #all_countours[key] = root
        self.create_tree(root.contour1, root)
        
    def create_tree(self, parent_contour, parent_node):
        possible_cuts = cu.get_possible_cuts(parent_contour)
        p = 0
        if parent_contour.contour.size > 4:
            print("BUMBUM        ", parent_contour.contour.size)
            print(" ")
            for path in possible_cuts:
                p = p + 1
                new_contour1, new_contour2 = parent_contour.slice_contour(path)
                new_node = Node(new_contour1, new_contour2, parent_contour)
                parent_node.children = np.append(parent_node.children, new_node)
                for v in parent_contour.contour:
                    print(v)
                print(" ")
                for v in path:
                    print(v)
                print(" ")
                for v in new_contour1.contour:
                    print(v)
                print(" ")
                for v in new_contour2.contour:
                    print(v)
                print(" ")
                #if path[0].x == 8 and path[0].y == 8:
                if p == 2:
                    #md.draw_contour(new_contour2.contour, 'k')
                    #md.draw_contour(new_contour1.contour, 'r')
                    md.draw_slice_vertices_with_edges(new_contour1.contour, 'k')
                    #md.draw_slice_vertices_with_edges(new_contour2.contour, 'r')
                    #md.draw_slice(path, 'g')
                    sys.exit("Error message")
                self.create_tree(new_contour1, new_node)
                self.create_tree(new_contour2, new_node)
        else:
            print("JUZ ZROBIONE")
                


class Node:
    def __init__(self, contour1, contour2, parent_contour):
        self.parent_contour = parent_contour
        self.contour1 = contour1
        self.contour2 = contour2
        self.children = np.empty(dtype=object, shape=0)
        
            
class DivisionTreeTests(unittest.TestCase):
 
    def test_cut(self):
        mesh = create_mesh()
        tree = DivisionTree()
        tree.start(mesh)
        

if __name__ == '__main__':
    unittest.main()
  