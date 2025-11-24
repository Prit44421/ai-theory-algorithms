import sys
import os
# Add parent directory to Python path so we can import from blindSearch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import blindSearch.planning.bfs as bfs_planning

# Simple job scheduling CSP in nQueen style
# Jobs must be assigned non-overlapping time slots on one machine

jobs = ["J1","J2","J3"]
index = {j:i for i,j in enumerate(jobs)}

# discrete time slots 0..3
slots = [0,1,2,3]

start_node = [-1]*len(jobs)  # -1 = unassigned slot


def is_safe(state, job_idx, slot):
    # no two jobs share the same slot
    for i, s in enumerate(state):
        if i != job_idx and s == slot:
            return False
    return True


def movegen(state):
    if -1 not in state:
        return []
    j = state.index(-1)
    children = []
    for s in slots:
        if is_safe(state, j, s):
            new_state = state[:]
            new_state[j] = s
            children.append(new_state)
    return children


def goal_test(state):
    if -1 in state:
        return False
    # all slots distinct already guaranteed by is_safe
    return True


solution = bfs_planning.bfs_closed(start_node, movegen, goal_test)

if not solution:
    print("No schedule found")
else:
    print(f"\nJob Scheduling CSP Solution Path Length: {len(solution)}\n")
    final = solution[-1]
    assign = {jobs[i]: final[i] for i in range(len(jobs))}
    print("Final schedule (job -> slot):", assign)
