from minimax import minimax
from alphaBetaPruning import alpha_beta

initial_state=[' ' for _ in range(9)]

def print_board(state):
    for i in range(0, 9, 3):
        print('|'.join(state[i:i+3]))
        print('-' * 5)


def check_winner(state):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    for combo in winning_combinations:
        if state[combo[0]] == state[combo[1]] == state[combo[2]] != ' ':
            return state[combo[0]]
    if all(cell != ' ' for cell in state):
        return 'Draw'
    else:
        return None



def evaluate(state):
    winner = check_winner(state)
    if winner == 'X':
        return 1
    elif winner == 'O':
        return -1
    else:
        return 0
    
def get_children(state,player):
    if player==0:
        player='X'
    else:
        player='O'
    children = []
    for i in range(9):
        if state[i] == ' ':
            new_state = state.copy()
            new_state[i] = player
            children.append(new_state)
    return children



method="alphaBetaPruning"  # Change to "minimax" to use minimax algorithm


human_player='X'
human_turn=True

state=initial_state
while True:
    print_board(state)
    winner = check_winner(state)
    if winner:
        if winner == 'Draw':
            print("It's a draw!")
        else:
            print(f"{winner} wins!")
        break
    if human_turn:
        move = int(input("Enter your move (1-9): ")) - 1
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
            if move < best_value:
                best_value = move
                best_move = child
        if best_move is not None:
            state = best_move
            human_turn = True