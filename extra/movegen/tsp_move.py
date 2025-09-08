"""TSP move generators.

Representation: list of city indices forming a Hamiltonian cycle (start city fixed at index 0).

Functions:
    two_opt(node)      -> reverse a segment (classic 2-opt).
    swap_cities(node)  -> swap positions of two cities.
    insert_city(node)  -> remove city i and insert at j.
    three_opt(node)    -> all 3-edge exchanges (subset canonical cases to limit explosion).
    double_bridge(node)-> 4-segment rearrangement (useful for escaping local minima).
"""


def two_opt(node):
    children=[]
    for i in range(1,len(node)-1):
        for j in range(i+1,len(node)):
            new=node[:i]+node[i:j+1][::-1]+node[j+1:]
            children.append(new)
    return children


def swap_cities(node):
    children=[]
    for i in range(1,len(node)):
        for j in range(i+1,len(node)):
            new=node[:]
            new[i],new[j]=new[j],new[i]
            children.append(new)
    return children


def insert_city(node):
    children=[]
    for i in range(1,len(node)):
        for j in range(1,len(node)):
            if i==j: continue
            perm=node[:]
            city=perm.pop(i)
            perm.insert(j,city)
            children.append(perm)
    return children


def three_opt(node):
    """Generate neighbors via a limited 3-opt (choose i<j<k and reconnect in 3 common permutations).
    Avoid permutations equivalent to 2-opt. Keeps start city fixed.
    """
    n=len(node)
    children=[]
    for i in range(1,n-3):
        for j in range(i+1,n-2):
            for k in range(j+1,n-1):
                A=node[:i]
                B=node[i:j]
                C=node[j:k]
                D=node[k:]
                # permutations (selected)
                children.append(A+B[::-1]+C+D)      # reverse B
                children.append(A+B+C[::-1]+D)      # reverse C
                children.append(A+C+B+D)            # swap B and C
    return children


def double_bridge(node):
    """Double-bridge move (common in Lin-Kernighan) splitting tour into 4 segments.
    Pattern: (A|B|C|D) -> A C B D to create deeper perturbation.
    """
    n=len(node)
    if n<9:
        return []
    children=[]
    # choose three split points
    for a in range(1,n-6):
        for b in range(a+2,n-4):
            for c in range(b+2,n-2):
                A=node[:a]
                B=node[a:b]
                C=node[b:c]
                D=node[c:]
                children.append(A+C+B+D)
    return children
