import sys
import os
# Add parent directory to Python path so we can import from blindSearch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import blindSearch.planning.bfs as bfs_planning

# Map Coloring Problem (example: Australia map)
# Regions: WA, NT, SA, Q, NSW, V, T
# Edges (adjacency):
# WA-NT, WA-SA, NT-SA, NT-Q, SA-Q, SA-NSW, SA-V, Q-NSW, NSW-V

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

colors = [1,2,3]  # 3-coloring (represent e.g., Red=1, Green=2, Blue=3)

start_node = [0]*len(regions)  # 0 = uncolored

# import move generators
override_movegen = None
try:
    from ai.movegen import mapcolor_move as mc_move
    def movegen(node):
        # use MRV heuristic expansion
        return mc_move.mrv_expand(node, adjacency, colors)
except ImportError:
    def movegen(node):
        # fallback simple expansion
        if 0 not in node: return []
        r=node.index(0)
        childs=[]
        for c in colors:
            new=node[:]
            new[r]=c
            childs.append(new)
        return childs


def goal_test(node):
    if 0 in node:
        return False
    for r, neighbors in adjacency.items():
        for n in neighbors:
            if node[r]==node[n]:
                return False
    return True

solution = bfs_planning.bfs_closed(start_node, movegen, goal_test)

if not solution:
    print("No solution found")
else:
    print(f"\nMap Coloring Solution Path Length: {len(solution)}\n")
    for i,state in enumerate(solution):
        assign = {regions[idx]:state[idx] for idx in range(len(state))}
        print(f"Step {i}: {assign}")
