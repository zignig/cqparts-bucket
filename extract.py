import cadquery as cq
import cqparts
import math
from collections import OrderedDict


from manufacture import Lasercut, Printable

# makes an array of local objects
class Extractor:
    def __init__(self,manufacture=[Lasercut,Printable]):
        # for duplicate names
        self.track = {}
        self.parts = OrderedDict()
        self.breakout = OrderedDict()
        for i in manufacture:
            self.breakout[i.__name__] = i

    def scan(self, obj, name):
        if isinstance(obj, cqparts.Part):
            if name in self.track:
                actual_name = name + "_%03i" % self.track[name]
                self.track[name] += 1
            else:
                self.track[name] = 1
                actual_name = name
            self.parts[actual_name] = obj

        if isinstance(obj, cqparts.Assembly):
            for i in obj.components:
                self.scan(obj.components[i], i)

    def show(self):
        for j in self.parts:
            i = self.parts[j]
            area = i.bounding_box.xlen * i.bounding_box.ylen
            print(i.__class__, i.bounding_box.xlen, i.bounding_box.ylen, area)

    def get_parts(self):
        return self.parts

