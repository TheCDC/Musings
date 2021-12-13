from typing import List, Set, Tuple, TypeVar
from day9_1 import grid, get_neigbors, get_lowpoints, GridType

PointType = TypeVar("PointType", bound=Tuple[int, int])


def get_neigbor_coords(grid: List[List[int]], x: int, y: int) -> List[Tuple[int, int]]:
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for o in offsets:
        xx = x + o[0]
        yy = y + o[1]
        if 0 <= xx and 0 <= yy:
            try:
                grid[yy][xx]
                neighbors.append((xx, yy))
            except IndexError:
                pass
    return neighbors


def fill_lowpoint(
    grid: List[List[int]],
    start: Tuple[int, int],
) -> Set[Tuple[int, int]]:
    filled = set()
    frontier = set([start])
    while True:
        if len(frontier) == 0:
            return filled
        neighbors_next = set(
            [
                n
                for f in frontier
                for n in get_neigbor_coords(grid, f[0], f[1])
                if grid[n[1]][n[0]] < 9 and not (n in filled)
            ]
        )
        filled = filled | neighbors_next
        frontier = neighbors_next
    return filled


def find_basins(
    grid: List[List[int]], lowpoints: List[Tuple[int, int]]
) -> List[List[Tuple[int, int]]]:
    if len(lowpoints) == 0:
        return []
    mine = list(fill_lowpoint(grid, lowpoints[0]))
    sub = find_basins(grid, lowpoints[1:])
    return [mine] + sub


def product(l):
    p = 1
    for i in l:
        p *= i
    return p


def main():
    lps = list(get_lowpoints(grid))
    basins = find_basins(grid, [(p[1], p[2]) for p in lps])
    by_len = [len(x) for x in basins]
    top = sorted(by_len, reverse=True)[:3]
    print(len(basins), top, product(top), sep="\n")


if __name__ == "__main__":
    main()
