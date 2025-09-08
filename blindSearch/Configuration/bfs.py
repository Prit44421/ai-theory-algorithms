def bfs(start_state,movegen,goal_test):
    open=[start_state]
    while open:
        node = open[0]
        open = open[1:]
        if goal_test(node):
            return node
        else:
            open=open+movegen(node)
    return False


def bfs_closed(start_state,movegen,goal_test):
    open=[start_state]
    closed=[]
    depth=0
    temp=1
    while open:
        if(temp==0):
            depth+=1
            print(f"Exploring depth: {depth}")
            temp=len(open)
        temp-=1
        node = open[0]
        open = open[1:]
        closed.append(node)
        if goal_test(node):
            return node
        else:
            childs=movegen(node)
            childs=[child for child in childs if child not in closed and child not in open]
            open.extend(childs)
    return False