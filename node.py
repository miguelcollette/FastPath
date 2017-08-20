class node:
    def __init__(self, coord_x, coord_y):
        self.x = coord_x
        self.y = coord_y
        self.adj = []
        self.c = 0
        self.h = 0
        self.in_opened = False
        self.in_closed = False
        self.n_from = None
        self.r_from = None
    
    # rich comparison methods for two nodes based on the cost and heuristic.
    #if they are equal then the higher cost is preferred, as it means we are possibly closer to the goal.
    #a node is greater than another if its c+h is less or equal with greater c
    #equal is defined by the coordinates only, so we can still know whether a node is the same as another and not only whether the cost estimation is the same.
    def __eq__(self, other):
        return other != None and self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return other == None or (self.x != other.x or self.y != other.y)

    def __gt__(self, other):
        return self.c + self.h < other.c + other.h or (self.c + self.h == other.c + other.h and self.c > other.c)
        
    def __ge__(self, other):
        return self.c + self.h < other.c + other.h or (self.c + self.h == other.c + other.h and self.c >= other.c)
        
    def __lt__(self, other):
        return self.c + self.h > other.c + other.h or (self.c + self.h == other.c + other.h and self.c < other.c)
        
    def __le__(self, other):
        return self.c + self.h > other.c + other.h or (self.c + self.h == other.c + other.h and self.c <= other.c)
        
    def __repr__(self):
        return str(self.h) + ' ' + str(self.c)

    def manhattan_distance(self, n):
        return abs(self.x - n.x) + abs(self.y - n.y)
    
    def euclidean_distance(self, n):
    #in case diagonal routes were added, then the euclidean distance should be used for the heuristic
        return math.sqrt((self.x - n.x)**2 + (self.y - n.y)**2)
        
    def reset(self):
    #reset the path_finding related attributes. In case we run several queries in the same graph.
        self.c = 0
        self.h = 0
        in_opened = False
        in_closed = False
        n_from = None
        r_from = None
        
        