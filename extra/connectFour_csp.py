import sys
import os
# Add parent directory to Python path so we can import from blindSearch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import blindSearch.planning.bfs as bfs_planning

# Connect Four as CSP-style search for a winning next move for player 1

ROWS = 6
COLS = 7

# board state: list of ROWS lists, each COLS wide, values: 0 empty, 1 P1, 2 P2

start_board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# small example: pre-fill few moves
start_board[5][3] = 1
start_board[5][2] = 2
start_board[4][3] = 1
start_board[5][4] = 2

start_node = start_board

PLAYER = 1  # we search for a winning move for player 1 only


def copy_board(b):
    return [row[:] for row in b]


def drop_piece(board, col, player):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            board[r][col] = player
            return True
    return False


def legal_moves(board):
    return [c for c in range(COLS) if board[0][c] == 0]


def check_win(board, player):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if all(board[r][c+i] == player for i in range(4)):
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == player for i in range(4)):
                return True
    # diag down-right
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i] == player for i in range(4)):
                return True
    # diag up-right
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i] == player for i in range(4)):
                return True
    return False


def movegen(board):
    if check_win(board, PLAYER):
        return []
    children = []
    for col in legal_moves(board):
        newb = copy_board(board)
        drop_piece(newb, col, PLAYER)
        children.append(newb)
    return children


def goal_test(board):
    return check_win(board, PLAYER)


solution = bfs_planning.bfs_closed(start_node, movegen, goal_test)

if not solution:
    print("No winning move sequence found (within search)")
else:
    print(f"\nConnect Four CSP Solution Path Length: {len(solution)}\n")
    final = solution[-1]
    print("Winning board for Player 1:")
    for r in range(ROWS):
        print(" ".join(str(x) for x in final[r]))
