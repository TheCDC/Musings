from typing import List, NewType, Tuple
from functools import reduce

PointType = NewType("PointType", Tuple[int, int])
GridType = NewType(
    "GridType",
    Tuple[Tuple[int, ...], ...],
)


def fold(grid: GridType, position: int, axis_along: str) -> GridType:
    if axis_along == "x":
        grid = tuple(zip(*grid))
    newgrid = [(r[:]) for r in grid]
    sub1 = grid[:position]
    sub2 = tuple(reversed(grid[position + 1 :]))
    assert len(sub2) == len(sub1)
    assert len(sub2[0]) == len(sub1[0])
    out = tuple(
        [
            tuple([max(col, sub2[irow][icol]) for icol, col in enumerate(row)])
            for irow, row in enumerate(sub1)
        ]
    )
    if axis_along == "x":
        out = tuple(zip(*out))
    return out


def create_grid(points: List[PointType]) -> GridType:
    xx, yy = reduce(lambda a, b: (max(a[0], b[0]), max(a[1], b[1])), points, points[0])
    ps = set(points)
    return tuple(
        [
            tuple([1 if (x, y) in ps else 0 for x in range(xx + 1)])
            for y in range(yy + 1)
        ]
    )


def count_points(grid):
    return len([(ix, iy) for iy, y in enumerate(grid) for ix, x in enumerate(y) if x])


with open("inputs/day13.txt") as f:
    points = []
    instructions: List[Tuple[str, int]] = []
    for line in f:
        if "," in line:
            s = [int(i) for i in line.split(",")]
            points.append((s[0], s[1]))
        elif "fold" in line:
            s = line.split("=")
            instructions.append((s[0][-1], int(s[1])))


def main():
    print(max(x[0] for x in points), max(x[1] for x in points))
    grid = create_grid(points)
    print(count_points(grid))
    folded = fold(grid, instructions[0][1], axis_along=instructions[0][0])
    print(count_points(folded))
    # print(*folded, sep="\n")
    # print(*grid, sep="\n")


if __name__ == "__main__":
    main()
