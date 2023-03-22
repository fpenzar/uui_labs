from heapq import heappop, heappush
from graph import Graph
from node import Node


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
            self.closed.update({current_node.name: current_node.cost})
            # check if the current node is the solution
            if self.graph.goal(current_node.name):
                self.solution = current_node
                return True
            # iterate over children
            for child in self.graph.expand(current_node.name):
                # skip state if already closed
                if child.name in self.closed:
                    continue
                new_node = Node(child.name, depth=current_node.depth+1, 
                                parent=current_node, cost=current_node.cost+child.cost)
                # insert into open
                open.append(new_node)
        return False
    

    # this is used in generating h* for checking consistency
    def ucs(self, start_state=None, goal_states=None, expand_function=None):
        if start_state is None:
            start_state = self.graph.get_start()
        if goal_states is None:
            goal_states = self.graph.goal_states
        if expand_function is None:
            expand_function = self.graph.expand
        
        start_node = Node(start_state, depth=0, parent=None, cost=0)
        open = [start_node]
        self.closed = {}
        while len(open):
            current_node = heappop(open)
            # skip state if already closed
            if current_node.name in self.closed:
                continue
            # add state to closed
            self.closed.update({current_node.name: current_node.cost})
            # check if the current node is the solution
            if current_node.name in goal_states:
                self.solution = current_node
                return True
            # iterate over children
            for child in expand_function(current_node.name):
                # skip state if already closed
                if child.name in self.closed:
                    continue
                new_node = Node(child.name, depth=current_node.depth+1, 
                                parent=current_node, cost=current_node.cost+child.cost)
                # insert sorted by cost, then name
                heappush(open, new_node)
        return None
    

    def a_star(self):
        start_state = self.graph.get_start()
        start_node = Node(start_state, depth=0, parent=None, cost=0, astar=True, 
                          heuristic=self.graph.get_heuristic(start_state))
        open = [start_node]
        self.closed = dict()
        open_map = {start_node.name: start_node.cost} # used for hashing for speed
        while len(open):
            current_node = heappop(open)
            # skip state if already closed
            if current_node.name in self.closed:
                continue
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
                                parent=current_node, cost=cost, astar=True, 
                                heuristic=self.graph.get_heuristic(child.name))
                # insert sorted by cost, then name
                heappush(open, new_node)
                open_map.update({new_node.name: new_node.cost})
        return False
    

    def check_consistency(self):
        print(f"# HEURISTIC-CONSISTENT {self.graph.heuristics_path}")
        # flag to keep track if the heuristic is consistent
        consistent = True
        for state, children in self.graph.get_all_states().items():
            h_state = self.graph.get_heuristic(state)
            for child in children:
                h_child = self.graph.get_heuristic(child.name)
                cost_and_h_child = h_child + child.cost
                if h_state <= cost_and_h_child:
                    condition = "[OK]"
                else:
                    condition = "[ERR]"
                    consistent = False
                h_formated = "{:.1f}".format(h_state)
                h_child_formated = "{:.1f}".format(h_child)
                child_cost_formated = "{:.1f}".format(child.cost)
                print(f"[CONDITION]: {condition} h({state}) <= h({child.name}) + c: {h_formated} <= {h_child_formated} + {child_cost_formated}")
        if consistent:
            conclusion = "consistent"
        else:
            conclusion = "not consistent"
        print(f"[CONCLUSION]: Heuristic is {conclusion}.")
    

    def generate_h_star(self):
        # initialize all values to inf (as if the states were not connected)
        self.h_star = {state: float("inf") for state in self.graph.get_all_states()}

        # start from each goal state
        for goal_state in self.graph.goal_states:
            # run ucs from each goal state (withohut end states to run it on the whole graph)
            self.ucs(start_state=goal_state, goal_states=[], expand_function=self.graph.expand_reverse)
            # the results for the whole graph are in self.closed
            for closed_state, value in self.closed.items():
                # update the self.h_star values
                if value < self.h_star[closed_state]:
                    self.h_star[closed_state] = value
    

    def check_optimistic(self):
        print(f"# HEURISTIC-OPTIMISTIC {self.graph.heuristics_path}")
        # generate h_star values for the graph
        self.generate_h_star()
        # flag to keep track if the heuristic is optimistic
        optimistic = True
        for state in self.graph.get_all_states():
            h = self.graph.get_heuristic(state)
            h_star = self.h_star[state]
            if h <= h_star:
                condition = "[OK]"
            else:
                condition = "[ERR]"
                optimistic = False
            h_formated = "{:.1f}".format(h)
            h_star_formated = "{:.1f}".format(h_star)
            print(f"[CONDITION]: {condition} h({state}) <= h*: {h_formated} <= {h_star_formated}")
        if optimistic:
            conclusion = "optimistic"
        else:
            conclusion = "not optimistic"
        print(f"[CONCLUSION]: Heuristic is {conclusion}.")
