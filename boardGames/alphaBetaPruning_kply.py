

def alpha_beta_kply(node, alpha, beta,evaluate, get_children, is_terminal, maximizing_player,max_depth,depth=0):
    if depth==max_depth or is_terminal(node):
        return evaluate(node,depth)
    elif maximizing_player:
        for child in get_children(node, 0):
            alpha = max(alpha, alpha_beta_kply(child, alpha, beta, evaluate, get_children, is_terminal, False, max_depth, depth+1))
            if alpha >= beta:
                return beta
        return alpha
    else:
        for child in get_children(node, 1):
            beta = min(beta, alpha_beta_kply(child, alpha, beta, evaluate, get_children, is_terminal, True, max_depth, depth+1))
            if alpha >= beta:
                return alpha
        return beta