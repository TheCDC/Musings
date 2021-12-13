from typing import List, NewType, Tuple
from functools import reduce
from copy import deepcopy

PointType = NewType("PointType", Tuple[int, int])
GridType = NewType(
    "GridType",
    List[List[int]],
)


def copy_grid(g):
    return [[c for c in r] for r in g]


def fold(grid: GridType, position: int, axis_along: str) -> GridType:
    grid_adjusted = (
        list(map(list, zip(*grid))) if axis_along == "x" else copy_grid(grid)
    )

    sub1 = grid_adjusted[:position]
    sss = grid_adjusted[position + 1 :]
    sub2 = list(reversed(sss + ((len(sub1) - len(sss)) * [[0] * len(sub1[0])])))

    for irow, row in reversed(list(enumerate(sub2))):
        for icol, col in enumerate(row):
            sub1[irow][icol] = max(sub1[irow][icol], col)
    out = list(zip(*copy_grid(sub1))) if axis_along == "x" else copy_grid(sub1)
    return GridType(out)


def create_grid(points: List[PointType]) -> GridType:
    xx, yy = reduce(lambda a, b: (max(a[0], b[0]), max(a[1], b[1])), points, points[0])
    ps = set(points)
    return GridType(
        [([1 if (x, y) in ps else 0 for x in range(xx + 1)]) for y in range(yy + 1)]
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
    grid = create_grid(points)
    folded = fold(grid, instructions[0][1], axis_along=instructions[0][0])
    print(count_points(folded))


if __name__ == "__main__":
    main()
