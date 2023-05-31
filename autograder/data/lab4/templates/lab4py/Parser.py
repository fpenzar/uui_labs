import sys
import numpy as np

TRAIN = "--train"
TEST = "--test"
NN = "--nn"
POPSIZE = "--popsize"
ELITISM = "--elitism"
P = "--p"
K = "--K"
ITER = "--iter"


class Parser:

    def read_stdin(self):
        for index, arg in enumerate(sys.argv):
            if arg == TRAIN:
                self.train_path = sys.argv[index + 1]
            elif arg == TEST:
                self.test_path = sys.argv[index + 1]
            elif arg == NN:
                self.nn = sys.argv[index + 1]
            elif arg == POPSIZE:
                self.popsize = int(sys.argv[index + 1])
            elif arg == ELITISM:
                self.elitism = int(sys.argv[index + 1])
            elif arg == P:
                self.mutation_prob = float(sys.argv[index + 1])
            elif arg == K:
                self.stdev = float(sys.argv[index + 1])
            elif arg == ITER:
                self.iterations = int(sys.argv[index + 1])
        self.parse_configuration()


    def parse_configuration(self):
        configuration = self.nn.split("s")[:-1]
        self.configuration = [int(i) for i in configuration]
        self.configuration.append(1)
    

    def read(self, path):
        dataset = []
        outputs = []
        with open(path) as file:
            for i, row in enumerate(file.readlines()):
                if i == 0:
                    # ignore labels
                    continue
                values = row.strip().split(",")
                features = values[:-1]
                features = np.array([float(value) for value in values])
                output = np.array(float(values[-1]))
                dataset.append(features)
                outputs.append(output)
        dataset = np.array(dataset)
        outputs = np.array(outputs)
        return dataset.transpose(), outputs
    
    def parse(self):
        train_data, train_outputs = self.read(self.train_path)
        test_data, test_outputs = self.read(self.test_path)
        self.set_input_dimension(test_data)
        return train_data, train_outputs, test_data, test_outputs

    def set_input_dimension(self, test_data: np.array):
        self.configuration.insert(0, test_data.shape[0])
