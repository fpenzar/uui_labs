import sys
from logic import klauzula, logic_tree

RESOLUTION = "resolution"
COOKING = "cooking"

class Parser:

    def __init__(self):
        self.resolution = False
        self.resolution_file = None
        self.cooking = False
        self.cooking_orders = None


    def read_stdin(self):
        for index, arg in enumerate(sys.argv):
            if arg == RESOLUTION:
                self.resolution = True
                self.resolution_file = sys.argv[index + 1]
                break
            elif arg == COOKING:
                self.cooking = True
                self.resolution_file = sys.argv[index + 1]
                self.cooking_orders = sys.argv[index + 2]
                break
    

    def parse(self):
        with open(self.resolution_file, "r") as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
        
        premises = []
        row = 1
        for index, line in enumerate(lines):
            if line.startswith("#"):
                continue
            literals = line.lower().split(" v ")
            clause = klauzula(literals, None, None, row)
            row += 1
            if self.resolution and index == len(lines) - 1:
                self.test_state = clause
                break
            premises.append(clause)
        
        return logic_tree(premises)
    

    def parse_cooking_orders(self):
        orders = []
        with open(self.cooking_orders, "r") as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
        
        for line in lines:
            if line.startswith("#"):
                continue
            command = line[-1]
            line = line[:-2]
            literals = line.lower().split(" v ")
            clause = klauzula(literals, None, None)
            orders.append((clause, command))
        return orders

    