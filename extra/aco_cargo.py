"""
Ant Colony Optimization for the Cargo Load Problem (Knapsack Problem)

This script provides a solver for the 0/1 Knapsack Problem using the Ant Colony Optimization (ACO) metaheuristic. The "Cargo Load Problem" is often a direct mapping to the Knapsack Problem.

---
The Problem: 0/1 Knapsack Problem
---
The Knapsack Problem is a classic combinatorial optimization problem. Given a set of items, each with a weight and a value, the goal is to determine the number of each item to include in a collection (the "knapsack") so that the total weight is less than or equal to a given limit and the total value is as large as possible.

This implementation specifically addresses the "0/1" version, which means for each item, you can either take it or leave it (you cannot take a fraction of an item or multiple copies of the same item).

Analogy to Cargo Loading:
-   **Items**: Pieces of cargo.
-   **Weight**: The weight or volume of each piece of cargo.
-   **Value**: The priority or monetary value of each piece of cargo.
-   **Knapsack Capacity**: The maximum weight or volume the vehicle (e.g., a truck or plane) can hold.
-   **Goal**: Maximize the total value of the cargo loaded onto the vehicle without exceeding its capacity.

---
Variations of the Knapsack Problem & How to Adapt This Code
---

1.  **Unbounded Knapsack Problem (UKP):**
    -   **Problem:** You can take an unlimited number of copies of each item.
    -   **Code Changes:**
        -   In `generate_solution`, the `available_items` list would not have items removed from it. An item could be selected multiple times.
        -   You would need a mechanism to stop an ant from adding the same item infinitely. For example, an ant's construction process for a solution would stop once no more items (of any type) can fit into the knapsack.

2.  **Multi-dimensional Knapsack Problem (MKP):**
    -   **Problem:** The knapsack has multiple constraints. For example, a vehicle has both a weight limit AND a volume limit.
    -   **Code Changes:**
        -   Each `item` would have multiple 'weight' attributes (e.g., `item['weight']`, `item['volume']`).
        -   The `capacity` would become a dictionary or list of constraints (e.g., `max_weight`, `max_volume`).
        -   In `generate_solution`, the check `if current_weight + items[item_idx-1]['weight'] <= capacity:` would need to be updated to check all constraints (e.g., `current_weight + new_weight <= max_weight AND current_volume + new_volume <= max_volume`).

3.  **Multiple Knapsacks Problem:**
    -   **Problem:** You have multiple knapsacks (e.g., multiple vehicles) and you want to distribute items among them to maximize total value.
    -   **Code Changes:** This is a much more complex adaptation.
        -   The solution representation would need to change. Instead of a single list `[1, 0, 1]`, it might be a list of lists, where each sublist represents a knapsack.
        -   The `generate_solution` function would need to decide both WHICH item to add and WHICH knapsack to add it to. The pheromone matrix might need to be redesigned to guide this dual choice.

---
ACO Parameters (How to Tune the Algorithm)
---
-   `num_ants`: The number of ants (solutions) generated per iteration.
-   `max_iterations`: The total number of cycles the algorithm runs for.
-   `alpha`: Pheromone influence factor. Higher alpha makes ants more likely to pick items that have been part of good solutions in the past.
-   `beta`: Heuristic influence factor. Higher beta makes ants more likely to pick items with a high value-to-weight ratio (a greedy choice).
-   `evaporation_rate`: Controls how quickly old pheromone trails fade. A higher rate encourages exploration.
-   `initial_pheromone`: The starting pheromone level for all items.
"""


import random

def calculate_fitness(solution, items):
    """
    Calculates the total value and weight of a given solution.
    A solution is a binary list where 1 means the item is selected and 0 means it's not.
    """
    total_weight = 0
    total_value = 0
    for i, selected in enumerate(solution):
        if selected:
            # Note: The problem items are 1-based in concept, but the list is 0-based.
            # Here, `i` is the 0-based index.
            total_weight += items[i]['weight']
            total_value += items[i]['value']
    return total_value, total_weight

def generate_solution(pheromone_matrix, items, capacity, alpha, beta):
    """
    Generates a single solution (a knapsack configuration) for one ant.
    The ant iteratively picks items to add to the knapsack based on pheromone and heuristic.
    """
    num_items = len(items)
    # Start with an empty knapsack (no items selected).
    solution = [0] * num_items
    current_weight = 0
    
    # The list of items the ant can still choose from.
    available_items = list(range(num_items)) # Using 0-based index
    
    # The ant continues to add items as long as there are items available to choose from.
    while available_items:
        # --- ACO Core: Probabilistic Item Selection ---
        probabilities = []
        total_prob = 0
        
        # Consider all available items that can fit in the remaining capacity.
        for item_idx in available_items:
            if current_weight + items[item_idx]['weight'] <= capacity:
                # Pheromone (alpha): The learned desirability of including this item.
                # In this problem, the pheromone is associated with each item, not a path between items.
                pheromone = pheromone_matrix[item_idx] ** alpha
                
                # Heuristic (beta): The greedy choice. A high value-to-weight ratio is a good heuristic.
                # This encourages picking "efficient" items.
                value_per_weight = items[item_idx]['value'] / items[item_idx]['weight']
                heuristic = value_per_weight ** beta
                
                # Combine pheromone and heuristic.
                prob = pheromone * heuristic
                probabilities.append((item_idx, prob))
                total_prob += prob
        
        # If no items can be added (either none left, or none fit), stop building.
        if not probabilities:
            break

        # --- Roulette Wheel Selection ---
        # Select the next item to add based on the calculated probabilities.
        r = random.uniform(0, total_prob)
        cumulative_prob = 0
        selected_item_idx = -1
        for item_idx, prob in probabilities:
            cumulative_prob += prob
            if cumulative_prob >= r:
                selected_item_idx = item_idx
                break
        
        # If an item was selected, add it to the solution.
        if selected_item_idx != -1:
            solution[selected_item_idx] = 1
            current_weight += items[selected_item_idx]['weight']
            available_items.remove(selected_item_idx)
        else:
            # This case should not be reached if `probabilities` is not empty.
            break
            
    return solution

def update_pheromone(solutions, items, capacity, pheromone_matrix, evaporation_rate):
    """
    Updates the pheromone levels on each item based on the quality of the solutions
    found by the ants in the current iteration.
    """
    # A constant to scale the amount of pheromone deposited.
    pheromone_constant = 10.0

    # --- 1. Evaporation ---
    # Reduce the pheromone level on all items. This encourages exploration.
    for i in range(len(pheromone_matrix)):
        pheromone_matrix[i] *= (1 - evaporation_rate)

    # --- 2. Deposition ---
    # Add pheromone to items that were part of good solutions.
    for solution in solutions:
        total_value, total_weight = calculate_fitness(solution, items)
        
        # We only reward valid solutions that do not exceed the capacity.
        if total_weight > capacity:
            continue
        
        if total_value > 0:
            # The amount of pheromone deposited is proportional to the quality (total value) of the solution.
            # Normalizing by the sum of all values can help scale the deposit.
            total_possible_value = sum(item['value'] for item in items)
            pheromone_deposit = pheromone_constant * (total_value / total_possible_value)
            
            # Apply the deposit to each item included in this successful solution.
            for i, selected in enumerate(solution):
                if selected:
                    pheromone_matrix[i] += pheromone_deposit

def aco_cargo(items, capacity, num_ants, max_iterations, alpha=1.0, beta=1.0, evaporation_rate=0.1, initial_pheromone=1.0):
    """
    The main function to run the Ant Colony Optimization algorithm for the Cargo/Knapsack problem.
    """
    num_items = len(items)
    
    # Initialize pheromone trails. Each item has its own pheromone level.
    pheromone_matrix = [initial_pheromone] * num_items
    best_solution = None
    best_value = 0
    best_weight = 0

    # Main loop of the ACO algorithm.
    for i in range(max_iterations):
        all_solutions = []
        # For each ant...
        for _ in range(num_ants):
            # ...generate a complete solution (knapsack configuration).
            solution = generate_solution(pheromone_matrix, items, capacity, alpha, beta)
            all_solutions.append(solution)
            
            current_value, current_weight = calculate_fitness(solution, items)
            
            # If the solution is valid and better than the current best, update the best solution.
            if current_weight <= capacity and current_value > best_value:
                best_solution = solution
                best_value = current_value
                best_weight = current_weight
                print(f"Iteration {i+1}, new best solution value: {best_value}, weight: {best_weight}")
        
        # After all ants have built their solutions, update the pheromone trails.
        update_pheromone(all_solutions, items, capacity, pheromone_matrix, evaporation_rate)
        
    return best_solution, best_value, best_weight

if __name__ == '__main__':
    # --- Example Usage: Cargo Load Problem (0/1 Knapsack Problem) ---
    items = [
        {'weight': 10, 'value': 60}, {'weight': 20, 'value': 100},
        {'weight': 30, 'value': 120}, {'weight': 15, 'value': 80},
        {'weight': 25, 'value': 110}, {'weight': 5, 'value': 30}
    ]
    
    knapsack_capacity = 50
    num_ants = 10
    max_iterations = 100

    print("Starting ACO for Cargo Loading...")
    best_sol, best_val, best_w = aco_cargo(items, knapsack_capacity, num_ants, max_iterations)
    
    print("\n--- Best Solution Found ---")
    if best_sol:
        # To make the output more readable, show the 1-based index of selected items.
        selected_items = [i+1 for i, sel in enumerate(best_sol) if sel]
        print(f"Selected items (by 1-based index): {selected_items}")
        print(f"Total Value: {best_val}")
        print(f"Total Weight: {best_w}/{knapsack_capacity}")
    else:
        print("No solution found.")
