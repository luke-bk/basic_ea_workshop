import random


# The problem we are solving, maximising the number of 1's in a list
# [0,0,0,0,0,0] all zero's is bad!
# [1,0,1,0,1,0] some of each, this is better.
# [1,1,1,1,1,1] This is the optimal solution
def fitness_function(chromosome):
    return sum(chromosome.genes)  # fitness function: Count the number of ones


# How do we represent a solution to our problem?
# A chromosome in this instance is a list of 0's and 1's, and an integer for fitness
# Our chromosome is really just a list..and our genes are just numbers..
class Chromosome:
    def __init__(self):
        self.genes = []  # just a list
        self.fitness = 0  # just a number


# Create an initial population of chromosomes (potential solutions...or just..lists)
# Our population is just a list of lists
def create_population(size, chromosome_length):
    population = []
    for x in range(size):
        chromosome = Chromosome()
        chromosome.genes = [random.randint(0, 1) for _ in range(chromosome_length)]
        population.append(chromosome)
    return population


# Survival of the fittest?? We are just comparing two lists and selecting the list with the most 1's
# Selection: Randomly compare two chromosomes, who is higher is selected
def tournament_selection(population, tournament_size):
    tournament = random.sample(population, tournament_size)
    return max(tournament, key=lambda chromosome: chromosome.fitness)


# Let's produce a child..Or, lets just combine two lists together
# Crossover: One-point crossover
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1.genes) - 1)  # choose a crossover point
    child_genes = parent1.genes[:point] + parent2.genes[point:]  # combine genes at the crossover point
    return child_genes


# Lets add in genetic diversity to escape local optimums..OR just change a number randomly in a list
# Mutation: Mutate genes based on mutation rate
def mutate(chromosome, rate):
    for i in range(len(chromosome.genes)):
        if random.random() < rate:
            chromosome.genes[i] = 1 - chromosome.genes[i]


# Admin work/ helper function. I just want to return the best chromosome in the current population
def best_chromosome(population):
    # Sort population by fitness in descending order
    population = sorted(population, key=lambda chromosome: chromosome.fitness, reverse=True)

    # Get the best chromosome and its fitness
    return population[0]


# The evolutionary algorithm!
def evolutionary_algorithm():
    # Parameters
    random.seed(10)  # control the randomness
    population_size = 10
    chromosome_length = 30
    mutation_rate = 0.01  # keep this small, if its too large, you will just have random search
    generations = 50
    tournament_size = 2  # "selection pressure" is low

    population = create_population(population_size, chromosome_length)  # step one: initialise populations

    for generation in range(generations):  # main evolutionary loop..or just a loop in a loop..
        for chromosome in population:  # step two: evaluate populations
            chromosome.fitness = fitness_function(chromosome)

        # Print the best fitness and the corresponding chromosome
        print(f"Generation {generation}: Best Fitness = {best_chromosome(population).fitness}, "
              f"Chromosome = {best_chromosome(population).genes}")

        if best_chromosome(population).fitness == chromosome_length:  # step three: check termination condition
            break

        # Create a new population
        new_population = []

        while len(new_population) < population_size:  # step four: population management
            parent1 = tournament_selection(population, tournament_size)
            parent2 = tournament_selection(population, tournament_size)
            child = Chromosome()
            child.genes = crossover(parent1, parent2)
            mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population


# Run the EA with this call
evolutionary_algorithm()
