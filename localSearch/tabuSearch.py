def best(nodes, heuristic):
    if not nodes:
        return []
    # print(f"Best nodes from {nodes}")
    nodes.sort(key=lambda x: heuristic(x))
    return nodes[0]


def tabuSearch(start_node,movegen,heuristic,max_iteration=1000):
    bestNode=start_node
    tabuList=set()
    tabuList.add(tuple(bestNode))
    for k in range(max_iteration):
        allowedNodes=[node for node in movegen(bestNode) if tuple(node) not in tabuList]
        nextNode=best(allowedNodes,heuristic)
        print(f"Iteration {k}, Exploring Node with heuristic {heuristic(nextNode)}: {nextNode}")
        if nextNode and heuristic(nextNode)<heuristic(bestNode):
            bestNode=nextNode
            tabuList.add(tuple(bestNode))
    return bestNode