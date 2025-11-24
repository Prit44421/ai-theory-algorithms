import sys
import os
# Add parent directory to Python path so we can import from blindSearch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import blindSearch.planning.bfs as bfs_planning

# Map Coloring as configuration CSP, similar style to nQueen

regions = ["WA","NT","SA","Q","NSW","V","T"]
index = {r:i for i,r in enumerate(regions)}

adjacency = {
    index['WA'] : [index['NT'], index['SA']],
    index['NT'] : [index['WA'], index['SA'], index['Q']],
    index['SA'] : [index['WA'], index['NT'], index['Q'], index['NSW'], index['V']],
    index['Q']  : [index['NT'], index['SA'], index['NSW']],
    index['NSW']: [index['Q'], index['SA'], index['V']],
    index['V']  : [index['SA'], index['NSW']],
    index['T']  : []
}

colors = [1,2,3]  # 3 colors

start_node = [0]*len(regions)  # 0 = uncolored


def is_safe(state, region, color):
    for nb in adjacency[region]:
        if state[nb] == color:
            return False
    return True


def movegen(state):
    # choose first uncolored region
    if 0 not in state:
        return []
    r = state.index(0)
    children = []
    for c in colors:
        if is_safe(state, r, c):
            new_state = state[:]
            new_state[r] = c
            children.append(new_state)
    return children


def goal_test(state):
    if 0 in state:
        return False
    for r, nbs in adjacency.items():
        for nb in nbs:
            if state[r] == state[nb]:
                return False
    return True


solution = bfs_planning.bfs_closed(start_node, movegen, goal_test)

if not solution:
    print("No solution found")
else:
    print(f"\nMap Coloring CSP Solution Path Length: {len(solution)}\n")
    final = solution[-1]
    assign = {regions[i]: final[i] for i in range(len(regions))}
    print("Final assignment:", assign)
