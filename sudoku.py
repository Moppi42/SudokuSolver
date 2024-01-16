import time
from copy import deepcopy
from itertools import chain

BOARD: list[int] = [
    5, 3, 0, 0, 7, 0, 0, 0, 0,  #
    6, 0, 0, 1, 9, 5, 0, 0, 0,  #
    0, 9, 8, 0, 0, 0, 0, 6, 0,  #
    8, 0, 0, 0, 6, 0, 0, 0, 3,  #
    4, 0, 0, 8, 0, 3, 0, 0, 1,  #
    7, 0, 0, 0, 2, 0, 0, 0, 6,  #
    0, 6, 0, 0, 0, 0, 2, 8, 0,  #
    0, 0, 0, 4, 1, 9, 0, 0, 5,  #
    0, 0, 0, 0, 8, 0, 0, 7, 9,  #
]


def get_row_items(board: list[int], index: int) -> set[int]:
    row_start = index - (index % 9)
    return set(board[row_start:row_start + 9])


def get_col_items(board: list[int], index: int) -> set[int]:
    col_index = index % 9
    return set(board[col_index::9])


def get_block_items(board: list[int], index: int) -> set[int]:
    row, col = divmod(index, 9)
    # row = index // 9
    # col = index % 9
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    start_index = row_start * 9 + col_start

    return set(chain(
        board[start_index:start_index + 3],
        board[start_index + 9:start_index + 12],
        board[start_index + 18:start_index + 21]
    ))


_ALL_NUMBERS = set(range(1, 10))


def get_possible_items_old(board: list[int], index: int) -> set[int]:
    row_items = get_row_items(board, index)
    col_items = get_col_items(board, index)
    block_items = get_block_items(board, index)

    global _ALL_NUMBERS
    return _ALL_NUMBERS - row_items - col_items - block_items


def get_possible_items(board: list[int], index: int) -> set[int]:
    row_index, col_index = divmod(index, 9)
    row_start = row_index * 9

    block_start_row = (row_index // 3) * 3
    block_start_col = (col_index // 3) * 3
    start_index = block_start_row * 9 + block_start_col

    global _ALL_NUMBERS
    return _ALL_NUMBERS - set(
        chain(
            board[row_start:row_start + 9],
            board[col_index::9],
            board[start_index:start_index + 3],
            board[start_index + 9:start_index + 12],
            board[start_index + 18:start_index + 21]
        )
    )


def get_holes(board: list[int]) -> list[int]:
    return [idx for idx, value in enumerate(board) if value == 0]


def solve_helper(output_board: list[int], holes: list[int], depth: int) -> bool:
    if depth >= len(holes):
        return True

    hole_index = holes[depth]
    possible_numbers = get_possible_items(output_board, hole_index)
    for number in possible_numbers:
        output_board[hole_index] = number
        if solve_helper(output_board, holes, depth + 1):
            return True

    output_board[hole_index] = 0
    return False


def solve(board: list[int]) -> list[int]:
    output_board = deepcopy(board)
    holes = get_holes(board)
    solve_helper(output_board, holes, 0)
    return output_board


def print_board(board: list[int]) -> None:
    for row in range(9):
        start = row * 9
        print(", ".join(str(x) for x in board[start: start + 9]))


import timeit

print(timeit.timeit("solve(BOARD)", setup="from __main__ import solve, BOARD", number=10000))
