import sys
import os
# Add parent directory to Python path so we can import from blindSearch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import blindSearch.Configuration.dfs as dfs
import blindSearch.Configuration.bfs as bfs
import blindSearch.Configuration.dfid as dfid


import blindSearch.planning.dfs as dfs_planning
import blindSearch.planning.bfs as bfs_planning
import blindSearch.planning.dfid as dfid_planning

# (x,y) represent current water in jug X (capacity a) and jug Y (capacity b)
# classic example capacities 4 and 3 to get 2 liters or we can parametrize
A_CAP = 4
B_CAP = 3
TARGET = 2   # desired amount in either jug

start_node = [0,0]


def movegen(node):
    children=[]
    x,y=node

    # fill A
    if x < A_CAP:
        children.append([A_CAP,y])
    # fill B
    if y < B_CAP:
        children.append([x,B_CAP])

    # empty A
    if x>0:
        children.append([0,y])
    # empty B
    if y>0:
        children.append([x,0])

    # pour A -> B
    if x>0 and y<B_CAP:
        amount=min(x,B_CAP-y)
        children.append([x-amount,y+amount])

    # pour B -> A
    if y>0 and x<A_CAP:
        amount=min(y,A_CAP-x)
        children.append([x+amount,y-amount])

    # remove duplicates if any
    unique=[]
    seen=set()
    for c in children:
        t=tuple(c)
        if t not in seen:
            seen.add(t)
            unique.append(c)
    return unique


def goal_test(node):
    x,y=node
    return x==TARGET or y==TARGET


# Planning problem (use BFS planning for shortest sequence)
solution=bfs_planning.bfs_closed(start_node,movegen,goal_test)

# solution=dfs_planning.dfs_closed(start_node,movegen,goal_test)
# solution=dfid_planning.dfid(start_node,movegen,goal_test)

if not solution:
    print("No solution found")
else:
    print(f"\nSolution Path Length: {len(solution)}\n")
    for i,state in enumerate(solution):
        print(f"Step {i}: JugA={state[0]} JugB={state[1]}")
