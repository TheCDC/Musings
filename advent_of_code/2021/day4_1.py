from dataclasses import dataclass
from typing import List


@dataclass
class MarkedBoard:
    board: List[List[int]]
    marks: List[List[bool]]
    moves: List[int]


with open("inputs/day4.txt") as f:
    moves = [int(i) for i in f.readline().strip().split(",")]
    boards = []
    b = []
    f.readline()
    for line in f:
        line = line.strip()
        if not line:
            boards.append(b)
            b = []
            continue
        b.append(list(map(lambda s: int(s.strip()), line.split())))
# print(moves)
# print(*boards, sep="\n")

state = [
    MarkedBoard(board=b, marks=[[False for _ in b[0]] for _ in b], moves=[])
    for b in boards
]


def check_board(board: MarkedBoard):
    # rows
    rows = any(map(all, board.marks))
    # cols
    cols = any(map(all, list(zip(*board.marks))))
    # diags
    a = all(board.marks[i][i] for i in range(len(board.marks)))
    b = all(board.marks[i][len(board.marks) - 1 - i] for i in range(len(board.marks)))
    return rows or cols or a or b


def apply_move(move: int, board: MarkedBoard):
    newboard = MarkedBoard(
        board=board.board, marks=board.marks, moves=board.moves + [move]
    )
    for y, row in enumerate(board.board):
        for x, col in enumerate(row):
            newboard.marks[y][x] = newboard.marks[y][x] or col == move
    return newboard


def find(
    moves: List[int],
    boards: List[MarkedBoard],
    *,
    depth=0,
):
    won = [b for b in boards if check_board(b)]
    if won or len(moves) == 0:
        return (
            won,
            moves,
            depth,
        )
    move = moves[0]

    return find(
        moves[1:],
        [apply_move(move, b) for b in boards],
        depth=depth + 1,
    )


def get_board_value(board: MarkedBoard):
    return (
        sum(
            [
                col * (not board.marks[y][x])
                for y, row in enumerate(board.board)
                for x, col in enumerate(row)
            ]
        )
        * board.moves[-1]
    )


a = find(moves, state)
print(*a, list(map(get_board_value, a[0])), sep="\n")
