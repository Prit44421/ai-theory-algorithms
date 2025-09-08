"""SAT move generators.

State: list[int] each 0/1 representing assignment of variables.

Functions:
    flip_all(node)            -> original: flip every single variable individually.
    flip_single(node,i)       -> helper to flip one index.
    flip_pair(node)           -> flip every unordered pair of variables.
    random_flip_k(node,k)     -> sample k random single-variable flips (non‑duplicate).
    flip_until_true(node,eval)-> greedy improving single flips (eval lower = better).
    single_improving_flip(node,eval) -> the best single flip (tie keep first) or [] if none.
"""


def flip_all(node):
    """Flip every variable one at a time (original movegen)."""
    children=[]
    for i in range(len(node)):
        if node[i]==0:
            children.append(node[:i]+[1]+node[i+1:])
        else:
            children.append(node[:i]+[0]+node[i+1:])
    return children


def flip_single(node,i):
    """Flip variable at index i (helper)."""
    if i<0 or i>=len(node):
        return []
    new=node[:]
    new[i]=1-new[i]
    return [new]


def flip_pair(node):
    """Generate children by flipping any pair of variables."""
    children=[]
    n=len(node)
    for i in range(n):
        for j in range(i+1,n):
            new=node[:]
            new[i]=1-new[i]
            new[j]=1-new[j]
            children.append(new)
    return children


def flip_until_true(node,evaluator):
    """Greedy: flip each variable if it improves evaluator (lower is better)."""
    base=evaluator(node)
    bests=[]
    for i in range(len(node)):
        c=node[:]
        c[i]=1-c[i]
        score=evaluator(c)
        if score<base:
            bests.append(c)
    return bests


def random_flip_k(node,k=3):
    """Return up to k random distinct single-variable flips (subset of flip_all)."""
    import random
    indices=list(range(len(node)))
    random.shuffle(indices)
    children=[]
    for i in indices[:k]:
        c=node[:]
        c[i]=1-c[i]
        children.append(c)
    return children


def single_improving_flip(node,evaluator):
    """Return list with best improving single flip (or empty list if none)."""
    base=evaluator(node)
    best=None
    best_score=base
    for i in range(len(node)):
        c=node[:]
        c[i]=1-c[i]
        sc=evaluator(c)
        if sc<best_score:
            best_score=sc
            best=c
    return [best] if best is not None else []
