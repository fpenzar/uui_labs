from state import State
import bisect


class Graph:

    def __init__(self):
        self.states = {}
        self.heuristics = {}
        self.goal_states = set()


    def add_state(self, state: str):
        self.states.update({state: []})
    

    def add_child_to_state(self, parent: str, child_name: str, cost: float):
        child = State(child_name, cost)
        # insert sorted by name
        bisect.insort(self.states[parent], child)
    

    def get_heuristic(self, state: str):
        return self.heuristics[state]
    

    def add_heuristics(self, path: str):
        self.heuristics_path = path
        if not path:
            return
        
        with open(path, "r") as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
        for line in lines:
            parsed = line.split(": ")
            state = parsed[0]
            heuristic = float(parsed[1])
            self.heuristics.update({state: heuristic})
    

    def expand(self, parent_name: str):
        return self.states[parent_name]


    def goal(self, state: str):
        return state in self.goal_states


    def add_goal_state(self, state: str):
        self.goal_states.add(state)
    

    def add_start(self, state: str):
        self.start = state
    

    def get_start(self):
        return self.start
