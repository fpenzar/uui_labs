import numpy as np
from neural_network import NeuralNetwork
from Parser import Parser
from genetic_algorithm import genetic_algorithm

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


if __name__ == "__main__":
    parser = Parser()
    parser.read_stdin()
    train_data, train_outputs, test_data, test_outputs = parser.parse()

    configuration = parser.configuration
    population_size = parser.popsize
    elitism = parser.elitism
    mutation_prob = parser.mutation_prob
    GA_stdev = parser.stdev
    iterations = parser.iterations
    nn_stdev = 0.01


    GA = genetic_algorithm(population_size, elitism, mutation_prob, GA_stdev, iterations, configuration, sigmoid, nn_stdev)
    GA.train_nn(train_data, train_outputs)
    GA.test(test_data, test_outputs)
    # nn = NeuralNetwork(configuration, sigmoid, 0.01)
    # result = nn.forward(test_data)
    # print(result - test_outputs)
