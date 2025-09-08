from collections import deque
def findLink(node,closed):
    node_key=tuple(node)
    if node_key in closed:
        return (node,closed[node_key])
    return None


def reconstruct_path(nodePair,closed):
    node,parent=nodePair
    path=[]
    path.append(node)
    while parent is not None:
        path.append(parent)
        node,parent=findLink(parent,closed)
    return path[::-1]




def dfs_closed(start_state,movegen,goal_test):
    open=deque([(start_state,None)])
    open_set={tuple(start_state)}
    closed={}
    while open:
        nodePair = open.pop()
        node = nodePair[0]
        open_set.remove(tuple(node))

        closed[tuple(node)]=nodePair[1]
        if goal_test(node):
            return reconstruct_path(nodePair,closed)
        else:
            childs=movegen(node)
            childs=[child for child in childs if tuple(child) not in open_set and tuple(child) not in closed]
            open.extend([(child,node) for child in childs])
            open_set.update(tuple(child) for child in childs)
    return False