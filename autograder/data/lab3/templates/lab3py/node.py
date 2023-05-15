import copy

class Node:
    
    def __init__(self, feature):
        self.subtree = dict()
        self.feature = feature
    

    def add_subtree(self, subtree, value):
        self.subtree[value] = subtree
    

    def __getitem__(self, key):
        return self.subtree[key]


    def is_leaf(self):
        if len(self.subtree) == 0:
            return True
        return False


    def print(self, i=0, to_print=""):
        i += 1
        if self.is_leaf():
            print(f"{to_print} {self.feature}")
            return
        for key, value in self.subtree.items():
            new_print = to_print + f"{i}:{self.feature}={key} "
            value.print(i, new_print)

