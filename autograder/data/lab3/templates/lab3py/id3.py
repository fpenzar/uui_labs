from node import Node
from data_point import feauture_counter_list, feature_with_IG, confusion_matrix
import copy
from math import log2

class ID3:

    def __init__(self, depth=None):
        self.max_depth = depth
        self.tree = None
    

    def fit(self, train_dataset):
        features = train_dataset[0].get_features()
        self.class_label = train_dataset[0].get_class_label()
        self.root_node = self.id3(train_dataset, train_dataset, features, self.class_label, 1)
        print("[BRANCHES]:")
        self.root_node.print()
    

    def predict(self, test_dataset):
        correct = 0
        to_print = "[PREDICTIONS]:"
        conf_matrix = confusion_matrix()
        for data_point in test_dataset:
            predicet_class_value = self.root_node.validate(data_point)
            conf_matrix.add(data_point.class_value, predicet_class_value)
            if data_point.class_value == predicet_class_value:
                correct += 1
            to_print += " " + predicet_class_value
        print(to_print)
        accuracy = round(correct/len(test_dataset), 5)
        accuracy_str = "{0:.5f}".format(accuracy)
        print(f"[ACCURACY]: {accuracy_str}")
        conf_matrix.print()


    def most_common_feature_value(self, D, feature):
        f_ctr_list = self.count_feature_values(D, feature)
        return f_ctr_list.get_most_common()


    def count_feature_values(self, D, feature):
        f_ctr_list = feauture_counter_list()
        for data_point in D:
            f_ctr_list.add(data_point[feature])
        return f_ctr_list


    def entropy(self, D, feature, feature_value=None):
        if feature_value is None:
            entropy_D = D
        else:
            entropy_D = self.get_D_with_given_feature_value(D, feature, feature_value)
        
        f_ctr_list = self.count_feature_values(entropy_D, self.class_label)
        entropy = 0
        N = len(entropy_D)
        for _, value in f_ctr_list.items():
            p = value.count / N
            entropy -= p * log2(p)
        return entropy


    def IG(self, D, feature):
        current_entropy = self.entropy(D, self.class_label)
        sum_of_partial_entropies = 0
        N = len(D)
        for feature_value in self.get_unique_values_for_feature(D, feature):
            partial_D = self.get_D_with_given_feature_value(D, feature, feature_value)
            partial_entropy = self.entropy(D, feature, feature_value)
            sum_of_partial_entropies += (len(partial_D)/N) * partial_entropy
        return current_entropy - sum_of_partial_entropies
    

    def get_highest_discriminative_feature(self, D, features):
        features_with_IG = []
        for feature in features:
            feature_IG = self.IG(D, feature)
            features_with_IG.append(feature_with_IG(feature, feature_IG))
        features_with_IG.sort(reverse=True)
        print(features_with_IG)
        return features_with_IG[0].feature

    
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
    

    def entropy_is_zero(self, D, class_label):
        return len(self.get_unique_values_for_feature(D, class_label)) == 1
        

    def id3(self, D, D_parent, features, class_label, depth):
        depth_limit_reached = False
        if self.max_depth is not None:
            if self.max_depth < depth:
                depth_limit_reached = True
        if len(D) == 0:
            most_common_class_value = self.most_common_feature_value(D_parent, class_label)
            return Node(most_common_class_value, most_common_class_value)
        
        most_common_class_value = self.most_common_feature_value(D, class_label)
        D_with_most_common_class_value = self.get_D_with_given_feature_value(D, class_label, most_common_class_value)
        if features is None or len(features) == 0 or \
           (set(D_with_most_common_class_value) == set(D_parent) and len(D_with_most_common_class_value) == len(D_parent)) or\
            depth_limit_reached:
            return Node(most_common_class_value, most_common_class_value)

        if self.entropy_is_zero(D, class_label):
            return Node(D[0].class_value, most_common_class_value)
        
        most_discriminative_feature = self.get_highest_discriminative_feature(D, features)
        current_node = Node(most_discriminative_feature, most_common_class_value)
        for feature_value in self.get_unique_values_for_feature(D, most_discriminative_feature):
            updated_features = copy.copy(features)
            updated_features.remove(most_discriminative_feature)
            subtree = self.id3(self.get_D_with_given_feature_value(D, most_discriminative_feature, feature_value), 
                            copy.deepcopy(D), updated_features, class_label, depth + 1)
            current_node.add_subtree(subtree, feature_value)
        return current_node
    

