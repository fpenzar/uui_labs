import sys
from graph import Graph
#from node import Node, Graph

SS_FLAG = "--ss"
ALG_FLAG = "--alg"
H_FLAG = "--h"
CHECK_OPT_FLAG = "--check-optimistic"
CHECK_CONSIST_FLAG = "--check-consistent"

class Parser:

    def __init__(self):
        self.check_consistency = False
        self.check_optimistic = False
        self.ss_path = None
        self.algorithm = None
        self.heuristics_path = None


    def read_stdin(self):
        for index, arg in enumerate(sys.argv):
            if arg == SS_FLAG:
                self.ss_path = sys.argv[index + 1]
            elif arg == ALG_FLAG:
                self.algorithm = sys.argv[index + 1]
            elif arg == H_FLAG:
                self.heuristics_path = sys.argv[index + 1]
            elif arg == CHECK_OPT_FLAG:
                self.check_optimistic = True
            elif arg == CHECK_CONSIST_FLAG:
                self.check_consistency = True
    

    def get_heuristics_path(self):
        return self.heuristics_path
    

    def get_algorithm(self):
        return self.algorithm
    

    def parse(self):
        graph = Graph()

        with open(self.ss_path, "r") as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
        
        start_state_processed = False
        end_states_processed = False
        for index, line in enumerate(lines):
            if line.startswith("#"):
                continue
            # starting state
            if not start_state_processed:
                graph.add_start(line)
                start_state_processed = True
                continue

            # end states
            if not end_states_processed:
                end_nodes = line.split()
                for end_node_name in end_nodes:
                    graph.add_goal_state(end_node_name)
                end_states_processed = True
                continue

            # add child nodes
            line_parsed = line.split(":")
            name = line_parsed[0]
            graph.add_state(name)
            for name_and_cost in line_parsed[1].split():
                child_name = name_and_cost.split(",")[0]
                child_cost = float(name_and_cost.split(",")[1])
                graph.add_child_to_state(name, child_name, child_cost)
        
        return graph
    