# -*- coding: utf-8 -*-
import bintrees as bt
import algorithms.CuttingUtils as cu
import numpy as np
from test import create_mesh
import unittest
import tree_view.meshDrawer as md

class DivisionTree:
    def __init__(self, initial_contour):
        self.all_countours = bt.FastRBTree()
    
    def start(self, mesh):
        root = Node(mesh.contour, None, None)
        #all_countours[key] = root
        self.create_tree(root.contour1, root)
        
    def create_tree(self, parent_contour, parent_node):
        possible_cuts = cu.get_possible_cuts(parent_contour)
        if parent_contour.contour.size > 4:
            print("ITERACJA        ", parent_contour.contour.size)
            print(" ")
            for path in possible_cuts:
                new_contour1, new_contour2 = parent_contour.slice_contour(path)
                new_node = Node(new_contour1, new_contour2, parent_contour)
                parent_node.children = np.append(parent_node.children, new_node)
                for v in new_contour1.contour:
                    print(v)
                print(" ")
                for v in new_contour2.contour:
                    print(v)
                print(" ")
                #md.draw_contour(new_contour2.contour, 'k')
                #md.draw_slice_vertices_with_edges(new_contour1.contour)
                #md.draw_slice(path, 'g')
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
        tree = DivisionTree(mesh.contour)
        tree.start(mesh)

if __name__ == '__main__':
    unittest.main()
  