"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


class InvalidMoveException(Exception):
    """
    Define a custom Exception,
    raised when a invalid move is made 
    """
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
    result_board = deepcopy(board)
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
    if board[0][2] == board[1][1] and board[0][2] == board[2][0]:
        return board[0][2]

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

    optimal_action = None

    # Initialize alpha, to store the best
    # already explored option for the maximizer
    alpha = -math.inf

    # Initialize beta, to store the best
    # already explored option for the minimizer
    beta = math.inf

    if current_player == X:
        # MAX
        value = -math.inf

        for action in possible_actions:
            action_value = min_value(result(board, action), alpha, beta)
            if action_value > value:
                value = action_value
                optimal_action = action
                if value > beta:
                    break
                if value > alpha:
                    alpha = value

    else:
        # MIN
        value = math.inf

        for action in possible_actions:
            action_value = max_value(result(board, action), alpha, beta)
            if action_value < value:
                value = action_value
                optimal_action = action
                if value < alpha:
                    break
                if value < beta:
                    beta = value

    return optimal_action


def max_value(board, alpha, beta):
    """
    Return the maximum utility value that can arise
    from a state given by board, considering optimal play
    """
    if terminal(board):
        return utility(board)

    # Initialize value as low as possible
    value = -math.inf

    for action in actions(board):
        # Call max and min recursively until a terminal state in reached
        action_value = min_value(result(board, action), alpha, beta)
        value = max(value, action_value)
        # Being a maximizer, it is known that the value max_value
        # returns, is gonna be at least the value I just got.
        # Since ultimately I want to minimize the value (max_value
        # was called by min_value), it is not worth to continue
        # searching for other results (prune the tree here)
        if value >= beta:
            break
        if value > alpha:
            alpha = value

    return value


def min_value(board, alpha, beta):
    """
    Return the minimum utility value that can arise
    from a state given by board, considering optimal play
    """
    if terminal(board):
        return utility(board)

    # Initialize value as high as possible
    value = math.inf

    for action in actions(board):
        # Call max and min recursively until a terminal state in reached
        action_value = max_value(result(board, action), alpha, beta)
        value = min(value, action_value)
        if value <= alpha:
            break
        if value < beta:
            beta = value

    return value


def count_empty(board):
    """
    Returns the number of EMPTY squares in the board
    """
    return (board[0].count(EMPTY) +
            board[1].count(EMPTY) +
            board[2].count(EMPTY))
