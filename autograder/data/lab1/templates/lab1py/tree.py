from graph import Graph
from node import Node
import bisect


class Tree:

    def __init__(self, graph: Graph):
        self.graph = graph
        self.solution = None
        self.algorithms = {
            "bfs": self.bfs,
            "ucs": self.ucs,
            "astar": self.a_star
        }
    

    def found_solution(self):
        if self.solution:
            return "yes"
        return "no"


    def get_algorithm_name(self):
        if self.algorithm == "bfs":
            return "BFS"
        elif self.algorithm == "ucs":
            return "UCS"
        elif self.algorithm == "astar":
            return f"A-STAR {self.graph.heuristics_path}"
    

    def print(self):
        print(f"# {self.get_algorithm_name()}")
        print(f"[FOUND_SOLUTION]: {self.found_solution()}")
        if not self.solution:
            return
        print(f"[STATES_VISITED]: {len(self.closed)}")
        print(f"[PATH_LENGTH]: {self.solution.depth + 1}")
        total_cost = "{:.1f}".format(self.solution.cost)
        print(f"[TOTAL_COST]: {total_cost}")
        print(f"[PATH]: {self.get_path()}")
    

    def get_path(self):
        path = []
        node = self.solution
        while node.parent:
            path.insert(0, node.name)
            node = node.parent
        path.insert(0, node.name)
        return " => ".join(path)
    

    def run_algorithm(self, algorithm):
        self.algorithm = algorithm
        return self.algorithms[algorithm]()
    

    def bfs(self):
        start_state = self.graph.get_start()
        start_node = Node(start_state, depth=0, parent=None, cost=0)
        open = [start_node]
        self.closed = {}
        while len(open):
            current_node = open.pop(0)
            # skip state if already closed
            if current_node.name in self.closed:
                continue
            # add state to closed
            self.closed.update({current_node.name, current_node.cost})
            # check if the current node is the solution
            if self.graph.goal(current_node.name):
                self.solution = current_node
                return True
            # iterate over children
            for child in self.graph.expand(current_node.name):
                new_node = Node(child.name, depth=current_node.depth+1, 
                                parent=current_node, cost=current_node.cost+child.cost)
                # insert into open
                open.append(new_node)
        return False
    

    def ucs(self):
        start_state = self.graph.get_start()
        start_node = Node(start_state, depth=0, parent=None, cost=0)
        open = [start_node]
        self.closed = {}
        while len(open):
            current_node = open.pop(0)
            # skip state if already closed
            if current_node.name in self.closed:
                continue
            # add state to closed
            self.closed.update({current_node.name, current_node.cost})
            # check if the current node is the solution
            if self.graph.goal(current_node.name):
                self.solution = current_node
                return True
            # iterate over children
            for child in self.graph.expand(current_node.name):
                new_node = Node(child.name, depth=current_node.depth+1, 
                                parent=current_node, cost=current_node.cost+child.cost)
                # insert sorted by cost, then name
                bisect.insort(open, new_node)
        return False
    

    def a_star(self):
        start_state = self.graph.get_start()
        start_node = Node(start_state, depth=0, parent=None, cost=0, astar=True, heuristic=self.graph.get_heuristic(start_state))
        open = [start_node]
        self.closed = dict()
        open_map = {start_node.name: start_node.cost} # used for hashing for speed
        while len(open):
            current_node = open.pop(0)
            # remove from open_map
            del open_map[current_node.name]
        
            # add state to closed
            self.closed.update({current_node.name: current_node.cost})
            # check if the current node is the solution
            if self.graph.goal(current_node.name):
                self.solution = current_node
                return True
            
            # iterate over children
            for child in self.graph.expand(current_node.name):
                cost = current_node.cost + child.cost
                # check if already in open
                if child.name in open_map:
                    if open_map[child.name] < cost:
                        continue
                    else:
                        del open_map[child.name]
                # check if already in closed
                elif child.name in self.closed:
                    if self.closed[child.name] < cost:
                        continue
                    else:
                        del self.closed[child.name]
                
                new_node = Node(child.name, depth=current_node.depth+1, 
                                parent=current_node, cost=cost, astar=True, heuristic=self.graph.get_heuristic(child.name))
                # insert sorted by cost, then name
                bisect.insort(open, new_node)
                open_map.update({new_node.name: new_node.cost})
        return False