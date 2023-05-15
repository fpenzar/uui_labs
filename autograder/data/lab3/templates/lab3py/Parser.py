import sys
from data_point import data_point


class Parser:

    def __init__(self):
        self.train_dataset_path = ""
        self.test_dataset_path = ""
        self.depth = None


    def read_stdin(self):
        self.train_dataset_path = sys.argv[1]
        self.test_dataset_path = sys.argv[2]
        if len(sys.argv) == 4:
            self.depth = int(sys.argv[3])
    

    def read(self, path):
        dataset = []
        with open(path) as file:
            for i, row in enumerate(file.readlines()):
                if i == 0:
                    labels = row.strip().split(",")
                    continue
                values = row.strip().split(",")
                dataset.append(data_point(labels, values))
        return dataset
    

    def parse(self):
        train_dataset = self.read(self.train_dataset_path)
        test_dataset = self.read(self.test_dataset_path)
        return train_dataset, test_dataset