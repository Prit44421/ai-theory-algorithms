def alpha_beta(node, alpha, beta,evaluate, get_children, is_terminal, maximizing_player=True):
    if is_terminal(node):
        return evaluate(node)
    elif maximizing_player:
        for child in get_children(node, 0):
            alpha = max(alpha, alpha_beta(child, alpha, beta, evaluate, get_children, is_terminal, False))
            if alpha >= beta:
                return beta
        return alpha
    else:
        for child in get_children(node, 1):
            beta = min(beta, alpha_beta(child, alpha, beta, evaluate, get_children, is_terminal, True))
            if alpha >= beta:
                return alpha
        return beta