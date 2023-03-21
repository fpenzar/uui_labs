class State:

    def __init__(self, name, cost):
        self.name = name
        self.cost = cost
    

    def __lt__(self, other):
        return self.name < other.name
    

    def __repr__(self):
        return f"<{self.name}: {self.cost}>"


    def __str__(self):
        return f"<{self.name}: {self.cost}>"
