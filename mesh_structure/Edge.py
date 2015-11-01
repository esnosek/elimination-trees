# -*- coding: utf-8 -*-

import bintrees as bt


class Edge:

    def __init__(self, v1, v2):
        # trzeba zadbac zeby v1 < v2
        self.v1 = v1
        self.v2 = v2
        self.__set_length()
        self.face_incident = bt.FastRBTree()

    def add_incident_face(self, f):
        key = (f.level, f.id)
        self.face_incident.insert(key, f)

    def __set_length(self):
        if (self.v1.x == self.v2.x):
            self.length = abs(self.v1.y - self.v2.y)
        else:
            self.length = abs(self.v1.x - self.v2.x)

    def __str__(self):
        return ("[" + str(self.v1.x) + ", " + str(self.v1.y) + "], [" +
                str(self.v2.x) + ", " + str(self.v2.y) + "]")

    def __eq__(self, other):
        return ((self.v1 == other.v1 or self.v1 == other.v2) and
                (self.v2 == other.v1 or self.v2 == other.v2))

    def __ne__(self, other):
        return not self.__eq__(other)
