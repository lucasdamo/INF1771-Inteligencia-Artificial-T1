import pathlib
from controllers import Map

class Node:
    def __init__(self, coordinates, node_weight:int, parent):
        self.coordinates = coordinates
        self.node_weight = node_weight
        self.total_path_cost = node_weight
        self.estimated_cost = self.total_path_cost
        self.parent_node = parent   # Armazena o pai para poder montar o caminho ao terminar!

    def __eq__(self,another):
        return self.coordinates == another.coordinates

    def __lt__(self, another):
        return self.estimated_cost < another.estimated_cost

    def __repr__(self):
        return ('[{0},{1},{2}]'.format(self.coordinates,self.node_weight,self.total_path_cost))



def Astar(map:Map):
    start = Node(map.start_point,1, None)
    end = Node(map.final_point,1, None)

    priority_queue = []
    closed_nodes = []

    path = []

    priority_queue.append(start)
    while priority_queue:
        priority_queue.sort()
        working_node = priority_queue.pop(0)
        closed_nodes.append(working_node)
        if working_node == end:
            path.append(working_node)
            while working_node.parent_node is not None:
                path.append(working_node.parent_node)
                working_node = working_node.parent_node
            return path
        
        x,y = working_node.coordinates
        neighbours_coords = []
        if x+1 < map.xlen:
            neighbours_coords.append((x+1,y))
        if y+1 < map.ylen:
            neighbours_coords.append((x, y+1))
        if x-1 >= 0:
            neighbours_coords.append((x-1, y))
        if y-1 >= 0:
            neighbours_coords.append((x, y-1))

        for n_coord in neighbours_coords:
            neighbor_node = Node(n_coord, map.get_node_weight(n_coord), working_node)
            if neighbor_node in closed_nodes:
                continue
            neighbor_node.total_path_cost = working_node.total_path_cost + neighbor_node.node_weight 
            neighbor_node.estimated_cost = neighbor_node.total_path_cost + map.get_heuristic_weight(neighbor_node.coordinates)
            
            #add neighbor in priority queue if it was not visited before or has lower heuristic value than previous instance
            if(valid_new_open_node(priority_queue, neighbor_node)):
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
        
input_path = pathlib.Path(__file__).parents[1].joinpath('input')
m = Map(input_path.joinpath('map.csv'), input_path.joinpath('cellweights.csv'))
Astar(m)
