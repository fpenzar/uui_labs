class Node:

    def __init__(self, name, depth, parent, cost, astar=False, heuristic=0):
        self.name = name
        self.depth = depth
        self.parent = parent
        self.cost = cost
        self.astar = astar
        self.heuristic = heuristic
        self.f = self.cost + self.heuristic


    def __lt__(self, other):
        # logic for when astar is used
        if self.astar:
            if self.f == other.f:
                return self.name < other.name
            return self.f < other.f
        
        # logic for ucs
        if self.cost == other.cost:
            return self.name < other.name
        return self.cost < other.cost


    def __gt__(self, other):
        return self.cost > other.cost
    

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"<{self.name}: {self.cost}>"
    
    def __str__(self):
        return f"<{self.name}: {self.cost}>"
