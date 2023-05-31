import numpy as np


class NeuralNetwork:

    def __init__(self, configuration, activation_func, stdev) -> None:
        self.weights = []
        self.biases = []
        self.activation_func = activation_func

        # configuration = [i, l_1, l_2, ... , o]
        for i in range(len(configuration) - 1):
            n = configuration[i]
            m = configuration[i+1]
            weights_i = np.random.normal(0, stdev, size=(m, n))
            biases_i = np.random.normal(0, stdev, size=(m, 1))

            self.weights.append(weights_i)
            self.biases.append(biases_i)
        # print(self.weights)
        # print(self.biases)


    def forward(self, X) -> np.array:
        input = X
        for i in range(len(self.weights) - 1):
            input = self.activation_func(np.matmul(self.weights[i], input) + self.biases[i])
        return (np.matmul(self.weights[-1], input) + self.biases[-1])[0]


    def set_fitness(self, fitness):
        self.fitness = fitness
    

    def __lt__(self, other):
        return self.fitness < other.fitness
