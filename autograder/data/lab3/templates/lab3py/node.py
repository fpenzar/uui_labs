from data_point import data_point

class Node:
    
    def __init__(self, feature, default_value):
        self.subtree = dict()
        self.feature = feature
        self.default_value = default_value
    

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
            print(f"{to_print}{self.feature}")
            return
        for key, value in self.subtree.items():
            new_print = to_print + f"{i}:{self.feature}={key} "
            value.print(i, new_print)
    

    def validate(self, data_point: data_point):
        if self.is_leaf():
            return self.feature
        
        if data_point[self.feature] not in self.subtree:
            return self.default_value
        
        return self.subtree[data_point[self.feature]].validate(data_point)
