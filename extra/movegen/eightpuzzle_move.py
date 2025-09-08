"""8-Puzzle move generators.

Representation: flat list length 9, row-major, 0 is blank.

Functions:
    standard_moves(node)  -> legal single blank moves.
    bidirectional_moves   -> alias of standard (useful for naming consistency).
    random_shuffle_moves  -> perform k random moves forward producing a trajectory list.
    prefer_corner_moves   -> like standard but children ordered prioritizing moves that place blank in a corner.
"""

ADJ_MOVES = [-3,3,-1,1]

def standard_moves(node):
    children=[]
    zero=-1
    for i,v in enumerate(node):
        if v==0:
            zero=i
            break
    for mv in ADJ_MOVES:
        nz=zero+mv
        if 0<=nz<9:
            if mv==-1 and zero%3==0:
                continue
            if mv==1 and zero%3==2:
                continue
            new=node[:]
            new[zero],new[nz]=new[nz],new[zero]
            children.append(new)
    return children


def bidirectional_moves(node):
    """Same as standard (alias for clarity in algorithms)."""
    return standard_moves(node)


def random_shuffle_moves(node,k=5):
    import random
    out=[]
    base=node
    for _ in range(k):
        succs=standard_moves(base)
        if not succs:
            break
        base=random.choice(succs)
        out.append(base)
    return out


def prefer_corner_moves(node):
    """Return standard moves ordered so resulting blank position corners come first."""
    succs=standard_moves(node)
    corners={0,2,6,8}
    scored=[]
    for s in succs:
        blank=s.index(0)
        score=0 if blank in corners else 1
        scored.append((score,s))
    scored.sort(key=lambda x:x[0])
    return [s for _,s in scored]
