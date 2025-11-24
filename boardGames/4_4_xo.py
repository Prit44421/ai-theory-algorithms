from minimax import minimax
from alphaBetaPruning import alpha_beta
from alphaBetaPruning_kply import alpha_beta_kply

initial_state=[' ' for _ in range(16)]

def print_board(state):
    for i in range(0, 16, 4):
        print('|'.join(state[i:i+4]))
        print('-' * 7)


winning_combinations = [
        # Rows
        [0, 1, 2], [1, 2, 3], [4, 5, 6], [5, 6, 7],
        [8, 9, 10], [9, 10, 11], [12, 13, 14], [13, 14, 15],
        # Columns
        [0, 4, 8], [4, 8, 12], [1, 5, 9], [5, 9, 13],
        [2, 6, 10], [6, 10, 14], [3, 7, 11], [7, 11, 15],
        # Diagonals
        [0, 5, 10], [1, 6, 11], [4, 9, 14], [5, 10, 15],
        [3, 6, 9], [2, 5, 8], [7, 10, 13], [6, 9, 12]
    ]

def check_winner(state):
    
    for combo in winning_combinations:
        if state[combo[0]] == state[combo[1]] == state[combo[2]] != ' ':
            return state[combo[0]]
    if all(cell != ' ' for cell in state):
        return 'Draw'
    else:
        return None


"""
def evaluate(state,depth=0):
    winner = check_winner(state)
    if winner == 'X':
        return 1
    elif winner == 'O':
        return -1
    else:
        return 0
"""
def evaluate(state, depth):
    winner = check_winner(state)
    if winner == 'X':
        return 100 - depth*5  # Prefer faster wins (higher value at lower depth)      
    if winner == 'O':
        return -100 + depth*5  # Prefer faster wins (more negative at lower depth)
    if winner == 'Draw':
        return 0

    # heuristic: count open lines
    score = 0
    for combo in winning_combinations:
        line = [state[i] for i in combo]

        if 'X' in line and 'O' in line:
            continue  # blocked line

        if 'X' in line:
            score += 3 ** line.count('X')
        if 'O' in line:
            score -= 3 ** line.count('O')

    return score
# """
    
def get_children(state,player):
    if player==0:
        player='X'
    else:
        player='O'
    children = []
    for i in range(16):
        if state[i] == ' ':
            new_state = state.copy()
            new_state[i] = player
            children.append(new_state)
    return children



method="alphaBetaPruning_kply"

human_player='X'
human_turn=True

state=initial_state
while True:
    print_board(state)
    print("Evaluated Score:", evaluate(state,0))
    winner = check_winner(state)
    if winner:
        if winner == 'Draw':
            print("It's a draw!")
        else:
            print(f"{winner} wins!")
        break
    if human_turn:
        move = int(input("Enter your move (1-16): ")) - 1
        if state[move] == ' ':
            state[move] = human_player
            human_turn = False
        else:
            print("Invalid move. Try again.")
    else:
        print("Computer is making a move...")
        childerens=get_children(state,1)
        best_move=None
        best_value = float('inf')
        for child in childerens:
            if method=="minimax":
                move=minimax(child,evaluate,get_children,check_winner, maximizing_player=True)
            if method=="alphaBetaPruning":
                move=alpha_beta(child, -float('inf'), float('inf'), evaluate, get_children, check_winner, maximizing_player=True)
            if method=="alphaBetaPruning_kply":
                move=alpha_beta_kply(child, -float('inf'), float('inf'), evaluate, get_children, check_winner, maximizing_player=True,max_depth=7)
            if move < best_value:
                best_value = move
                best_move = child
        if best_move is not None:
            state = best_move
            human_turn = True