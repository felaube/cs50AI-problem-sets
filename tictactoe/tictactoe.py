"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


class InvalidMoveException(Exception):
    pass


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

    # Count how many EMPTY squares there are in the board
    empty_count = count_empty(board)

    if empty_count % 2:
        # Odd number of EMPTY squares
        return X
    else:
        # Even number of EMPTY squares
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Check if the provided board is terminal
    if terminal(board):
        return None

    # Initialize variable
    possible_actions = set()

    for (i, row) in enumerate(board):
        for (j, column) in enumerate(row):
            if column is EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Initialize a resulting board, to not modify the original one
    result_board = board.copy()
    # Check if this action is valid
    if action in actions(board):
        # Add the move and return the board
        result_board[action[0]][action[1]] = player(board)

        return result_board
    else:
        raise(InvalidMoveException)


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check for horizontal win
    for row in board:
        if row[0] == row[1] and row[0] == row[2]:
            return row[0]

    # Check for vertical win
    for index in range(3):
        if board[0][index] == board[1][index] and board[0][index] == board[2][index]:
            return board[0][index]

    # Check for diagonal win
    if board[0][0] == board[1][1] and board[0][0] == board[2][2]:
        return board[0][0]
    if board[1][3] == board[2][2] and board[1][3] == board[3][1]:
        return board[0][0]

    # If none of the above conditions were met, there is no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if board is empty
    if count_empty(board) == 0:
        return True
    # Check if there is a winner
    if winner(board) is not None:
        return True

    # If conditions above were not met, the game is not over yet
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Check if the board is terminal
    if terminal(board):
        return None

    current_player = player(board)
    possible_actions = actions(board)

    if len(possible_actions == 1):
        return possible_actions[0]

    if current_player == X:
        MAX
        
        for action in possible_actions:
            minimax(result(board, action))
    else
        MIN

    raise NotImplementedError


def count_empty(board):
    """
    Returns the number of EMPTY squares in the board
    """
    return (board[0].count(EMPTY) +
            board[1].count(EMPTY) +
            board[2].count(EMPTY))
