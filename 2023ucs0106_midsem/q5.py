import random


'''
graph = [
    [0,   29,  20,  21,  16,  31, 1000,  12],
    [29,   0,  15,  29,  1000,  40,  72,  21],
    [20,  15,   0,  15,  14,  25,  81,   9],
    [21,  29,  15,   0,   4,  12,  92,  12],
    [16,  1000,  14,   4,   0,  16,  95,  10],
    [31,  40,  25,  12,  16,   0,  70,  15],
    [1000, 72,  81,  92,  95,  70,   0, 101],
    [12,  21,   9,  12,  10,  15, 101,   0]
]
'''


graph=[
    [0,300,1000,90],
    [300,0,5,100],
    [1000,5,0,10],
    [90,100,10,0]
]


source_node=1


# this funtion claculate the cost of tour 
def tour_length(tour, distance_matrix):
    length=0
    for i in range(len(tour)-1):
        length+=distance_matrix[tour[i]-1][tour[(i+1)%len(tour)]-1]
    return length


# this funtion generates the tour from start_city to goal_city by using probalistic approach using pheromone

def generate_tour(start_city, distance_matrix, pheromone_matrix, alpha, beta,goal_city):
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

        # if i find the goal city i break because my tour is complete
        if current_city==goal_city:
            break
    return tour



# this funtion updates the pheromon on each edge
def update_pheromone(tours, distance_matrix, pheromone_matrix, evaporation_rate):

    pheromone_constant=1000

    pheromone_matrix=[[p*(1-evaporation_rate) for p in row] for row in pheromone_matrix]

    for tour in tours:
        tour_length_value=tour_length(tour, distance_matrix)
        for i in range(len(tour)):
            pheromone_matrix[tour[i]-1][tour[(i+1)%len(tour)]-1]+=(pheromone_constant/tour_length_value)

"""
to get the minimum path from source vertex to all vertexes,
i applied aco by putting ants on all vertexes and then generated the tour
from the start vertex to source vertex.
i have taken source vertex as my goal vertex
and i am storing the best tour found from start to goal vertex until each iteration 
"""

def aco(distance_matrix, num_ants, max_iterations, goal_city, alpha=1.0, beta=2.0, evaporation_rate=0.5, initial_pheromone=1.0):
    num_cities=len(distance_matrix)

    pheromone_matrix=[[initial_pheromone for _ in range(num_cities)] for _ in range(num_cities)]

    # best_tours store the best tour from each start vertex to goal vertex
    best_tours=[[] for i in range(num_cities)]

    for i in range(max_iterations):
        ants=[random.randint(1, num_cities) for _ in range(num_ants)]
        tours=[]
        for start in ants:
            tour=generate_tour(start, distance_matrix, pheromone_matrix, alpha, beta, goal_city)
            tours.append(tour)
            if len(best_tours[start-1])==0 or tour_length(tour,distance_matrix)<tour_length(best_tours[start-1],distance_matrix):
                best_tours[start-1]=tour
                print(f"new best tour found for vertex: {start} in iteration {i+1} : with length {tour_length(best_tours[start-1], distance_matrix)} :  {best_tours[start-1]}")

        update_pheromone(tours, distance_matrix, pheromone_matrix, evaporation_rate)
    return best_tours



solution=aco(graph,num_ants=5,max_iterations=1000, alpha=2.0, beta= 1.0, evaporation_rate=0.3, initial_pheromone=1.0, goal_city=source_node)

print("\n\n\n")

for i in range(len(graph)):
    if(i+1 != source_node):
        print(f"Distance between {i+1} and {source_node} is {tour_length(solution[i],graph)} with path: {solution[i]}")