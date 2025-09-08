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






n=7



start_node = []


def is_safe(node, row, col):
    for prev_row in range(row):
        if node[prev_row] == col or abs(prev_row-row) == abs(node[prev_row]-col):
            return False
    else:
        return True

def movegen(node):
    children=[]
    row=len(node)
    if row>=n:
        return children
    for col in range(n):
        if is_safe(node,row,col):
            new_node=node[:]
            new_node.append(col)
            children.append(new_node)
    return children

def goal_test(node):
    return len(node)==n


# Configuration Problem
# solution=dfs.dfs_closed(start_node,movegen,goal_test)
# solution=bfs.bfs_closed(start_node,movegen,goal_test)

# solution=dfid.dfid(start_node,movegen,goal_test)


# Planning problem

# solution=dfs_planning.dfs_closed(start_node,movegen,goal_test)
solution=bfs_planning.bfs_closed(start_node,movegen,goal_test)

# solution=dfid_planning.dfid(start_node,movegen,goal_test)


print(f"\nSolution Path Length: {len(solution)}\n")

print(f"Solution Path: {solution}")

print("\nSolution Board:")
for r in range(n):
    line=""
    for c in range(n):
        if solution[-1][r]==c:
            line+=" Q "
        else:
            line+=" . "
    print(line)