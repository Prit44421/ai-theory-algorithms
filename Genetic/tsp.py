import random
import sys


# Crossover
# 1. Partially Mapped Crossover (PMX)
# 2. Order Crossover (OX)
# 3. Cycle Crossover (CX)
def crossover_pmx(parent1, parent2):
    size = len(parent1)
    child1, child2 = [-1]*size, [-1]*size

    start, end = sorted([random.randint(0, size - 1) for _ in range(2)])

    child1[start:end] = parent1[start:end]
    child2[start:end] = parent2[start:end]

    for i in range(start, end):
        if parent2[i] not in child1[start:end]:
            current_gene = parent2[i]
            p1_gene_at_pos = parent1[i]
            
            idx = parent2.index(p1_gene_at_pos)
            while child1[idx] != -1:
                 p1_gene_at_pos = parent1[idx]
                 idx = parent2.index(p1_gene_at_pos)
            child1[idx] = current_gene

    for i in range(start, end):
        if parent1[i] not in child2[start:end]:
            current_gene = parent1[i]
            p2_gene_at_pos = parent2[i]
            idx = parent1.index(p2_gene_at_pos)
            while child2[idx] != -1:
                 p2_gene_at_pos = parent2[idx]
                 idx = parent1.index(p2_gene_at_pos)
            child2[idx] = current_gene
            
    for i in range(size):
        if child1[i] == -1:
            child1[i] = parent2[i]
        if child2[i] == -1:
            child2[i] = parent1[i]
            
    return child1, child2

def crossover_ox(parent1, parent2):
    size = len(parent1)
    start, end = sorted([random.randint(0, size - 1) for _ in range(2)])

    child1 = [None] * size
    child1[start:end] = parent1[start:end]
    middle1=parent1[start:end]
    p2_iter = iter([x for x in parent2 if x not in middle1])
    for i in range(size):
        if child1[i] is None:
            child1[i] = next(p2_iter)

    child2 = [None] * size
    child2[start:end] = parent2[start:end]
    middle2=parent2[start:end]
    p1_iter = iter([x for x in parent1 if x not in middle2])
    for i in range(size):
        if child2[i] is None:
            child2[i] = next(p1_iter)

    return child1, child2

def crossover_cx(parent1, parent2):
    size = len(parent1)
    child1 = [-1] * size
    child2 = [-1] * size

    # Cycle Crossover for Child 1
    cycles = []
    visited = [False] * size
    for i in range(size):
        if not visited[i]:
            cycle = []
            curr = i
            while not visited[curr]:
                visited[curr] = True
                cycle.append(curr)
                curr = parent2.index(parent1[curr])
            cycles.append(cycle)

    for i, cycle in enumerate(cycles):
        if i % 2 == 0:  # Even cycles (including the first one)
            for index in cycle:
                child1[index] = parent1[index]
                child2[index] = parent2[index]
        else:  # Odd cycles
            for index in cycle:
                child1[index] = parent2[index]
                child2[index] = parent1[index]

    return child1, child2

# Mutation
# 1. Inversion Mutation (2-opt)
# 2. Swap Mutation (4-opt)

def mutate_inversion(individual, mutation_rate=0.01):
    i,j=sorted([random.randint(0,len(individual)-1) for _ in range(2)])
    if random.random() < mutation_rate:
        individual[i:j]=reversed(individual[i:j])
    return individual

def mutate_swap(individual, mutation_rate=0.01):
    if random.random() < mutation_rate:
        i, j = sorted([random.randint(0, len(individual) - 1) for _ in range(2)])
        individual[i], individual[j] = individual[j], individual[i]
    return individual

# Generate initial population
def state_gen(start_state,n):
    states=[]
    for i in range(n):
        state = list(range(len(start_state)))
        random.shuffle(state)
        states.append(state)
    return states

def fitness_func(state, heuristic):
    return 100_000_000-heuristic(state)


# Parent Selection
# 1. Roulette Wheel Selection
# 2. Tournament Selection
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

def select_parents_tournament(candidates, fitness_func, heuristic, n):
    selected = []
    tournament_size = max(2, len(candidates) // 10)
    for _ in range(n):
        tournament = random.sample(candidates, tournament_size)
        winner = max(tournament, key=lambda x: fitness_func(x, heuristic))
        selected.append(winner)
    return selected




def genetic_algorithm(start_state, population, heuristic, generations=1000, mutation_rate=0.01, k=2):
    candidates = state_gen(start_state, population)
    best_offspring = candidates[0]


    for i in range(generations):
        # candidates = select_parents(candidates, fitness_func, heuristic, population)
        next_generation = []

        while len(next_generation) < population:
            parent1, parent2 = select_parents(candidates, fitness_func, heuristic, 2)
            child1, child2 = crossover_pmx(parent1, parent2)
            next_generation.append(mutate_inversion(child1, mutation_rate))
            next_generation.append(mutate_inversion(child2, mutation_rate))

        next_generation= sorted(next_generation, key=lambda x: fitness_func(x, heuristic), reverse=True)


        candidates = candidates[:k] + next_generation[:population - k]
        candidates = sorted(candidates, key=lambda x: fitness_func(x, heuristic), reverse=True)
        best_offspring = max(candidates, key=lambda x: fitness_func(x, heuristic))
        if i % 100 == 0 or i == generations - 1:
            print(f"Generation {i+1}: Best Offspring: {best_offspring}, Fitness: {heuristic(best_offspring)}")

    print(f"Best Offspring: {best_offspring}, Fitness: {heuristic(best_offspring)}")
    return best_offspring