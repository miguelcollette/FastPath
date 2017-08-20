# FastPath
Fastest Path in a transport network from an image of the network.

# Route finding

The challenge is to find a route between two points in a city. For each route we are provided with an image of the public transport map that is colour-coded according to the speed of the routes:

| RGB Hex Code    | Speed   | Designation           |
|:---------------:|--------:|-----------------------|
| 0x000000        | 0       | No road               |
| 0xffffff        | 1       | Junction              |
| 0xb03a2e        | 2       | Footpath              |
| 0x6c3483        | 3       | Lane                  |
| 0x2874a6        | 5       | Single Carriage way   |
| 0x117565        | 10      | Dual Carriage way     |
| 0x239b56        | 15      | Motorway              |
| 0xd4ac0d        | 20      | Highspeed rail        |
| 0xd35400        | 1       | Start / finish        |

The start and finish points are labelled in the same way - it does not matter in which direction the route is travelled. The speed of each segment indicates the time taken to travel over one unit length of the route - so the total time between two junctions is equal to the length of the route (in pixels) multiplied by the speed.

For each input map we should produce an image of the same size whose pixels are black everywhere except for the route between start and finish which should be white.

we are provided with 11 maps. map_0000.png to map_0009.png are for small towns. map_0010.png is a special case and represents a very large transport network.


# My solution - in Python

## Version and installation

I coded and ran my solution in Python 3.6

The zip file contains the source code the data and an empty results folder in which the output images will be stored.
Extract the content of the zip file in the location of your choice. Make sure you run or install python 3.6.

To extract the data from the images I used PIL. Which is a Python library that you need to install.

'pip install pillow'

## Execution

Once this is done you are up and running. All you need to do is go to the folder were you extracted the zip file.

'cd /yourpath/route_planning_miguel'

And then run path_finding.py.  Two options here :

* If you run without arguments, it will process all the images in the data folder (make sure only images are in this folder)

'python path_finding.py'

* You can add one or several file names (with extension) and it will fetch and process the given images in the data folder

'python path_finding.py myimage1.png myimage2.png'

You can see the results in the results folder. The file are named after the original image name with the prefix "path_".


## How is the solution designed

### Build a graph from the image matrix

By parsing the image RGB matrix we look for the nodes of our graph, they are the intersections, the start / finish points, and the end of routes.
When we come across an intersection or a finish / end point, we will explore all the routes starting from this point, to the next intersections, start / finish point or end of route.
Then we can add the corresponding nodes to the adjacency list of the first one and vice versa. We keep a list of the routes and the coordinates of the pixels forming them.
Thus the adjacency lists have the next nodes along with the cost to reach it and the route. The cost in our case is the time, obtained thanks to the speed on the given route and the length of that route.
Note that with this design it would be possible to have several speeds on the same route: for example a simple carriage way becoming a single carriage way without any intersection.
As we build the graph we make a dictionary that maps the coordinates of a node to the node object.

So at the end we have a graph defined by:

*a adjacency dictionary: keys being the node object and values being the adjacency lists of those nodes
*A dictionary that maps the coordinates of a pixel to the associated node, if any
*a list of the routes with for each route, all the pixels that are on this route
*the key points: Start / finish points

### Run A* algorithm on this graph from one key point to the other.

I decided to use A* algorithm for this problem to optimise the time to reach the destination.
As we know the destination coordinates we can push the research towards it with a good heuristic.
I used the time to travel the Manhattan distance at the maximum possible speed (20 here).
This heuristic never overestimates the cost, and is I believe the most accurate we can get without extra processing.
Thus A* is sure to return the optimal solutions, or one of them if several have the same cost, and quickly as we have a good heuristic.
I make sure to be able to backtrack the path A* is building and create a new image with the corresponding pixels white.
The start / finish points are kept in their original colour.

### Notes

As the problem was defined it was not mandatory to build the graph as the image corresponds to one query. 
Running A* directly on the RGB matrix would have probably been reasonably fast.
But in practice one transport network is being used by a lot of people so it makes sense to build the graph from it as a preprocessing.
Then the start / finish points could be added with the particular queries.
That's also why I clear the path finding related information after the output route is defined, so the nodes are ready for the next query.
Also the heuristic could be easily switched to Euclidean distance instead of Manhattan distance if we considered diagonal routes.
Finally, it would be reasonably easy to add routes, nodes and update the graph from the existing network.

The solution I proposed works for all the given input images, including the largest network.
For even bigger network, I think the most time consuming task is to build the graph, then A* is probably one of the fastest solutions to find the path.
One thing to consider would be to take into account the number of different modes of transportations, the walking time etc.
With a multicriteria approach A* is much less straight forward and it would not be trivial to choose only one path and in an acceptable time.
Also the feasibility of some solutions could be discuss: some roads must not be served by public transport, so is it possible to take a car, then a train then again a car?
All those further concerns could be considered when going further in dealing with this problem.
