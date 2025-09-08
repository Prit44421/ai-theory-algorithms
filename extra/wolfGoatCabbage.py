import sys
import os
# Add parent directory to Python path so we can import from blindSearch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import blindSearch.planning.bfs as bfs_planning
# (Farmer, Wolf, Goat, Cabbage) each 0=left,1=right
start_node = [0,0,0,0]


def unsafe(state):
    F,W,G,C = state
    # Wolf and Goat alone
    if W == G and W != F:
        return True
    # Goat and Cabbage alone
    if G == C and G != F:
        return True
    return False


def movegen(node):
    children=[]
    F=node[0]
    # farmer alone
    ns=node[:]
    ns[0]=1-F
    if not unsafe(ns):
        children.append(ns)
    # farmer with one item
    for i in range(1,4):
        if node[i]==F:
            ns=node[:]
            ns[0]=1-F
            ns[i]=1-node[i]
            if not unsafe(ns):
                children.append(ns)
    # dedupe
    uniq=[]
    seen=set()
    for c in children:
        t=tuple(c)
        if t not in seen:
            seen.add(t)
            uniq.append(c)
    return uniq


def goal_test(node):
    return node==[1,1,1,1]

solution=bfs_planning.bfs_closed(start_node,movegen,goal_test)

if not solution:
    print("No solution found")
else:
    labels=["Farmer","Wolf","Goat","Cabbage"]
    print(f"\nWolf-Goat-Cabbage Solution Path Length: {len(solution)}\n")
    for i,state in enumerate(solution):
        left=[labels[idx] for idx,pos in enumerate(state) if pos==0]
        right=[labels[idx] for idx,pos in enumerate(state) if pos==1]
        print(f"Step {i}: Left={left} | Right={right}")
