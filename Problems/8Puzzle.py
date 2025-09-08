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
import localSearch.hillClimbing as hillclimbing
# represents the starting 8 puzzle board configuration
    # [8, 6, 7]
    # [2, 5, 4]
    # [3, 0, 1]
start_node = [8,6,7,2,5,4,3,0,1]


print("Start Node:")
print(f"{start_node[0:3]}\n{start_node[3:6]}\n{start_node[6:9]}")
print("\n")


def movegen(node):
    childeren=[]
    # find the position of 0
    zero_pos=-1
    for i in range(9):
        if(node[i]==0):
            zero_pos=i
            break
        if(zero_pos!=-1):
            break

    # possible moves: up, down, left, right
    for move in [-3,3,-1,1]:
        new_zero_pos=zero_pos+move
        if(new_zero_pos>=0 and new_zero_pos<9):
            # check for left and right moves
            if(move==-1 and zero_pos%3==0):
                continue
            if(move==1 and zero_pos%3==2):
                continue
            new_node=node[:]
            # swap 0 with the adjacent number
            new_node[zero_pos],new_node[new_zero_pos]=new_node[new_zero_pos],new_node[zero_pos]
            childeren.append(new_node)

    return childeren


def goal_test(node):
    goal=[1,2,3,4,5,6,7,8,0]
    test = (node == goal)
    # print(f"Testing node\n{node[0:3]}\n{node[3:6]}\n{node[6:9]}\n : {test}")
    return test


def heuristic_hamming(node):
    goal=[1,2,3,4,5,6,7,8,0]
    score = 0
    for i in range(9):
        if node[i]!=0 and node[i] != goal[i]:
            score += 1
    return score


def heuristic_manhattan(node):
    goal_positions = {
        1: 0, 2: 1, 3: 2,
        4: 3, 5: 4, 6: 5,
        7: 6, 8: 7, 0: 8
    }
    score = 0
    for i in range(9):
        value = node[i]
        if value != 0:
            goal_index = goal_positions[value]
            score += abs(i//3-goal_index//3) + abs(i%3-goal_index%3)
    return score



# Planning problem

# solution=dfs_planning.dfs_closed(start_node,movegen,goal_test)
solution=bfs_planning.bfs_closed(start_node,movegen,goal_test)

# solution=dfid_planning.dfid(start_node,movegen,goal_test)



#Heuristic Search
# solution=bestfs.bestfirstsearch(start_node,movegen,goal_test,heuristic_hamming)
# solution=bestfs.bestfirstsearch(start_node,movegen,goal_test,heuristic_manhattan)
# solution=hillclimbing.hillClimbing(start_node,movegen,heuristic_hamming)
# solution=hillclimbing.hillClimbing(start_node,movegen,heuristic_manhattan)

# print(f"Final Node with hill climbing heuristic {heuristic_manhattan(solution)}: {solution}")


if not solution:
    print("No solution found")
else:
    print(f"\nSolution Path Length: {len(solution)}\n")

    for i in range(len(solution)):
        step = solution[i]
        print(f"Step: {i+1}\n{step[0:3]}\n{step[3:6]}\n{step[6:9]}\n")
