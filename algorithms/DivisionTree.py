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
        self.all_countours = {}
        self.licznik = 0  
        
    def start(self, mesh):
        root = Node(mesh.contour, None, None)
        #all_countours[key] = root
        
        self.create_tree(root.contour1, root, 0)
        
    def create_tree(self, parent_contour, parent_node, counter):
#        for v in parent_contour.contour:
#            print(v)
#        print(self.__is_atomic_square(parent_contour))
    
        if not self.__is_atomic_square(parent_contour):
            possible_cuts = cu.get_possible_cuts(parent_contour)
            #print(len(possible_cuts))
            for path in possible_cuts:
                if counter > -1:
                    print(counter) 
                new_contour1, new_contour2 = parent_contour.slice_contour(path)
                #if new_contour1.get_center() in self.all_countours:
                    
                
                
                new_node = Node(new_contour1, new_contour2, parent_contour)
                parent_node.children = np.append(parent_node.children, new_node)
#                for v in parent_contour.contour:
#                    print(v)
#                print(" ")
#                for v in path:
#                    print(v)
#                print(" ")
#                for v in new_contour1.contour:
#                    print(v)
#                print(" ")
#                for v in new_contour2.contour:
#                    print(v)
#                print("###########################################")
#                if path[0].x == 9 and path[0].y == 1:
#                    if path[1].x == 9 and path[1].y == 2: # and new_contour2.contour[1].x == 16 and new_contour2.contour[1].y == 4:
#                        #if p == 2:
#                        #md.draw_contour(parent_contour.contour, 'k')
#                        #md.draw_contour(new_contour2.contour, 'k')
#                        md.draw_contour(new_contour1.contour, 'r')
#                        #md.draw_slice_vertices_with_edges(new_contour1.contour, 'k')
#                        #md.draw_slice_vertices_with_edges(new_contour2.contour, 'r')
#                        #md.draw_slice(path, 'g')
#                        sys.exit("Error message")
                #print("*" *40) 
                self.create_tree(new_contour1, new_node, counter + 1)
                self.create_tree(new_contour2, new_node, counter + 1)
        else:
            self.licznik = self.licznik + 1
            #print("ala ", self.licznik)
#            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#            for v in parent_contour.contour:
#                print(v)
#            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#            print("")
                
    def __is_atomic_square(self, parent_contour):
        for v in parent_contour.contour:
            index_curr_v = np.where(parent_contour.contour == v)[0][0]
            index_prev_v = index_curr_v - 1
            index_next_v = index_curr_v + 1
            prev_v = parent_contour[index_prev_v]
            next_v = parent_contour[index_next_v]
            inside_directions = parent_contour.get_inside_directions(prev_v, v, next_v)
            if len(inside_directions) > 0:
                return False
        return True

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
  