class Node:
    def __init__(self, coordinates:tuple[int, int], node_weight:int, parent_node):
        self.coordinates = coordinates
        self.parent_node = parent_node
        self.node_weight = node_weight

        self.start_distance = 0
        self.end_distance = 0
        self.total_path_cost = node_weight

    def __eq__(self,another):
        return self.coordinates == another.coordinates

    def __lt__(self, another):
        return self.total_path_cost < another.total_path_cost

    def __repr__(self):
        return ('[{0},{1},{1}]'.format(self.coordinates,self.node_weight,self.total_path_cost))

    def distance_to(self, another):
        x1,y1 = self.coordinates
        x2,y2 = another.coordinates
        
        return abs(x2-x1) + abs(y2-y1)


def Astar(map):

    start = Node(map.get_starting_point(),1,None)

    end = Node(map.get_final_point(),1,None)

    priority_queue = []

    closed_nodes = []

    path = []

    priority_queue.append(start)

    while priority_queue:

        priority_queue.sort()

        working_node = priority_queue.pop(0)

        closed_nodes.append(working_node)

        x,y = working_node.coordinates

        neighbors_coordinates = [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]

        for n_coord in neighbors_coordinates:
            #create neighbor node with parent as current
            neighbor_node = Node(n_coord, map.get_node_weight(n_coord) , working_node)
            #calculate manhatan heuristic
            neighbor_node.start_distance = neighbor_node.distance_to(start)
            neighbor_node.end_distance = neighbor_node.distance_to(end)
            #adds to total cost of path the distance and time consumed by previous node + this nodes estimated distance cost 
            neighbor_node.total_path_cost = working_node.total_path_cost + neighbor_node.end_distance
            
            #add neighbor in priority queue if it was not visited before or has lower heuristic value than previous instance
            if(valid_new_open_node(priority_queue,neighbor_node)):
                priority_queue.append(neighbor_node)



    return None


def valid_new_open_node(priority_queue, neighbor_node):
    for n in priority_queue:
        if (neighbor_node == n):
            if (neighbor_node.total_path_cost >= n.total_path_cost):
                return False
            else:
                return True
    return True
        