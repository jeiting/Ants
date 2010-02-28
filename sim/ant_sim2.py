"""
ant_sim2.py

Second pass at an ant simulation.

"""
from random import random as rand
from math import atan, sin , cos

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

BIN_SIZE = 10
XBINS = int(SCREEN_WIDTH/BIN_SIZE)
YBINS = int(SCREEN_WIDTH/BIN_SIZE)

node_bins = {}
for x in xrange(XBINS):
    node_bins[x] = {}
    for y in xrange(YBINS):
        node_bins[x][y] = []


SKY_HEIGHT = 100
PI = 3.14
class Ant(object):
    def __init__(self, waypoint):
        self.waypoint = waypoint
        self.previous_point = None
        self.has_dirt = False
        
    def tick(self):
        num_paths = len(self.waypoint.neighbors)
        do_dig = False
        new_point = None
        if self.waypoint.y <= SKY_HEIGHT:
            self.has_dirt = False
        r = rand()
        if num_paths == 1 and not self.has_dirt:
            # Dead end
            if r > .3:
                do_dig = True
        elif num_paths == 2 and not self.has_dirt:
            # Straight tunnel
            if r > .001:
                do_dig = True
        else:
            do_dig = False
            # Nothing special here
            # Pick a random node
            next_point = self.waypoint.neighbors[int(rand()*len(self.waypoint.neighbors))]
            self.previous_point = self.waypoint
            self.waypoint = next_point
        
        if do_dig:
            # dig a new waypoint
            if not self.previous_point:
                # dig down
                theta = -PI/2
            else:
                dx = self.waypoint.x - self.previous_point.x
                if dx == 0:
                    theta = -PI/2
                else:
                    theta = atan((self.waypoint.y - self.previous_point.y)/(dx))
            new_x = self.waypoint.x + BIN_SIZE*sin(theta)
            new_y = self.waypoint.y + BIN_SIZE*cos(theta)
            new_point = Node()
            new_point.x = new_x
            new_point.y = new_y
        
        if new_point:
            self.has_dirt = True
            self.waypoint.neighbors.append(new_point)
            new_point.neighbors.append(self.waypoint)
            self.previous_point = self.waypoint
            self.waypoint = new_point
            bin_x, bin_y = bin(new_point.x,new_point.y)
            node_bins[bin_x][bin_y].append(new_point)
        
class Node(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.neighbors = []
    

def print_map():
    for x in xrange(XBINS):
        line = "%3d: " % x
        for y in xrange(YBINS):
            if len(node_bins[x][y]) > 0:
                line += "*"
            else:
                line += " "
        print line

def bin(x,y):
    return int(float(x)/BIN_SIZE), int(float(y)/float(BIN_SIZE))

def main():
    # Cover the surface with waypoints for ants to move over
    prev_node = None
    for x in xrange(XBINS):
        n = Node()
        n.x = x*BIN_SIZE
        n.y = SKY_HEIGHT
        bin_x, bin_y = bin(n.x,n.y)
        node_bins[bin_x][bin_y].append(n)
        n.neighbors.append(prev_node)
        if prev_node:
            prev_node.neighbors.append(n)
        prev_node = n
    # Surface populated
    
    # create an ant
    a = Ant(prev_node)
    for x in xrange(1000000):
        a.tick()
    
    print_map()

if __name__ == "__main__":
    main()