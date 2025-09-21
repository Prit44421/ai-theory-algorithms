"""
Ant Colony Optimization for the Vehicle Routing Problem (VRP)

This script provides a solver for the Capacitated Vehicle Routing Problem (CVRP) using the Ant Colony Optimization (ACO) metaheuristic.

---
The Problem: Vehicle Routing Problem (VRP)
---
VRP is a classic combinatorial optimization problem that seeks to find the optimal set of routes for a fleet of vehicles to serve a given set of customers. The goal is to minimize the total cost, which is typically the total distance traveled by all vehicles.

This implementation specifically addresses the Capacitated VRP (CVRP), which includes the following constraints:
1.  Each vehicle starts and ends its route at a central depot.
2.  Each customer must be visited exactly once by one vehicle.
3.  The total demand of the customers served by a single vehicle must not exceed its capacity.

---
Variations of VRP & How to Adapt This Code
---
VRP has many variations. Here are a few common ones and how you could modify this code to handle them:

1.  VRP with Time Windows (VRPTW):
    -   Problem: Each customer has a specific time window during which they must be visited.
    -   Code Changes:
        -   Add `ready_time` and `due_date` for each customer.
        -   Track the `current_time` for each vehicle as it travels. Travel time can be derived from the distance matrix.
        -   When selecting the next city, an ant can only consider cities where the vehicle can arrive within the time window. If a vehicle arrives early, it must wait.
        -   The heuristic could be modified to prioritize customers with tighter or earlier time windows.

2.  VRP with Pickup and Delivery (VRPPD):
    -   Problem: Vehicles must pick up items from one location and deliver them to another.
    -   Code Changes:
        -   The problem definition needs to include pickup-delivery pairs.
        -   The state for each ant needs to be more complex, tracking which items have been picked up.
        -   The logic for selecting the next city must ensure that a delivery location is only visited after the corresponding pickup location has been visited by the same vehicle.

3.  Multi-Depot VRP (MDVRP):
    -   Problem: There are multiple depots from which vehicles can start and end their routes.
    -   Code Changes:
        -   The `generate_routes` function would need to handle multiple starting points. You could assign ants to different depots.
        -   When a vehicle completes its route, it must return to its original starting depot. The logic would need to be adjusted to handle this.

---
ACO Parameters (How to Tune the Algorithm)
---
-   `num_ants`: The number of ants (solutions) generated per iteration. More ants mean more exploration but higher computational cost.
-   `max_iterations`: The total number of cycles the algorithm runs for.
-   `alpha`: Pheromone influence factor. Higher alpha means ants are more likely to follow popular paths (exploitation).
-   `beta`: Heuristic influence factor. Higher beta means ants are more likely to choose closer cities (greedy behavior).
-   `evaporation_rate`: Rate at which pheromones evaporate. A high rate encourages exploration of new paths, while a low rate reinforces existing good paths.
-   `initial_pheromone`: The initial amount of pheromone on all paths.
"""
import random

def calculate_total_distance(routes, distance_matrix):
    """
    Calculates the total distance traveled for a set of routes.
    A solution in VRP is a set of routes, so we sum the distance of each route.
    """
    total_distance = 0
    # Iterate through each individual route in the solution
    for route in routes:
        # For each route, sum the distances between consecutive cities
        for i in range(len(route) - 1):
            # Note: city numbers are 1-based, so we subtract 1 for 0-based matrix indexing
            from_city = route[i]
            to_city = route[i+1]
            total_distance += distance_matrix[from_city - 1][to_city - 1]
    return total_distance

def generate_routes(start_depot, distance_matrix, pheromone_matrix, demands, vehicle_capacity, alpha, beta):
    """
    Generates a complete VRP solution (a set of routes) for one ant.
    The ant starts building routes from the depot until all cities have been visited.
    """
    num_cities = len(distance_matrix)
    # Create a set of unvisited cities. The depot is not a "customer" to be visited.
    unvisited = set(range(1, num_cities + 1))
    unvisited.remove(start_depot)
    
    # This will hold the complete solution for this ant (e.g., [[1, 2, 4, 1], [1, 3, 5, 1]])
    routes = []
    
    # Continue creating new routes as long as there are unvisited customer cities
    while unvisited:
        # Each new route starts at the depot
        current_route = [start_depot]
        current_load = 0
        current_city = start_depot
        
        # This inner loop builds a single route for one vehicle
        while True:
            # From the current city, find all unvisited cities that the vehicle can serve
            # without exceeding its capacity.
            possible_next = []
            for city in unvisited:
                if current_load + demands[city - 1] <= vehicle_capacity:
                    possible_next.append(city)
            
            # If there are no cities that can be visited (either all are visited or capacity limit reached),
            # the current route is finished.
            if not possible_next:
                break 

            # --- ACO Core: Probabilistic City Selection ---
            probabilities = []
            total_prob = 0
            for city in possible_next:
                # Pheromone level (alpha): The learned desirability of this path.
                pheromone = pheromone_matrix[current_city - 1][city - 1] ** alpha
                # Heuristic information (beta): The greedy choice. 1/distance makes closer cities more attractive.
                heuristic = (1 / distance_matrix[current_city - 1][city - 1]) ** beta
                # Combine pheromone and heuristic to get the probability
                prob = pheromone * heuristic
                probabilities.append((city, prob))
                total_prob += prob
            
            # --- Roulette Wheel Selection ---
            # Select the next city based on the calculated probabilities.
            r = random.uniform(0, total_prob)
            cumulative_prob = 0
            next_city = -1
            for city, prob in probabilities:
                cumulative_prob += prob
                if cumulative_prob >= r:
                    next_city = city
                    break
            
            # This should not happen if possible_next is not empty, but as a safeguard.
            if next_city == -1:
                break

            # Add the selected city to the route and update vehicle state
            current_route.append(next_city)
            current_load += demands[next_city - 1]
            unvisited.remove(next_city)
            current_city = next_city

        # The route is complete, so the vehicle returns to the depot.
        current_route.append(start_depot)
        routes.append(current_route)
        
    return routes

def update_pheromone(all_routes, distance_matrix, pheromone_matrix, evaporation_rate):
    """
    Updates the pheromone matrix based on the solutions found by all ants.
    This involves two steps: evaporation and deposition.
    """
    # A constant used to determine the amount of pheromone to deposit.
    pheromone_constant = 100.0

    # --- 1. Evaporation ---
    # Reduce the pheromone on all paths. This prevents getting stuck in local optima
    # and encourages exploration of new paths.
    for i in range(len(pheromone_matrix)):
        for j in range(len(pheromone_matrix[i])):
            pheromone_matrix[i][j] *= (1 - evaporation_rate)

    # --- 2. Deposition ---
    # Deposit new pheromone on the paths used by the ants.
    # Better solutions (shorter total distance) deposit more pheromone.
    for routes in all_routes: # 'routes' is the full solution for one ant
        total_distance = calculate_total_distance(routes, distance_matrix)
        if total_distance == 0: continue
        
        # The amount of pheromone to deposit is inversely proportional to the solution's quality (distance).
        pheromone_deposit = pheromone_constant / total_distance
        
        # Apply the deposit to every edge in the solution's routes
        for route in routes:
            for i in range(len(route) - 1):
                from_city = route[i]
                to_city = route[i+1]
                pheromone_matrix[from_city - 1][to_city - 1] += pheromone_deposit
                # For a symmetric VRP, the path from A to B is the same as B to A.
                pheromone_matrix[to_city - 1][from_city - 1] += pheromone_deposit

def aco_vrp(distance_matrix, demands, vehicle_capacity, num_ants, max_iterations, alpha=1.0, beta=2.0, evaporation_rate=0.5, initial_pheromone=1.0):
    """
    The main function to run the Ant Colony Optimization algorithm for VRP.
    """
    num_cities = len(distance_matrix)
    # In this implementation, City 1 (index 0) is always the depot.
    depot = 1 

    # Initialize the pheromone matrix with a small, constant value.
    pheromone_matrix = [[initial_pheromone for _ in range(num_cities)] for _ in range(num_cities)]
    best_solution = None
    best_distance = float('inf')

    # Main loop of the ACO algorithm.
    for i in range(max_iterations):
        # This list will store the solutions (sets of routes) for all ants in this iteration.
        all_ant_routes = []
        # For each ant...
        for _ in range(num_ants):
            # ...generate a complete solution.
            routes = generate_routes(depot, distance_matrix, pheromone_matrix, demands, vehicle_capacity, alpha, beta)
            all_ant_routes.append(routes)
            
            # Check if this ant's solution is the best one found so far.
            current_distance = calculate_total_distance(routes, distance_matrix)
            if current_distance < best_distance:
                best_solution = routes
                best_distance = current_distance
                print(f"Iteration {i+1}, new best solution: {best_solution} with distance {best_distance:.2f}")
        
        # After all ants have found their solutions, update the global pheromone matrix.
        update_pheromone(all_ant_routes, distance_matrix, pheromone_matrix, evaporation_rate)
        
    return best_solution, best_distance

if __name__ == '__main__':
    # --- Example Usage ---
    # This is a small example to demonstrate how to use the aco_vrp function.
    
    # 5 cities, where city 1 (index 0) is the depot.
    # The matrix represents the travel distance between any two cities.
    distance_matrix = [
        [0, 10, 20, 30, 40],
        [10, 0, 15, 25, 35],
        [20, 15, 0, 10, 20],
        [30, 25, 10, 0, 10],
        [40, 35, 20, 10, 0]
    ]
    
    # Demands for each city. The depot (city 1) has a demand of 0.
    demands = [0, 5, 8, 6, 7]
    
    # The maximum capacity of each vehicle.
    vehicle_capacity = 15
    # Number of ants to use in each iteration.
    num_ants = 5
    # Number of iterations to run the algorithm.
    max_iterations = 100

    print("Starting ACO for VRP...")
    best_routes, best_dist = aco_vrp(distance_matrix, demands, vehicle_capacity, num_ants, max_iterations)
    
    print("\n--- Best Solution Found ---")
    print(f"Routes: {best_routes}")
    print(f"Total Distance: {best_dist:.2f}")
