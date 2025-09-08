"""Water Jug move generators.

State: [x,y] amounts in jug A (cap a_cap) and jug B (cap b_cap).

Functions:
    classic_moves(node,a,b) -> all legal primitive operations (fill, empty, pour).
    greedy_toward(target)   -> wrapper producing children ordered by proximity to target.
"""


def classic_moves(node,a_cap,b_cap):
    x,y=node
    children=[]
    # fill
    if x<a_cap: children.append([a_cap,y])
    if y<b_cap: children.append([x,b_cap])
    # empty
    if x>0: children.append([0,y])
    if y>0: children.append([x,0])
    # pour A->B
    if x>0 and y<b_cap:
        amt=min(x,b_cap-y)
        children.append([x-amt,y+amt])
    # pour B->A
    if y>0 and x<a_cap:
        amt=min(y,a_cap-x)
        children.append([x+amt,y-amt])
    uniq=[]
    seen=set()
    for c in children:
        t=tuple(c)
        if t not in seen:
            seen.add(t)
            uniq.append(c)
    return uniq


def greedy_toward(node,a_cap,b_cap,target):
    """Return classic moves sorted by min(|x-target|,|y-target|)."""
    moves=classic_moves(node,a_cap,b_cap)
    scored=[]
    for m in moves:
        score=min(abs(m[0]-target),abs(m[1]-target))
        scored.append((score,m))
    scored.sort(key=lambda x:x[0])
    return [m for _,m in scored]
