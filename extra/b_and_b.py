"""
Branch and Bound (B&B) Algorithm
Algorithm B&B searches in the space of partial paths. 
It extends the cheapest partial path till it finds one to the goal.
"""

def b_and_b(start, goal_test, move_gen, k):
    """
    Branch and Bound algorithm
    
    Parameters:
    - start: initial state
    - goal_test: function to check if a state is a goal
    - move_gen: function to generate children of a state
    - k: heuristic function k(N, M) that estimates cost from N to M
    
    Returns:
    - path to goal (reversed) or empty list if no solution
    """
    # OPEN ← ([S], 0) : [ ]
    # OPEN is a priority queue of (path, cost) pairs
    OPEN = [([start], 0)]
    
    while OPEN:
        # pathPair ← head OPEN
        # (path, cost) ← pathPair
        path_pair = OPEN.pop(0)  # Remove head
        path, cost = path_pair
        
        # N ← head path
        N = path[0]  # Current node is head of path
        
        # if GOALTEST(N) == true
        if goal_test(N):
            # then return reverse(path)
            return list(reversed(path))
        
        # else
        # children ← MOVEGEN(N)
        children = move_gen(N)
        
        # newPaths ← MAKEPATHS(children, pathPair)
        new_paths = make_paths(children, path_pair, k)
        
        # OPEN ← SORT_cost(newPaths ++ tail OPEN)
        OPEN = sorted(new_paths + OPEN, key=lambda x: x[1])
    
    # return empty list
    return []


def make_paths(children, path_pair, k):
    """
    MAKEPATHS(children, pathPair)
    
    Parameters:
    - children: list of child nodes
    - path_pair: (path, cost) tuple
    - k: heuristic function
    
    Returns:
    - list of new (path, cost) pairs
    """
    # if children is empty
    if not children:
        # then return empty list
        return []
    
    # else
    # (path, cost) ← pathPair
    path, cost = path_pair
    
    # M ← head children
    M = children[0]
    
    # N ← head path
    N = path[0]
    
    # return ([M,path], cost + k(N, M)): MAKEPATHS(tail children, pathPair)
    new_path = [M] + path
    new_cost = cost + k(N, M)
    
    return [(new_path, new_cost)] + make_paths(children[1:], path_pair, k)


# Example usage
if __name__ == "__main__":
    # Define a simple graph
    graph = {
        'S': ['A', 'B'],
        'A': ['C', 'D'],
        'B': ['E'],
        'C': ['G'],
        'D': [],
        'E': ['G'],
        'G': []
    }
    
    # Edge costs
    costs = {
        ('S', 'A'): 1,
        ('S', 'B'): 5,
        ('A', 'C'): 2,
        ('A', 'D'): 4,
        ('B', 'E'): 2,
        ('C', 'G'): 3,
        ('E', 'G'): 1
    }
    
    def move_gen(node):
        return graph.get(node, [])
    
    def goal_test(node):
        return node == 'G'
    
    def k(n, m):
        return costs.get((n, m), 0)
    
    result = b_and_b('S', goal_test, move_gen, k)
    print("Path found:", result)
    
    if result:
        total_cost = sum(k(result[i], result[i+1]) for i in range(len(result)-1))
        print("Total cost:", total_cost)
