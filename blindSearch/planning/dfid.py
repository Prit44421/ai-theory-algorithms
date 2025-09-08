def findLink(node,closed):
    if node == closed[0][0]:
        return closed[0]
    else:
        return findLink(node,closed[1:])


def reconstruct_path(nodePair,closed):
    node,_,parent=nodePair
    path=[]
    path.append(node)
    while parent is not None:
        path.append(parent)
        node,_,parent=findLink(parent,closed)
    return path[::-1]

#depth limited search
def dls(node, movegen, goal_test, depth):
    open=[]
    open.append((node, 0,None))  # (state, current_depth)
    closed=[]
    while open:
        nodePair = open[0]
        node, current_depth, _ = nodePair
        if(goal_test(node)):
            return reconstruct_path(nodePair,closed)
        closed.append(nodePair)
        if current_depth < depth:
            childs=movegen(node)
            childs=[child for child in childs if child not in [n for n,d,p in closed] and child not in [n for n, d, p in open]]
            open=[(child, current_depth + 1, node) for child in childs] + open[1:]
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


