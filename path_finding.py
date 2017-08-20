import sys
from node import *
from network import *
from bisect import insort_left

def routes_res(n):
    routes = []
    current = n
    while current.n_from:
        routes.append(current.r_from)
        current = current.n_from
    return routes

def a_star(node_from, node_to, speeds):
#A* algorithm implemented. The heuristic used is the Manhattan distance divided by the speed.
#the heuristic being optimistic we are guaranteed to find the fastest route (or one of them if several)
    max_speed = max(speeds.values())
    opened = [node_from]
    closed = []
    while opened != []:
        current = opened.pop()
        if current == node_to:
            return routes_res(current)
        else:
            for neighbour in current.adj:
                n = neighbour[0]
                if not n.in_closed:
                    new_cost = current.c + neighbour[1]
                    new_estim = n.manhattan_distance(node_to) / max_speed
                    new_f = new_cost + new_estim
                    c = n.c
                    h = n.h
                    f = c+h
                    if not n.in_opened:
                    #enter the values of c, h, the route and node we come from, and add n to the opened list
                        n.c = new_cost
                        n.h = new_estim
                        n.n_from = current
                        n.r_from = neighbour[2]
                        insort_left(opened, n)
                        n.in_opened = True
                    elif f>new_f or (f == new_f and c<new_cost):
                    #update the values, and reposition the node at the right index in the list
                        opened.remove(n)
                        n.c = new_cost
                        n.h = new_estim
                        n.n_from = current
                        n.r_from = neighbour[2]
                        insort_left(opened, n)
            closed.append(current)
            current.in_closed = True
    print("here")
    return []

if __name__ == '__main__':
    associations = [('000000', 0.0), ('ffffff', 1.0), ('b03a2e', 2.0), ('6c3483', 3.0), ('2874a6 ', 5.0), ('117565', 10.0), ('239b56', 15.0), ('d4ac0d', 20.0), ('d35400', 1.0)]
    speeds = generate_speeds(associations)
  
    if len(sys.argv) == 1:
        image_list = ['map_00010.png', 'map_00009.png','map_00008.png','map_00007.png','map_00006.png','map_00005.png','map_00004.png','map_00003.png','map_00002.png','map_00001.png', 'map_00000.png']
    else:
        image_list = sys.argv[1:]
    #The user did not provide an image name to deal with, we will process all the images in data
    for image in image_list:
        test = network("./data/"+image)
        test.build_network_graph(speeds)
        route = a_star(test.key_points[0], test.key_points[1], speeds)
        test.create_res_image(route)
        test.clear_path_data()

  
  
                
        