def best(nodes, heuristic):
    if not nodes:
        return []
    # print(f"Best nodes from {nodes}")
    nodes.sort(key=lambda x: heuristic(x))
    return nodes[0]



def hillClimbing(start_node, movegen, heuristic):
    bestNode=start_node
    nextNode=best(movegen(start_node),heuristic)
    while nextNode and heuristic(nextNode)<heuristic(bestNode):
        print(f"Exploring Node with heuristic {heuristic(bestNode)}: {bestNode}")
        bestNode=nextNode
        nextNode=best(movegen(bestNode),heuristic)
    return bestNode