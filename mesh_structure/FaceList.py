# -*- coding: utf-8 -*-

from mesh_structure.Face import Face
import bintrees as bt


class FaceList:

    def __init__(self):
        self.face_tree = bt.FastRBTree()

    def add_face(self, level, id, vertex_list, edge_list):
        f = Face(level, id, vertex_list, edge_list)
        key = (level, id)
        if key in self.face_tree:
            return self.face_tree[key]
        else:
            for v in vertex_list:
                v.add_incident_face(f)
            for e in edge_list:
                e.add_incident_face(f)
            self.face_tree.insert(key, f)
        return f
