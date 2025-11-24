"""
A* Algorithm
A* algorithm for finding optimal path using g(n) + h(n) evaluation.
g(n) = actual cost from start to n
h(n) = heuristic estimate from n to goal
"""

def a_star(start, goal_test, move_gen, h):
    """
    A* Algorithm
    
    Parameters:
    - start: initial state
    - goal_test: function to check if a state is a goal
    - move_gen: function to generate children (neighbors) of a state
    - h: heuristic function h(N) that estimates cost from N to goal
    
    Returns:
    - path to goal or None if no solution
    """
    # parent(S) ← null
    parent = {start: None}
    
    # g(S) ← 0
    g = {start: 0}
    
    # f(S) ← g(S) + h(S)
    f = {start: g[start] + h(start)}
    
    # OPEN ← {S}
    OPEN = [start]
    
    # CLOSED ← empty list
    CLOSED = []
    
    # while OPEN is not empty
    while OPEN:
        # N ← remove node with lowest f-value from OPEN
        N = min(OPEN, key=lambda node: f.get(node, float('inf')))
        OPEN.remove(N)
        
        # add N to CLOSED
        CLOSED.append(N)
        
        # if GOALTEST(N) == TRUE then return RECONSTRUCTPATH(N)
        if goal_test(N):
            return reconstruct_path(N, parent)
        
        # for each neighbour M ∈ MOVEGEN(N)
        for M in move_gen(N):
            # if (M ∉ OPEN and M ∉ CLOSED)
            if M not in OPEN and M not in CLOSED:
                # parent(M) ← N
                parent[M] = N
                
                # g(M) ← g(N) + k(N, M); f(M) ← g(M) + h(M)
                g[M] = g[N] + k(N, M)
                f[M] = g[M] + h(M)
                
                # add M to OPEN
                OPEN.append(M)
            
            # else
            else:
                # if (g(N) + k(N, M)) < g(M)
                if (g[N] + k(N, M)) < g.get(M, float('inf')):
                    # parent(M) ← N
                    parent[M] = N
                    
                    # g(M) ← g(N) + k(N, M); f(M) ← g(M) + h(M)
                    g[M] = g[N] + k(N, M)
                    f[M] = g[M] + h(M)
                    
                    # if X ∈ CLOSED
                    if M in CLOSED:
                        # PROPAGATEIMPROVEMENT(M)
                        propagate_improvement(M, parent, g, f, h, CLOSED)
    
    # return empty list
    return None


def propagate_improvement(M, parent, g, f, h, CLOSED):
    """
    PROPAGATEIMPROVEMENT(M)
    Update costs of descendants when a better path is found
    
    Parameters:
    - M: node whose cost was improved
    - parent: parent dictionary
    - g: g-values dictionary
    - f: f-values dictionary
    - h: heuristic function
    - CLOSED: closed list
    """
    # for each neighbour X ∈ MOVEGEN(M)
    for X in move_gen(M):
        # if g(M) + k(M, X) < g(X)
        if g[M] + k(M, X) < g.get(X, float('inf')):
            # parent(X) ← M
            parent[X] = M
            
            # g(X) ← g(M) + k(M, X)
            g[X] = g[M] + k(M, X)
            
            # f(X) ← g(X) + h(X)
            f[X] = g[X] + h(X)
            
            # if X ∈ CLOSED
            if X in CLOSED:
                # PROPAGATEIMPROVEMENT(X)
                propagate_improvement(X, parent, g, f, h, CLOSED)


def reconstruct_path(node, parent):
    """
    Reconstruct path from start to node using parent pointers
    
    Parameters:
    - node: goal node
    - parent: parent dictionary
    
    Returns:
    - path from start to node
    """
    path = []
    current = node
    while current is not None:
        path.append(current)
        current = parent.get(current)
    return list(reversed(path))


# Global edge costs (for k function)
edge_costs = {}


def k(n, m):
    """
    Cost function between nodes n and m
    """
    return edge_costs.get((n, m), 1)


# Global move_gen function for propagate_improvement
def move_gen(node):
    """
    This will be set in main
    """
    return []


# Example usage
if __name__ == "__main__":
    # Define a graph
    graph = {
        'S': [('A', 1), ('B', 4)],
        'A': [('C', 2), ('D', 5)],
        'B': [('C', 1), ('E', 3)],
        'C': [('G', 3)],
        'D': [('G', 2)],
        'E': [('G', 1)],
        'G': []
    }
    
    # Build edge costs
    for node, edges in graph.items():
        for neighbor, cost in edges:
            edge_costs[(node, neighbor)] = cost
    
    # Heuristic function (straight-line distance to goal)
    heuristic = {
        'S': 7,
        'A': 6,
        'B': 4,
        'C': 3,
        'D': 3,
        'E': 1,
        'G': 0
    }
    
    def move_gen_impl(node):
        return [neighbor for neighbor, _ in graph.get(node, [])]
    
    # Set global move_gen
    move_gen = move_gen_impl
    
    def goal_test(node):
        return node == 'G'
    
    def h(node):
        return heuristic.get(node, 0)
    
    result = a_star('S', goal_test, move_gen_impl, h)
    print("Path found:", result)
    
    if result:
        total_cost = sum(edge_costs.get((result[i], result[i+1]), 0) for i in range(len(result)-1))
        print("Total cost (g):", total_cost)
        print("f-value at goal:", total_cost + h('G'))
