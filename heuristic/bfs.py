def findLink(node,closed):
    for n,p,h in closed:
        if n==node:
            return (n,p,h)
    return None


def reconstruct_path(nodePair,closed):
    node,parent,_=nodePair
    path=[]
    path.append(node)
    while parent is not None:
        path.append(parent)
        node,parent,_=findLink(parent,closed)
    return path[::-1]




def bestfirstsearch(start_node, movegen, goal_test, heuristic):
    open=[(start_node,None,heuristic(start_node))]
    closed=[]
    while open:
        nodePair = open[0]
        node = nodePair[0]
        if goal_test(node):
            return reconstruct_path(nodePair,closed)
        else:
            closed.append(nodePair)
            childs=movegen(node)
            childs=[child for child in childs if child not in [n for n,p,h in closed] and child not in [n for n,p,h in open]]
            child_pair=[(child,node,heuristic(child)) for child in childs]
            child_pair.sort(key=lambda x: x[2])
            open=child_pair+open[1:]
    return False
