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

# heuristic search
import heuristic.bfs as bestfs



start_node=[0,0,0,0,0] # represents (x1,x2,x3,x4,x5) all False

def movegen(node):
    children=[]
    for i in range(len(node)):
        if(node[i]==0):
            children.append(node[:i]+[1]+node[i+1:])
        else:
            children.append(node[:i]+[0]+node[i+1:])
    return children

def goal_test(node):

    # problem (x1∨¬x2)∧(¬x1∨x3)∧(x2∨x4)∧(x3∨¬x5)∧(¬x4∨¬x5)
    test = bool(
            (node[0] or not node[1]) and
            (not node[0] or node[2]) and
            (node[1] or node[3]) and
            (node[2] or not node[4]) and
            (not node[3] or not node[4])
        )


    print(f"Testing node {node} : {test}")
    return test

def heuristic(node):
    # number of clauses satisfied
    score = 0
    if (node[0] or not node[1]):
        score += 1
    if (not node[0] or node[2]):
        score += 1
    if (node[1] or node[3]):
        score += 1
    if (node[2] or not node[4]):
        score += 1
    if (not node[3] or not node[4]):
        score += 1
    return len(node)-score  



# Configuration Problem

# Without Closed
# solution=dfs.dfs(start_node,movegen,goal_test)
# solution=bfs.bfs(start_node,movegen,goal_test)

# With Closed
# solution=dfs.dfs_closed(start_node,movegen,goal_test)
# solution=bfs.bfs_closed(start_node,movegen,goal_test)

# solution=dfid.dfid(start_node,movegen,goal_test)


# Planning problem

# solution=dfs_planning.dfs_closed(start_node,movegen,goal_test)
# solution=bfs_planning.bfs_closed(start_node,movegen,goal_test)

# solution=dfid_planning.dfid(start_node,movegen,goal_test)



#Heuristic Search
solution=bestfs.bestfirstsearch(start_node,movegen,goal_test,heuristic)


print(f"\nSolution Path Length: {len(solution)}\n")


print(solution)