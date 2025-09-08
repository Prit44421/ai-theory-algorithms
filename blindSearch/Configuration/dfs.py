def dfs(start_state,movegen,goal_test):
    open=[start_state]
    while open:
        node = open[0]
        open = open[1:]
        if goal_test(node):
            return node
        else:
            open=movegen(node)+open
    return False

def dfs_closed(start_state,movegen,goal_test):
    open=[start_state]
    closed=[]
    while open:
        node = open[0]
        open = open[1:]
        closed.append(node)
        if goal_test(node):
            return node
        else:
            childs=movegen(node)
            childs=[child for child in childs if child not in closed and child not in open]
            open=childs+open
    return False