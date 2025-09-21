import random
import math





def stochastic_hill_climbing(start_node, movegen, heuristic, max_steps=1000, temperature=0.5):
    current_node = start_node
    best_node = start_node
    for step in range(max_steps):
        neighbors = movegen(current_node)
        if not neighbors:
            return best_node
        n=max_steps//10
        while n>0:
            n-=1
            next_node = random.choice(neighbors)
            delta_e = heuristic(current_node) - heuristic(next_node)
            # print(delta_e)
            if random.uniform(0, 1) < 1/(1+math.exp(min(700,-delta_e / temperature))):
                current_node = next_node
                if heuristic(current_node) < heuristic(best_node):
                    best_node = current_node
                break
    return best_node

