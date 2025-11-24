"""AO* algorithm closely matching the lecture slide pseudocode."""

def ao_star(start, futility, successors, h):
    # add start to G
    G = {start}

    # compute h(start)
    h_val = {start: h(start)}

    # solved(start) ← FALSE
    solved = {start: False}

    # initially nothing is marked; we store a single best child list per node
    marked = {}

    # while solved(start) = FALSE and h(start) < Futility
    while (not solved[start]) and (h_val[start] < futility):

        # label: FORWARD PHASE
        # U ← trace marked paths in G to a set of unexpanded nodes
        U = trace_unexpanded(start, G, marked, successors)

        # N ← select a node from U  (just take one)
        N = next(iter(U))

        # children ← SUCCESSORS(N)
        children = successors(N)

        # if children is empty
        if not children:
            # h(N) ← Futility
            h_val[N] = futility
        else:
            # check for looping in the members of children
            # remove any looping members from children
            children = [c for c in children if c not in current_path_from_start(start, N, marked)]

            # for each S ∈ children
            for S in children:
                # add S to G
                if S not in G:
                    G.add(S)

                # compute h(S)
                if S not in h_val:
                    h_val[S] = h(S)

                # if S is primitive
                if len(successors(S)) == 0:
                    # solved(S) ← TRUE
                    solved[S] = True

        # label: PROPAGATE BACK
        # M ← {N}    /* set of modified nodes */
        M = {N}

        # while M is not empty
        while M:
            # D ← remove deepest node from M (we just pop any)
            D = M.pop()

            # compute best cost of D from its children (OR node: min; no AND arcs here)
            ch = successors(D)
            if not ch:
                best_cost = h_val[D]
                best_children = []
            else:
                best_cost = float("inf")
                best_children = []
                for c in ch:
                    if h_val[c] < best_cost:
                        best_cost = h_val[c]
                        best_children = [c]

            old_h = h_val[D]
            h_val[D] = best_cost

            # mark best option at D as MARKED
            marked[D] = best_children

            # if all nodes connected through marked arcs are solved
            if all(solved.get(c, False) for c in best_children):
                # solved(D) ← TRUE
                solved[D] = True

            # if D has changed
            if h_val[D] != old_h:
                # add all parents of D to M
                for p in G:
                    if D in successors(p):
                        M.add(p)

    # if solved(start) = TRUE return the marked subgraph; else null
    if solved[start]:
        return extract_marked_subgraph(start, marked)
    return None


def trace_unexpanded(start, G, marked, successors):
    """Trace marked paths from start to collect unexpanded nodes U."""
    U = set()

    def visit(n):
        # if n has no marked children yet, it is unexpanded
        if n not in marked or not marked[n]:
            U.add(n)
            return
        for c in marked[n]:
            visit(c)

    visit(start)
    return U


def current_path_from_start(start, target, marked):
    """Return nodes on some marked path from start to target (for simple loop check)."""
    path = []

    def dfs(n):
        path.append(n)
        if n == target:
            return True
        for c in marked.get(n, []):
            if dfs(c):
                return True
        path.pop()
        return False

    dfs(start)
    return set(path)


def extract_marked_subgraph(start, marked):
    """Collect nodes reachable from start following marked arcs."""
    result = set()

    def visit(n):
        if n in result:
            return
        result.add(n)
        for c in marked.get(n, []):
            visit(c)

    visit(start)
    return result


# Example usage
if __name__ == "__main__":
    # Example AND-OR graph for solving a problem
    # Problem: Get to work
    # Can be solved by (Take bus) OR (Drive car)
    # Drive car requires (Have car) AND (Have gas)
    
    graph = {
        'GetToWork': ['TakeBus', 'DriveCar'],
        'TakeBus': [],  # Primitive - can do directly
        'DriveCar': ['HaveCar', 'HaveGas'],  # AND node
        'HaveCar': [],  # Primitive
        'HaveGas': []   # Primitive
    }
    
    # Heuristic costs
    costs = {
        'GetToWork': 10,
        'TakeBus': 5,
        'DriveCar': 3,
        'HaveCar': 1,
        'HaveGas': 1
    }
    
    def successors(node):
        return graph.get(node, [])
    
    def h(node):
        return costs.get(node, 0)
    
    futility = 1000

    result = ao_star('GetToWork', futility, successors, h)
    
    if result:
        print("Solution found!")
        print("Nodes in solution:", result)
        print("\nMarked paths:")
        for node, children in marked.items():
            if node in result:
                print(f"  {node} -> {children}")
    else:
        print("No solution found (futile)")
