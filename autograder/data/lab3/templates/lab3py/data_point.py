class data_point:

    def __init__(self, labels, values):
        self.data = dict()
        for i, (key, value) in enumerate(zip(labels, values)):
            if i == len(labels):
                break
            self.data[key] = value
        
        self.class_label = labels[-1]
        self.class_value = values[-1]

        self.labels = labels
        self.values = values

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def get_class_label(self):
        return self.class_label
    
    def get_class_value(self):
        return self.class_value
    
    def get_features(self):
        return self.labels[:-1]
    
    def __hash__(self):
        return hash("".join(self.labels + self.values))


class feature_with_IG:
    def __init__(self, feature, IG):
        self.feature = feature
        self.IG = IG

    def __lt__(self, other):
        if other.IG == self.IG:
            return self.feature > other.feature
        return self.IG < other.IG
    

    def __repr__(self):
        return f"IG({self.feature})={self.IG}"


class feature_count:

    def __init__(self, feature_value):
        self.feature_value = feature_value
        self.count = 0
    
    def __hash__(self):
        return hash(self.feature_value)

    def __lt__(self, other):
        if other.count == self.count:
            return self.feature_value > other.feature_value
        return self.count < other.count

class confusion_matrix:

    def __init__(self):
        self.values = set()
        self.matrix = dict()
    
    def add(self, real_value, predicted_value):
        self.values.add(real_value)
        self.values.add(predicted_value)
        if real_value not in self.matrix:
            self.matrix[real_value] = {}
        if predicted_value not in self.matrix[real_value]:
            self.matrix[real_value][predicted_value] = 0
        self.matrix[real_value][predicted_value] += 1
    
    def print(self):
        values_sorted = sorted(list(self.values))
        for value in values_sorted:
            if value not in self.matrix:
                self.matrix[value] = {}
        for real_value in self.matrix:
            for value in values_sorted:
                if value not in self.matrix[real_value]:
                    self.matrix[real_value][value] = 0
        
        print("[CONFUSION_MATRIX]:")
        for real_value in values_sorted:
            for i, predicted_value in enumerate(values_sorted):
                if i != len(values_sorted) - 1:
                    print(self.matrix[real_value][predicted_value], end=" ")
                else:
                    print(self.matrix[real_value][predicted_value])


class feauture_counter_list:

    def __init__(self):
        self.dict = dict()
    
    def add(self, feature_value):
        current_feature = feature_count(feature_value)
        if feature_value not in self.dict:
            self.dict[feature_value] = current_feature
        self.dict[feature_value].count += 1
    
    def get_most_common(self):
        return sorted(list(self.dict.values()))[-1].feature_value


    def items(self):
        return self.dict.items()
    

    def __getitem__(self, key):
        return self.dict[key]
