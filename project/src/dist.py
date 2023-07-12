import threading
import sys

class Dist:
    def __init__(self):
        self.m = threading.Lock()
        self.left = 0
        self.front = 0
        self.right = 0
        self.raw = []

    def update(self, data):

        def getmin(a, b):
            in_rng = lambda x: data.range_min <= x <= data.range_max
            vsp = filter(in_rng, data.ranges[a:b])
            if len(vsp) > 0:
                return min(vsp)
            else:
                return sys.maxint

        newfront = getmin(330, 360)
        newleft = getmin(30, 80)
        newright = getmin(300,330)
        self.m.acquire()
        self.left = newleft
        self.front = newfront
        self.right = newright
        self.raw = data
        self.m.release()

    def get(self):
        self.m.acquire()
        l = self.left
        f = self.front
        r = self.right
        self.m.release()
        return (f, l, r)

    def angle_to_index(self, angle):
        return int((angle - self.raw.angle_min)/self.raw.angle_increment)


    def at(self, angle):
        def getmin(a, b):
            in_rng = lambda x: self.raw.range_min <= x <= self.raw.range_max
            vsp = filter(in_rng, self.raw.ranges[a:b])
            if len(vsp) > 0:
                return min(vsp)
            else:
                return sys.maxint
        self.m.acquire()
        i = self.angle_to_index(angle)
        start = i - 15
        if start < 0:
            start = 0
        end = i + 15
        if end >= len(self.raw.ranges):
            end = len(self.raw.ranges) - 1
        ans = getmin(start, end)
        self.m.release()
        return ans
