import random

def crossover(parent1, parent2):
    size = len(parent1)
    point = random.randint(0, size - 1)
    
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]


    return child1, child2

def mutate(individual, mutation_rate=0.01):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i]=random.choice([0,1])
    return individual


def state_gen(start_state,n):
    states=[]
    for i in range(n):
        state=[random.choice([0,1]) for x in range(len(start_state))]
        states.append(state)
    return states

def fitness_func(state, heuristic):
    return len(state) - heuristic(state)


def select_parents(candidates, fitness_func, heuristic, n):
    weights = [fitness_func(c, heuristic) for c in candidates]
    total_fitness = sum(weights)
    selected = []
    for _ in range(n):
        c=random.random() * total_fitness
        for i, w in enumerate(weights):
            c -= w
            if c <= 0:
                selected.append(candidates[i])
                break
    return selected



def genetic_algorithm(start_state, population, heuristic, generations=1000, mutation_rate=0.01, k=2):
    candidates = state_gen(start_state, population)
    best_offspring = None


    for i in range(generations):
        candidates = select_parents(candidates, fitness_func, heuristic, population)
        next_generation = []

        while len(next_generation) < population:
            parent1, parent2 = select_parents(candidates, fitness_func, heuristic, 2)
            child1, child2 = crossover(parent1, parent2)
            next_generation.append(mutate(child1, mutation_rate))
            next_generation.append(mutate(child2, mutation_rate))

        next_generation= sorted(next_generation, key=lambda x: fitness_func(x, heuristic), reverse=True)


        candidates = candidates[:k] + next_generation[:population - k]
        best_offspring = max(candidates, key=lambda x: fitness_func(x, heuristic))

    print(f"Best Offspring: {best_offspring}, Fitness: {fitness_func(best_offspring, heuristic)}")
    return best_offspring