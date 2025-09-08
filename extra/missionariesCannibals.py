import sys
import os
# Add parent directory to Python path so we can import from blindSearch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import blindSearch.planning.bfs as bfs_planning

# State representation: [M_left, C_left, Boat_side]
# M_left + M_right = 3, C_left + C_right = 3, Boat_side: 0=left,1=right
# Start: all on left -> [3,3,0]
# Goal: all on right -> [0,0,1]

start_node=[3,3,0]
TOTAL=3

moves=[(1,0),(2,0),(0,1),(0,2),(1,1)]  # (missionaries, cannibals) to move


def valid(m_left,c_left):
    m_right=TOTAL-m_left
    c_right=TOTAL-c_left
    if m_left<0 or c_left<0 or m_right<0 or c_right<0:
        return False
    # missionaries not outnumbered on either bank (unless missionaries =0 on that bank)
    if m_left>0 and c_left>m_left:
        return False
    if m_right>0 and c_right>m_right:
        return False
    return True


def movegen(node):
    children=[]
    m_left,c_left,boat=node
    direction = -1 if boat==0 else 1  # if on left, subtract from left; if on right, add back
    next_boat = 1-boat
    for dm,dc in moves:
        nm_left = m_left + direction*dm
        nc_left = c_left + direction*dc
        if valid(nm_left,nc_left):
            children.append([nm_left,nc_left,next_boat])
    # dedupe (not strictly needed)
    uniq=[]
    seen=set()
    for c in children:
        t=tuple(c)
        if t not in seen:
            seen.add(t)
            uniq.append(c)
    return uniq


def goal_test(node):
    return node==[0,0,1]

solution=bfs_planning.bfs_closed(start_node,movegen,goal_test)

if not solution:
    print("No solution found")
else:
    print(f"\nMissionaries & Cannibals Solution Path Length: {len(solution)}\n")
    for i,state in enumerate(solution):
        m_left,c_left,boat=state
        m_right=TOTAL-m_left
        c_right=TOTAL-c_left
        left=f"M:{m_left} C:{c_left}"
        right=f"M:{m_right} C:{c_right}"
        side="Left" if boat==0 else "Right"
        print(f"Step {i}: Left={left} | Right={right} | Boat={side}")
