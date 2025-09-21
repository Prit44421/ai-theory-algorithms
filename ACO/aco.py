import random

def tour_length(tour, distance_matrix):
    length=0
    for i in range(len(tour)):
        length+=distance_matrix[tour[i]-1][tour[(i+1)%len(tour)]-1]
    return length

def generate_tour(start_city, distance_matrix, pheromone_matrix, alpha, beta):
    num_cities=len(distance_matrix)
    unvisited=set(range(1,num_cities+1))
    unvisited.remove(start_city)
    tour=[start_city]
    current_city=start_city
    while unvisited:
        probabilities=[]
        total=0
        for city in unvisited:
            pheromone=pheromone_matrix[current_city-1][city-1]**alpha
            heuristic=(1/distance_matrix[current_city-1][city-1])**beta
            prob=pheromone*heuristic
            probabilities.append((city, prob))
            total+=prob
        r=random.uniform(0, total)
        cumulative=0
        for city, prob in probabilities:
            cumulative+=prob
            if cumulative>=r:
                next_city=city
                break
        tour.append(next_city)
        unvisited.remove(next_city)
        current_city=next_city
    return tour




def update_pheromone(tours, distance_matrix, pheromone_matrix, evaporation_rate):

    pheromone_constant=1000

    pheromone_matrix=[[p*(1-evaporation_rate) for p in row] for row in pheromone_matrix]

    for tour in tours:
        tour_length_value=tour_length(tour, distance_matrix)
        for i in range(len(tour)):
            pheromone_matrix[tour[i]-1][tour[(i+1)%len(tour)]-1]+=(pheromone_constant/tour_length_value)



def aco(distance_matrix, num_ants, max_iterations, alpha=1.0, beta=2.0, evaporation_rate=0.5, initial_pheromone=1.0):
    num_cities=len(distance_matrix)


    pheromone_matrix=[[initial_pheromone for _ in range(num_cities)] for _ in range(num_cities)]
    best_tour=None
    for i in range(max_iterations):
        ants=[random.randint(1, num_cities) for _ in range(num_ants)]
        tours=[]
        for start in ants:
            tour=generate_tour(start, distance_matrix, pheromone_matrix, alpha, beta)
            tours.append(tour)
            if best_tour is None or tour_length(tour, distance_matrix)<tour_length(best_tour, distance_matrix):
                best_tour=tour
                print(f"Iteration {i+1}, new best tour: {best_tour} with length {tour_length(best_tour, distance_matrix)}")
        
        update_pheromone(tours, distance_matrix, pheromone_matrix, evaporation_rate)
    return best_tour
