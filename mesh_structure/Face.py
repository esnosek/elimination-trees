# -*- coding: utf-8 -*-


class Face:

    def __init__(self, level, id, vertex_list, edge_list):
        self.vertex_list = vertex_list
        self.edge_list = edge_list
        self.level = level
        self.id = id

    def __str__(self):
        return (str(self.vertex_list[0]) +
                str(self.vertex_list[1]) +
                str(self.vertex_list[2]) +
                str(self.vertex_list[3]))

    def __eq__(self, other):
        return (self.vertex_list[0] == other.vertex_list[0] and
                self.vertex_list[2] == other.vertex_list[2])

    def __ne__(self, other):
        return not self.__eq__(other)
