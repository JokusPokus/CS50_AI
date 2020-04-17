"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

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
    # Compute number of filled spaces
    filled = sum([len(list(filter(None, row))) for row in board])

    # If even number of filled spaces left, X moves, else O.
    return X if filled % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] is None:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_opt = deepcopy(board)
    i, j = action
    if board_opt[i][j] is not None:
        raise ValueError("This action is not possible")
    board_opt[i][j] = player(board_opt)
    return board_opt


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Winner can only exist after at least 5 moves
    if sum([len(list(filter(None, row))) for row in board]) < 5:
        return None

    board_seq = board[0] + board[1] + board[2]
    winning_lines = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]
    for i, j, k in winning_lines:
        if board_seq[i] is not None and board_seq[i] == board_seq[j] == board_seq[k]:
            return board_seq[i]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Return True if there is a winner or all spaces are filled out (i.e., a tie)
    return bool(winner(board)) or sum([len(list(filter(None, row))) for row in board]) == 9


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        return 1
    if winner(board) == "O":
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    factor = 1 if player(board) == "X" else -1
    optimum = float("-inf")

    for action in actions(board):
        new_state = result(board, action)

        if terminal(new_state):
            util = factor * utility(new_state)
        else:
            util = factor * utility(result(new_state, minimax(new_state)))

        if util == 1:
            return action

        if util > optimum:
            optimum = util
            optimal_action = action
    return optimal_action



