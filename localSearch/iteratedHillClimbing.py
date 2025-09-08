def best(nodes, heuristic):
    if not nodes:
        return []
    # print(f"Best nodes from {nodes}")
    nodes.sort(key=lambda x: heuristic(x))
    return nodes[0]



def hillClimbing(start_node, movegen, heuristic, verbose=False):
    bestNode=start_node
    nextNode=best(movegen(start_node),heuristic)
    while nextNode and heuristic(nextNode)<heuristic(bestNode):
        if verbose:
            print(f"Exploring Node with heuristic {heuristic(bestNode)}: {bestNode}")
        bestNode=nextNode
        nextNode=best(movegen(bestNode),heuristic)
    return bestNode


def iteratedHillClimbing(movegen, heuristic, node_generator, max_attempts=10, verbose=False):
    best_node = node_generator()
    for k in range(max_attempts):
        start_node = node_generator()
        print(f"\nStarting new iteration: {k} with start node {start_node} and cost {heuristic(start_node)}")
        current_best=hillClimbing(start_node, movegen, heuristic, verbose)
        if heuristic(current_best)<heuristic(best_node):
            best_node=current_best
    return best_node