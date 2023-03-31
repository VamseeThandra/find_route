import sys

# Constants
INFORMED = 1
UNIFORMED = 0

def ReadDataFromFile(filename):
    data = []
    for line in open(filename,"r").readlines():
        if( "END OF INPUT" in line ):
            break
        line_data = line.split()
        data.append(line_data)

    return data

def FindHeuristicDistanceOfGivenNode(node):
    for line in heuristic_data:
        if node in line:
            return int(line[1])

def PrintRoute(route):
    route_length = len(route)-1
    for i in range(route_length):
        for data in distances_data:
            if ((route[i] in data) and (route[i+1] in data)):
                print("{} to {}, {} Km".format(route[i],route[i+1],float(data[2])))

def InformedSearch():
    Search(INFORMED)

def UniformedSearch():
    Search(UNIFORMED)

def Search(isHeuristicGiven):

    # A* Logic
    nodes_popped = 0
    nodes_generated = 1
    nodes_expanded = 0
    max_nodes_in_memory = -9999   # Some small value
    visited = []
    fringe = [{
     'node' : start_location,
     'route' : [start_location] ,
     'distance_travelled' : 0,
     'heuristic_distance' : FindHeuristicDistanceOfGivenNode(start_location) if (isHeuristicGiven==1) else 0
    }]

    counter = 0

    while (True):

        if(fringe == []):
            print("Nodes Popped: ",nodes_popped)
            print("Nodes Expanded: {}".format(len(visited)))
            print('Nodes generated: {}'.format(nodes_generated))
            # print("Max nodes in memory: {}".format(max_nodes_in_memory))
            print("Distance: infinity")
            print("Route: None")

            exit()
        temp_node = fringe.pop(0)
        nodes_popped +=1
        node_to_be_expanded = temp_node['node']
        if(node_to_be_expanded not in visited):
            visited.append(node_to_be_expanded)
        else:
            nodes_expanded+=1
            continue
        if(node_to_be_expanded == destination_location):
            nodes_expanded+=1
            break
    
        for data in distances_data:
            if node_to_be_expanded in data:
                neighbour = data[1] if (data.index(node_to_be_expanded) == 0) else data[0]
                neighbour_distance_travelled = int(temp_node['distance_travelled'])+int(data[2])
                prev_route = temp_node['route'].copy()
                prev_route.append(neighbour)
                fringe.append({
                'node': neighbour,
                'route': prev_route,
                'distance_travelled': neighbour_distance_travelled,
                'heuristic_distance': (neighbour_distance_travelled + FindHeuristicDistanceOfGivenNode(neighbour)) if (isHeuristicGiven==1) else 0
                })
                nodes_generated+=1

            else:
                continue
        filter = 'heuristic_distance' if (isHeuristicGiven==1) else 'distance_travelled'
        fringe = sorted(fringe, key = lambda x: x[filter])   # Sorting the fringe

        if(len(fringe)>max_nodes_in_memory):
            max_nodes_in_memory=len(fringe)
        nodes_expanded+=1
        
    print("Nodes Popped: ",nodes_popped)
    print("Nodes Expanded: {}".format(len(visited)-1))
    print("Nodes Generated: {}".format(nodes_generated))
    # print("Max nodes in memory: {}".format(max_nodes_in_memory))
    print("Distance: {} km".format(float(temp_node['distance_travelled'])))
    print("Route: ")
    PrintRoute(temp_node['route'])


input_filename = sys.argv[1]
start_location = sys.argv[2]
destination_location = sys.argv[3]

# Read data about distances between different cities
distances_data = ReadDataFromFile(input_filename)

if(len(sys.argv)==5):
    heuristic_filename = sys.argv[4]
    heuristic_data = ReadDataFromFile(heuristic_filename)
    InformedSearch()
elif(len(sys.argv) == 4):
    UniformedSearch()