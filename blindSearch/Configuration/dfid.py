

#depth limited search
def dls(node, movegen, goal_test, depth):
    open=[]
    open.append((node, 0))  # (state, current_depth)
    closed=[]
    while open:
        nodePair = open[0]
        node, current_depth = nodePair
        if(goal_test(node)):
            return node
        closed.append(node)
        if current_depth < depth:
            childs=movegen(node)
            childs=[child for child in childs if child not in closed and child not in [n for n, d in open]]
            open=[(child, current_depth + 1) for child in childs] + open[1:]
        else:
            open=open[1:]   
    return False





def dfid(start_state, movegen, goal_test):
    depth = 0
    while True:
        print(f"Exploring depth: {depth}")
        result = dls(start_state, movegen, goal_test, depth)
        if result is not False:
            return result
        depth += 1


