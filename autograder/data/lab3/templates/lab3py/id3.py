from node import Node
from data_point import feauture_counter_list
import copy

class ID3:

    def __init__(self, depth=None):
        self.max_depth = depth
        self.tree = None
    

    def fit(self, train_dataset):
        features = train_dataset[0].get_features()
        class_label = train_dataset[0].get_class_label()
        self.root_node = self.id3(train_dataset, train_dataset, features, class_label, 1)
        print("[BRANCHES]")
        self.root_node.print()
    

    def predict(self, test_dataset):
        ...
    

    def most_common_feature_value(self, D, feature):
        f_ctr_list = self.count_feature_values(D, feature)
        return f_ctr_list.get_most_common()


    def count_feature_values(self, D, feature):
        f_ctr_list = feauture_counter_list()
        for data_point in D:
            f_ctr_list.add(data_point[feature])
        return f_ctr_list
    

    def IG(self, D, features):
        # test
        return features[0]
    

    def get_unique_values_for_feature(self, D, feature):
        unique_values = []
        for data_point in D:
            if data_point[feature] not in unique_values:
                unique_values.append(data_point[feature])
        return unique_values
    

    def get_D_with_given_feature_value(self, D, feature, feature_value):
        output = []
        for data_point in D:
            if data_point[feature] == feature_value:
                output.append(data_point)
        return output

    
    def id3(self, D, D_parent, features, class_label, depth):
        depth_limit_reached = False
        if self.max_depth is not None:
            if self.max_depth < depth:
                depth_limit_reached = True
        if len(D) == 0 or depth_limit_reached:
            most_common_class_value = self.most_common_feature_value(D_parent, class_label)
            return Node(most_common_class_value)
        
        most_common_class_value = self.most_common_feature_value(D, class_label)
        D_with_most_common_class_value = self.get_D_with_given_feature_value(D, class_label, most_common_class_value)
        if features is None or len(features) == 0 or \
           (set(D_with_most_common_class_value) == set(D_parent) and len(D_with_most_common_class_value) == len(D_parent)):
            return Node(most_common_class_value)
        
        most_discriminative_feature = self.IG(D, features)
        current_node = Node(most_discriminative_feature)
        for feature_value in self.get_unique_values_for_feature(D, most_discriminative_feature):
            updated_features = copy.copy(features)
            updated_features.remove(most_discriminative_feature)
            subtree = self.id3(self.get_D_with_given_feature_value(D, most_discriminative_feature, feature_value), 
                            copy.deepcopy(D), updated_features, class_label, depth + 1)
            current_node.add_subtree(subtree, feature_value)
        return current_node
    

