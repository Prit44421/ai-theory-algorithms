"""Missionaries & Cannibals move generators.

State: [M_left, C_left, Boat_side] with totals = 3.
Functions:
    valid(m_left,c_left) -> safety test.
    generate(node)       -> all legal moves.
    heuristic_generate(node) -> legal moves ordered: (1,1),(2,0),(0,2),(1,0),(0,1) preference.
"""
TOTAL=3
MOVES=[(1,0),(2,0),(0,1),(0,2),(1,1)]

def valid(m_left,c_left):
    m_right=TOTAL-m_left
    c_right=TOTAL-c_left
    if m_left<0 or c_left<0 or m_right<0 or c_right<0: return False
    if m_left>0 and c_left>m_left: return False
    if m_right>0 and c_right>m_right: return False
    return True


def generate(node):
    m_left,c_left,boat=node
    direction=-1 if boat==0 else 1
    next_boat=1-boat
    children=[]
    for dm,dc in MOVES:
        nm_left=m_left+direction*dm
        nc_left=c_left+direction*dc
        if valid(nm_left,nc_left):
            children.append([nm_left,nc_left,next_boat])
    uniq=[]
    seen=set()
    for c in children:
        t=tuple(c)
        if t not in seen:
            seen.add(t)
            uniq.append(c)
    return uniq


def heuristic_generate(node):
    order=[(1,1),(2,0),(0,2),(1,0),(0,1)]
    m_left,c_left,boat=node
    direction=-1 if boat==0 else 1
    next_boat=1-boat
    children=[]
    for dm,dc in order:
        nm_left=m_left+direction*dm
        nc_left=c_left+direction*dc
        if valid(nm_left,nc_left):
            children.append([nm_left,nc_left,next_boat])
    return children
