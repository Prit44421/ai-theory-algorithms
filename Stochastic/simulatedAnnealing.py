import random
import math


def cooling_funtion(initial_temp, cooling_rate, step):
    return initial_temp * (cooling_rate**step)


def simulated_annealing(start_node, movegen, heuristic, max_steps=1000, initial_temp=100, cooling_rate=0.95):
    current_node = start_node
    best_node = start_node
    temperature = initial_temp
    for step in range(1,max_steps):
        n= max_steps // 10
        while n>0:
            n-=1
            neighbors = movegen(current_node)
            if not neighbors:
                return best_node
            next_node = random.choice(neighbors)
            delta_e = heuristic(current_node) - heuristic(next_node)
            if random.uniform(0, 1) < 1/(1+math.exp(min(700,-delta_e / temperature))):
                current_node = next_node
                if heuristic(current_node) < heuristic(best_node):
                    best_node = current_node
                break
            
            temperature= cooling_funtion(initial_temp, cooling_rate, step)
    return best_node