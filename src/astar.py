import pathlib
from controllers import Map

class Node:
    def __init__(self, coordinates, node_weight:int, estimated_cost ,parent):
        self.coordinates = coordinates
        self.node_weight = node_weight
        self.total_path_cost = node_weight
        self.estimated_cost = self.total_path_cost + estimated_cost
        self.parent_node = parent   #stores the parent to build the path

    def __eq__(self,another):
        return self.coordinates == another.coordinates

    def __lt__(self, another):
        return self.estimated_cost < another.estimated_cost

    def __repr__(self):
        return ('[{0},{1},{2}]'.format(self.coordinates,self.node_weight,self.total_path_cost))

class Astar:
    def __init__(self,map : Map):
        self.map = map
        self.start = Node(map.start_point,1,self.map.get_heuristic_weight(map.start_point), None)
        self.end = Node(map.final_point,1,self.map.get_heuristic_weight(map.final_point), None)
        self.priority_queue = []
        self.closed_nodes = []
        self.path = []
        self.over = False
        self.steps = 0
        
        self.priority_queue.append(self.start)

    def solve(self): #solves the algorithm by calling 'advance' method with a very large number until it's done
        steps = 1000
        while not self.over:
            self.advance(steps)
            steps = steps * 1000 #calling in multiples for log n time where 'n' is number of total steps remaining

    def advance(self,steps): #advances the algorithm by the amount of steps provided
        while self.priority_queue and steps > 0 and not self.over:
            self.priority_queue.sort()
            working_node = self.priority_queue.pop(0)
            self.closed_nodes.append(working_node)
            if working_node == self.end:
                self.over = True
                self.path = []
                self.path.append(invert_coordinates(working_node.coordinates))
                while working_node.parent_node is not None:
                    self.path.append(invert_coordinates(working_node.parent_node.coordinates))
                    working_node = working_node.parent_node
                return
            x,y = working_node.coordinates
            neighbours_coords = []
            if x+1 < self.map.xlen:
                neighbours_coords.append((x+1,y))
            if y+1 < self.map.ylen:
                neighbours_coords.append((x, y+1))
            if x-1 >= 0:
                neighbours_coords.append((x-1, y))
            if y-1 >= 0:
                neighbours_coords.append((x, y-1))

            #expand on each neighbor
            for n_coord in neighbours_coords:
                node_weight_var = self.map.get_node_weight(n_coord)
                neighbor_node = Node(n_coord,node_weight_var,self.map.get_heuristic_weight(n_coord) ,working_node)
                if neighbor_node in self.closed_nodes:
                    continue #if neighbour has already been analysed
                neighbor_node.total_path_cost = working_node.total_path_cost + neighbor_node.node_weight 
                neighbor_node.estimated_cost = neighbor_node.total_path_cost + self.map.get_heuristic_weight(neighbor_node.coordinates)
                #add neighbor in priority queue if it was not visited before or has lower heuristic value than it's previous instance
                if(valid_new_open_node(self.priority_queue, neighbor_node)):
                    self.priority_queue.append(neighbor_node)
            self.steps = self.steps + 1
            steps -= 1
        return
    def get_visual_elements(self):
        path = self.get_best_path()
        open_nodes = self.get_all_open_nodes()
        closed_nodes = self.get_all_closed_nodes()
        return path,open_nodes,closed_nodes


    def get_best_path(self): #returns the current best path found
        if not self.over: 
            self.path = []
            working_node = self.priority_queue[0]
            self.path.append(invert_coordinates(working_node.coordinates))
            while working_node.parent_node is not None:
                self.path.append(invert_coordinates(working_node.parent_node.coordinates))
                working_node = working_node.parent_node    
        return self.path
    
    def get_all_open_nodes(self): #returns all open nodes not in path
        open_nodes = []
        for node in self.priority_queue:
            node_coordinates_fixed = invert_coordinates(node.coordinates)
            if node_coordinates_fixed not in self.path:
                open_nodes.append(node_coordinates_fixed)
        return open_nodes
    
    def get_all_closed_nodes(self): #returns all closed nodes not in path
        closed_nodes = []
        for node in self.closed_nodes:
            node_coordinates_fixed = invert_coordinates(node.coordinates)
            if node_coordinates_fixed not in self.path:
                closed_nodes.append(node_coordinates_fixed)
        return closed_nodes

def invert_coordinates(c):
    return [c[1],c[0]]


def valid_new_open_node(priority_queue, neighbor_node):
    for n in priority_queue:
        if (neighbor_node == n):
            if (neighbor_node.total_path_cost >= n.total_path_cost):
                return False
    return True

'''    
input_path = pathlib.Path(__file__).parents[1].joinpath('input')
m = Map(input_path.joinpath('map.csv'), input_path.joinpath('cellweights.csv'))
result = Astar(m)
result.solve()
'''