"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_X = 0
    count_O = 0
    for row in board:
        count_X += row.count(X)
        count_O += row.count(O)
    if count_X == 0 and count_X == 0:
      return X  
    elif count_X > count_O:
        return O
    else:
        return X
    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    avail = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                avail.add((i,j))
    return avail        
    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    changed_board = copy.deepcopy(board)
    player_turn = player(board)
    i,j = action
    try:
        changed_board[i][j] = player_turn
    except:
        raise Exception('Invalid move')
    return changed_board
    # raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        # check horizontal
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
        # check vertical
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]
        # check diagonal
        if (board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]) and board[1][1] != EMPTY:
            return board[1][1]
    return None
    # raise NotImplementedError

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    elif not actions(board):
        return True
    else:
        return False
    # raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    # raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:
        return None
    Max = float('inf')
    Min = float('-inf')
    best_move = None
    if player(board) == X:
        for action in actions(board):
            val = max(Min,min_value(result(board,action)))
            if val > Min:
                Min = val
                best_move = action
        return best_move
    else:
        for action in actions(board):
            val = min(Max,max_value(result(board,action)))
            if val < Max:
                Max = val
                best_move = action
        return best_move
    # raise NotImplementedError

def max_value(state):
    v = float('-inf')
    if terminal(state):
        return utility(state)
    for action in actions(state):
        test = max(v,min_value(result(state,action)))
        if test > v:
            v = test
    return v

def min_value(state):
    v = float('inf')
    if terminal(state):
        return utility(state)
    for action in actions(state):
        test = min(v,max_value(result(state,action)))
        if test < v:
            v = test
    return v