import itertools

def calculate_tour_cost(tour, matrix):
    """Calculates the total cost of a given tour."""
    total_cost = 0
    # Add cost for each leg of the tour
    for i in range(len(tour) - 1):
        total_cost += matrix[tour[i]][tour[i+1]]
    # Add cost of returning from the last city to the start city
    total_cost += matrix[tour[-1]][tour[0]]
    return total_cost

def tour_to_string(tour_indices, names):
    """Converts a tour from indices to a readable string of city names."""
    return " -> ".join(names[i] for i in tour_indices) + f" -> {names[tour_indices[0]]}"

# --- Part 1: Problem Setup ---

# City mapping for easier reading and indexing
city_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
city_map = {name: i for i, name in enumerate(city_names)}

# Symmetric distance matrix
dist_matrix = [
    [0, 12, 10, 19, 8, 14, 15],
    [12, 0, 3, 7, 11, 8, 9],
    [10, 3, 0, 6, 9, 7, 12],
    [19, 7, 6, 0, 5, 10, 8],
    [8, 11, 9, 5, 0, 6, 7],
    [14, 8, 7, 10, 6, 0, 4],
    [15, 9, 12, 8, 7, 4, 0]
]

# --- Part 2: Heuristic Search (Hill Climbing) ---

# 1. Initial State
initial_tour_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
current_tour = [city_map[name] for name in initial_tour_names]

print("--- Hill Climbing for TSP ---")
print(f"\nInitial Tour: {tour_to_string(current_tour, city_names)}")
initial_cost = calculate_tour_cost(current_tour, dist_matrix)
print(f"Initial Cost: {initial_cost}")

# 3. Task: Repeat the process for 3 moves
num_moves = 3
for move in range(num_moves):
    print("\n" + "="*20)
    print(f"   MOVE {move + 1}")
    print("="*20)
    print(f"Current Tour: {tour_to_string(current_tour, city_names)}")
    current_cost = calculate_tour_cost(current_tour, dist_matrix)
    print(f"Current Cost: {current_cost}\n")

    best_neighbor = None
    min_neighbor_cost = float('inf')

    # Enumerate all neighbor tours by swapping two cities (excluding 'A')
    # The indices to swap are from 1 to 6 (for cities B, C, D, E, F, G)
    print("Enumerating and evaluating neighbors...")
    for i, j in itertools.combinations(range(1, len(current_tour)), 2):
        neighbor = current_tour[:]
        # Swap the two cities
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        neighbor_cost = calculate_tour_cost(neighbor, dist_matrix)
        
        print(f"  - Swapping ({city_names[current_tour[i]]}, {city_names[current_tour[j]]}): "
              f"{tour_to_string(neighbor, city_names)} | Cost: {neighbor_cost}")
        
        # Check if this neighbor is the best one found so far
        if neighbor_cost < min_neighbor_cost:
            min_neighbor_cost = neighbor_cost
            best_neighbor = neighbor

    print("\n--- Move Summary ---")
    # If a better neighbor is found, move to it.
    if min_neighbor_cost < current_cost:
        print(f"Best neighbor found with cost {min_neighbor_cost}.")
        print(f"Next Move: {tour_to_string(best_neighbor, city_names)}")
        current_tour = best_neighbor
    else:
        # This is a local minimum, the algorithm stops improving.
        print("No better neighbor found. Reached a local minimum.")
        print(f"Final Tour: {tour_to_string(current_tour, city_names)}")
        print(f"Final Cost: {current_cost}")
        break # Exit the loop if no improvement is made

print("\n--- Final Result after 3 Moves ---")
final_cost = calculate_tour_cost(current_tour, dist_matrix)
print(f"Final Tour: {tour_to_string(current_tour, city_names)}")
print(f"Final Cost: {final_cost}")