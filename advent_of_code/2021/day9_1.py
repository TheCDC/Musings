from typing import List, TypeVar


with open("inputs/day9.txt") as f:
    lines = f.read().strip().split("\n")
    grid = [[int(i) for i in line] for line in lines]

GridType = TypeVar("GridType", bound=List[List[int]])


def get_neigbors(grid: GridType, x: int, y: int):
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for o in offsets:
        xx = x + o[0]
        yy = y + o[1]
        if 0 <= xx and 0 <= yy:
            try:
                neighbors.append(grid[yy][xx])
            except IndexError:
                pass
    return neighbors


def is_lowpoint(grid: GridType, x: int, y: int):
    return all(grid[y][x] < n for n in get_neigbors(grid, x, y))


def risk_level(x: int):
    return x + 1


def get_lowpoints(grid):
    return [
        (col, icol, irow)
        for irow, row in enumerate(grid)
        for icol, col in enumerate(row)
        if is_lowpoint(grid, icol, irow)
    ]


def main():
    lowpoints = get_lowpoints(grid)
    print(sum(risk_level(x[0]) for x in lowpoints))
    # print(sum(1 for x in lowpoints if x[0] == 0))


if __name__ == "__main__":
    main()
