from neural_network import NeuralNetwork
import numpy as np
import copy


class genetic_algorithm:

    def __init__(self, population_size, elitism, mutation_prob, stdev, iterations, nn_configuration, activation_func, nn_stdev):
        self.population_size = population_size
        self.elitism = elitism
        self.mutation_prob = mutation_prob
        self.stdev = stdev
        self.iterations = iterations
        self.nn_configuration = nn_configuration
        self.activation_func = activation_func
        self.nn_stdev = nn_stdev
        self.populate()

    def populate(self):
        self.population = []
        for _ in range(self.population_size):
            self.population.append(NeuralNetwork(self.nn_configuration, self.activation_func, self.nn_stdev))


    def mean_squared_error(self, individual):
        N = self.outputs.shape[0]
        return np.sum(np.square(self.outputs - individual.forward(self.dataset))) / N


    def test(self, test_dataset, test_outputs):
        self.dataset = test_dataset
        self.outputs = test_outputs
        self.calculate_fitness()
        m_sqr_err = -1 * self.population[-1].fitness
        print(f"[Test error]: {m_sqr_err}")
    

    def train_nn(self, train_dataset, train_outputs):
        self.dataset = train_dataset
        self.outputs = train_outputs
        for i in range(self.iterations):
            self.calculate_fitness()
            self.calculate_selection_probs()

            if (i + 1) % 2000 == 0:
                m_sqr_err = -1 * self.population[-1].fitness
                print(f"[Train error @{i + 1}]: {m_sqr_err}")

            children = []
            for elite in self.population[len(self.population) - self.elitism:]:
                children.append(elite)
            
            for _ in range(len(self.population) - self.elitism):
                parent_1, parent_2 = self.selection()
                child = self.crossover(parent_1, parent_2)
                self.mutation(child)
                children.append(child)
            self.population = children

            
    def fitness(self, individual):
        return -self.mean_squared_error(individual)


    def crossover(self, parent_1, parent_2):
        child = NeuralNetwork(self.nn_configuration, self.activation_func, self.nn_stdev)
        for i in range(len(child.weights)):
            child.weights[i] = (parent_1.weights[i] + parent_2.weights[i]) / 2
            child.biases[i] = (parent_1.biases[i] + parent_2.biases[i]) / 2
        return child
    

    def mutation(self, individual: NeuralNetwork):
        for i in range(len(individual.weights)):
            weights_mask = np.random.choice([0, 1], size=individual.weights[i].shape, p=[1-self.mutation_prob, self.mutation_prob])
            biases_mask = np.random.choice([0, 1], size=individual.biases[i].shape, p=[1-self.mutation_prob, self.mutation_prob])
            weights_increase = np.random.normal(0, self.stdev, size=individual.weights[i].shape)
            biases_increase = np.random.normal(0, self.stdev, size=individual.biases[i].shape)
            
            individual.weights[i] += weights_mask * weights_increase
            individual.biases[i] += biases_mask * biases_increase
    

    def calculate_fitness(self):
        for individual in self.population:
            fitness = self.fitness(individual)
            individual.set_fitness(fitness)
        self.population.sort()


    def calculate_selection_probs(self):
        adjusted_fitnesses = []
        lowest_fitness_value = self.population[0].fitness
        for individual in self.population:
            adjusted_fitnesses.append(individual.fitness + (-1 * lowest_fitness_value))
        total_sum = sum(adjusted_fitnesses)
        self.selection_probs = [score / total_sum for score in adjusted_fitnesses]
        
    

    def selection(self):
        parent_1_index = np.random.choice(len(self.population), p=self.selection_probs)
        # choose next parent but do not use the one already used
        selection_probs_copy = copy.copy(self.selection_probs)
        selection_probs_copy.pop(parent_1_index)
        total_sum = sum(selection_probs_copy)
        selection_probs_copy = [p / total_sum for p in selection_probs_copy]
        parent_2_index = np.random.choice(len(self.population) - 1, p=selection_probs_copy)
        if parent_2_index >= parent_1_index:
            parent_2_index += 1

        return self.population[parent_1_index], self.population[parent_2_index]
        