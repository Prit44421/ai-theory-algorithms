def best(nodes, heuristic, beam_width):
    if not nodes:
        return []
    # print(f"Best nodes from {nodes}")
    nodes.sort(key=lambda x: heuristic(x))
    beam_width=min(beam_width,len(nodes))
    return nodes[:beam_width]



def beamSearch(start_node, movegen, heuristic, beam_width=3,max_steps=100):
    bestNode=start_node
    bestNodes=best(movegen(start_node),heuristic,beam_width)
    closed=set()
    closed.add(tuple(start_node))
    step=0
    while bestNodes and step<max_steps:
        step+=1
        print(f"Step: {step} Exploring Nodes: {bestNodes} with best heuristic {heuristic(bestNodes[0])}")
        childrens=[]
        for node in bestNodes:
            childrens.extend(movegen(node))
        childrens=[child for child in childrens if tuple(child) not in closed]
        for child in childrens:
            closed.add(tuple(child))
        bestNodes=best(childrens,heuristic,beam_width)
        if bestNodes and heuristic(bestNodes[0])<heuristic(bestNode):
            bestNode=bestNodes[0]
    return bestNode