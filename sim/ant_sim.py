#!/usr/bin/env python
"""
Simulate the alg. for building an ant colony using only ants. 

Just focus on the scruct and the data structure, you can then 
print work out the simulation parameters.


"""

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
GRID_ROWS = 100

GRID_DIM = SCREEN_HEIGHT/GRID_ROWS

GRID_COLS = SCREEN_WIDTH/GRID_DIM

GROUND_LEVEL = 200

PI = 3.1415927

SPREAD = PI/5
BRANCH_THRESHOLD = .001
NEW_THRESHOLD = .6

NUM_DIGS = 4*GRID_ROWS
NUM_PASSES = 4


import random
import math
from math import sqrt,sin,cos



class Node(object):
    left = 0
    right = 0
    def __init__(self, r = None, theta = None):
        self.parent = None
        self.x = None
        self.y = None
        self.branches = []
    
    def set_point(self,r,theta):
        if self.parent.parent is not None:
            dx = self.parent.parent.x - self.parent.x
            dy = self.parent.parent.y - self.parent.y
            if dy == 0:
                angle = 0
            else:
                a = float(dx)/dy
                if a > 1:
                    angle = PI/2
                elif a < -1:
                    angle = -PI/2
                else:
                    angle = math.asin(a)
        else:
            angle = 0
        angle *= .4
        if abs(theta) > PI/2:
            print "WRONG!"
        self.x = int(round(self.parent.x + r*sin(angle + theta)))
        self.y = int(round(self.parent.y + r*cos(angle + theta)))
    
    
def grid_for_point(screen_x, screen_y):
    """ Takes screen coords and returns grid. """
    return (screen_x/GRID_DIM , screen_y/GRID_DIM)

def local_grid_coords(x,y):
    """ Takes screen pixel coords and returns local coords. """
    grid_x, grid_y = grid_for_point(x,y)
    return (x - grid_x*GRID_DIM, y - grid_y*GRID_DIM)

def generate_next_point(x,y):
    # Find the farthest corner to produce the largest R
    local_x, local_y = local_grid_coords(x,y)
    #print "Starting local coords: %d, %d" % (local_x, local_y)
    min_r = int(sqrt(abs(local_x - GRID_DIM)**2 + abs(local_y - GRID_DIM)**2))
    max_r = int(sqrt(GRID_DIM**2 + GRID_DIM**2))
    #print "Minimum R: %d" % min_r
    #print "Maximum R: %d" % max_r
    if min_r == max_r:
        min_r = 0
    r = random.randrange(min_r,max_r)
    #print "R = %d" % r
    theta = 10
    while abs(theta) > PI/2:
        theta = random.gauss(0,SPREAD)
    #print "theta = %.2f" % theta
    return r, theta

def main():
    grid = {}
    for x in xrange(GRID_COLS):
        grid[x] = {}
        for y in xrange(GRID_ROWS):
            grid[x][y] = None 
    print "Screen width     %d"     % SCREEN_WIDTH
    print "Screen height    %d"    % SCREEN_HEIGHT
    print "Grid rows        %d"        % GRID_ROWS
    print "Grid cols        %d"        % GRID_COLS
    print "Grid dim         %d"     % GRID_DIM
    print "Ground level     %d"     % (GROUND_LEVEL/GRID_DIM)
    
    start_i = int(random.random()*SCREEN_WIDTH)
    start_j = GROUND_LEVEL/GRID_DIM
    starting_grid = grid_for_point(start_i,start_j)
    print "Random starting point: %d,%d" % (start_i, start_j)
    print "Random starting grid: %d,%d" % starting_grid
    
    # Create first point node
    first_node = Node()
    first_node.x = start_i
    first_node.y = start_j
    grid[starting_grid[0]][starting_grid[1]] = first_node
    
    # Start the loop
    for p in xrange(NUM_PASSES):
        last_node = first_node
        for n in xrange(NUM_DIGS):
            r, theta = generate_next_point(last_node.x, last_node.y)
            nbranches = len(last_node.branches)
            if  nbranches > 0 and random.random() > BRANCH_THRESHOLD and nbranches < 3:
                last_node = last_node.branches[random.randrange(nbranches)]
            
            if random.random() > NEW_THRESHOLD:
                continue
            # Create new node
            node = Node()
            node.parent = last_node
            node.set_point(r,theta)
            i,j = grid_for_point(node.x,node.y)
            if i >= GRID_COLS or j >= GRID_ROWS or i < 0 or j < 0:
                continue
            if grid[i][j] is not None:
                #print "Already hit this node."
                last_node = grid[i][j]
                continue
            grid[i][j] = node
            last_node.branches.append(node)
            last_node = node
    for x in grid:
        row_str = "%2d: " % x
        for y in grid[x]:
            if grid[x][y] is not None:
                row_str += "*"
            else:
                row_str += " "
        print row_str
    print "Done"
if __name__ == "__main__":
    main()