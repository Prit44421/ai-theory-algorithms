"""
Branch and Bound with Cycle Detection (B&B)
A version of B&B that avoids getting into loops. 
If a child of N is already present in the path, then that is discarded.
"""

def b_and_b_nocycles(start, goal_test, move_gen, k):
    """
    Branch and Bound algorithm with cycle detection
    
    Parameters:
    - start: initial state
    - goal_test: function to check if a state is a goal
    - move_gen: function to generate children of a state
    - k: heuristic function k(N, M) that estimates cost from N to M
    
    Returns:
    - path to goal (reversed) or empty list if no solution
    """
    # OPEN ← ([S], 0) : [ ]
    OPEN = [([start], 0)]
    
    while OPEN:
        # pathPair ← head OPEN
        path_pair = OPEN.pop(0)
        # (path, cost) ← pathPair
        path, cost = path_pair
        
        # N ← head path
        N = path[0]
        
        # if GOALTEST(N) == true then return reverse(path)
        if goal_test(N):
            return list(reversed(path))
        
        # else
        # children ← MOVEGEN(N)
        children = move_gen(N)
        
        # noloops ← REMOVESEEN(children, path)
        noloops = remove_seen(children, path)
        
        # newPaths ← MAKEPATHS(noloops, pathPair)
        new_paths = make_paths(noloops, path_pair, k)
        
        # OPEN ← SORT_cost(newPaths ++ tail OPEN)
        OPEN = sorted(new_paths + OPEN, key=lambda x: x[1])
    
    # return empty list
    return []


def remove_seen(children, path):
    """
    REMOVESEEN(children, path)
    Remove children that are already in the path (cycle detection)
    
    Parameters:
    - children: list of child nodes
    - path: current path
    
    Returns:
    - list of children not in path
    """
    # if children is empty then return empty list
    if not children:
        return []
    
    # else
    # M ← head children
    M = children[0]
    
    # if OCCURSIN(M, path)
    if occurs_in(M, path):
        # then return REMOVESEEN(tail children, path)
        return remove_seen(children[1:], path)
    # else return M:REMOVESEEN(tail children, path)
    else:
        return [M] + remove_seen(children[1:], path)


def occurs_in(node, lst):
    """
    OCCURSIN(node, list)
    Check if node is in list
    
    Parameters:
    - node: node to search for
    - lst: list to search in
    
    Returns:
    - True if node is in list, False otherwise
    """
    # if list is empty then return False
    if not lst:
        return False
    # else if node == head list then return True
    elif node == lst[0]:
        return True
    # else return OCCURSIN(node, tail list)
    else:
        return occurs_in(node, lst[1:])


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
    # Define a graph with potential cycles
    graph = {
        'S': ['A', 'B'],
        'A': ['C', 'S'],  # Cycle back to S
        'B': ['A', 'E'],  # Can go to A
        'C': ['G'],
        'E': ['G'],
        'G': []
    }
    
    # Edge costs
    costs = {
        ('S', 'A'): 1,
        ('S', 'B'): 5,
        ('A', 'C'): 2,
        ('A', 'S'): 1,  # Cycle
        ('B', 'A'): 1,
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
    
    result = b_and_b_nocycles('S', goal_test, move_gen, k)
    print("Path found:", result)
    
    if result:
        total_cost = sum(k(result[i], result[i+1]) for i in range(len(result)-1))
        print("Total cost:", total_cost)
        print("\nThis algorithm avoided cycles that would have occurred with basic B&B")
