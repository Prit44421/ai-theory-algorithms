def minimax(node, evaluate, get_children, is_terminal, maximizing_player=True):
    if is_terminal(node):
        value = evaluate(node)
    elif maximizing_player:
        player=0
        value = -float('inf')
        for child in get_children(node,player):
            value = max(value, minimax(child, evaluate, get_children, is_terminal, False))
    else:
        player = 1
        value = float('inf')
        for child in get_children(node,player):
            value = min(value, minimax(child, evaluate, get_children, is_terminal, True))
    return value