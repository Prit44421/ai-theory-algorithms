import random


def random_walk(start_node,movegen,heuristic,max_steps=1000):
    current_node=start_node
    best_node=start_node
    for step in range(max_steps):
        if movegen(current_node)==[]:
            return current_node
        current_node=random.choice(movegen(current_node))
        if heuristic(current_node)<heuristic(best_node):
            best_node=current_node
    return best_node