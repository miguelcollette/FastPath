from PIL import Image
import ntpath
from collections import defaultdict
from node import *

key_points_tuple = (int('d3',16), int('54', 16), int('00',16)) #RGB values to be changed

class network:
    def __init__(self, image_file):
        # A network object, created from an image of the network.
        # The initialisation just creates the attributes that will be used when we create the graph from the parsing.
        self.image_file = image_file
        self.im = Image.open(image_file)
        self.pixels = self.im.load()
        self.size_x, self.size_y = self.im.size[0], self.im.size[1]
        self.network_graph = {}
        self.routes = []
        self.key_points = []
        self.coord_to_node = defaultdict(lambda:None)
    
    def create_image(self, name):
        self.im.save(name+'.png')
  
    def reload_image(self):
        self.im = Image.open(self.image_file)
        self.pixels = self.im.load()
  
    def create_res_image(self, indexes):
        im = Image.new(self.im.mode, self.im.size)
        pix = im.load()
        for index in indexes:
            for (x, y) in self.routes[index]:
                pix[x,y] = (255, 255, 255)
        for n in self.key_points:
            pix[n.x,n.y] = key_points_tuple
        im.save("./results/path_"+ ntpath.basename(self.image_file))
  
    def clear_path_data(self):
        for node in self.coord_to_node.values():
            node.reset()

    def build_network_graph(self, speeds):
    #This method creates the graph defined by the RGB matrix of the picture, nodes being the intersections, start/finish points, and end of roads.
    #pixels is the RGB matrix, speeds is the dictionary that links an RGB tuple to a speed
    #return an adjacence list that defines the graph, the start and finish points, a dictionary that links the coordinates to the node number, and a list of routes, to be able to recreate the path once we get it.

        routes = []
        key_points = []
        coord_to_node = defaultdict(lambda:None)
        
        for x in range(self.size_x):
            for y in range(self.size_y):
                if speeds[str(self.pixels[x,y])] == 1:
                #found a node
                    if coord_to_node[str((x,y))] == None:
                    #new Node to add
                        n = node(x, y)
                        coord_to_node[str((x,y))] = n
                        if self.pixels[x,y] == key_points_tuple:
                        #the node is also a start / finish point
                            key_points.append(n)
          
                    self.explore_route(x, y, coord_to_node, routes, key_points, speeds)

        self.routes = routes
        self.key_points = key_points
        self.coord_to_node = coord_to_node

    def explore_route(self, x, y, coord_to_node, routes, key_points, speeds):
    # this method explores the routes starting from a given node. It stores the routes and add the edges and their values in the graph.
        node_from = coord_to_node[str((x,y))]
        for neighbour in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
            if neighbour[0] >=0 and neighbour[0] < self.size_x and neighbour[1] >=0 and neighbour[1] < self.size_y:
                if self.pixels[neighbour[0], neighbour[1]] != (0,0,0):
                    route = [(x,y), neighbour]
                    stop = False
                    cost = 1
                    last = (x, y)
                    current = neighbour
          
                    while speeds[str(self.pixels[current[0],current[1]])] !=1 and stop == False:
                        cost_to_add = 1.0/speeds[str(self.pixels[current[0],current[1]])]
                        #Define whether the route continues, and if so in which direction
                        if current[0] - 1 >= 0 and self.pixels[current[0]-1, current[1]] != (0,0,0) and (current[0]-1, current[1]) != last:
                            last = current
                            current = (current[0]-1, current[1])
                        elif current[0] + 1 < self.size_x and self.pixels[current[0]+1, current[1]] != (0,0,0) and (current[0]+1, current[1]) != last:
                            last = current
                            current = (current[0]+1, current[1])
                        elif current[1] - 1 >= 0 and self.pixels[current[0], current[1]-1] != (0,0,0) and (current[0], current[1]-1) != last:
                            last = current
                            current = (current[0], current[1]-1)
                        elif current[1] + 1 < self.size_y and self.pixels[current[0], current[1]+1] != (0,0,0) and (current[0], current[1]+1) != last:
                            last = current
                            current = (current[0], current[1]+1)
                        else:
                        # the route stops here
                            stop = True
                            
                        if stop == False:
                            cost += cost_to_add
                            self.pixels[last] = (0,0,0)
                            #clear the route so we don't explore it in the other direction
                            route.append(current)

                    if coord_to_node[str(current)] == None:
                    #new node to add
                        n = node(current[0], current[1])
                        node_to = n
                        coord_to_node[str(current)] = node_to

                        if self.pixels[n.x,n.y] == key_points_tuple:
                            #the node is also a start / finish point
                            key_points.append(node_to)

                    index_route = len(routes)
                    routes.append(route)
                    node_to = coord_to_node[str(current)]

                    #adding the links in the graph on both directions (only one if the route is a loop)
                    #the difference of cost may happen when a route ends as the from and to may not have the same associated speed
                    node_from.adj.append((node_to, cost, index_route))
                    if node_to != node_from:
                        node_to.adj.append((node_from, cost - 1 + speeds[str(self.pixels[current[0],current[1]])], index_route))

def generate_speeds(associations):
    d= {}
    for asso in associations:
        r,g,b = asso[0][:2], asso[0][2:4], asso[0][4:]
        d[str((int(r,16), int(g,16), int(b, 16)))] = asso[1]
    return d
