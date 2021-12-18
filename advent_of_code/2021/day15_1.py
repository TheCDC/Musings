from typing import Deque, List, NewType, Optional, Set, Tuple
from collections import deque
from day13_1 import PointType
from dataclasses import dataclass


@dataclass
class PathWithLength:
    cost_total: int
    path: Tuple[PointType, ...]
    path_set: Set[PointType]


with open("inputs/day15.txt") as f:
    grid_real = [[int(i) for i in line.strip()] for line in f.readlines() if line]

with open("inputs/day15_example.txt") as f:
    grid_example = [[int(i) for i in line.strip()] for line in f.readlines() if line]


def is_point_in_grid(grid: List[List[int]], point: PointType):
    return (
        point[1] >= 0
        and point[1] < len(grid)
        and point[0] >= 0
        and point[0] < len(grid[0])
    )


def solve_exhaustive(grid: List[List[int]]):
    offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    paths: Deque[PathWithLength] = deque()
    point_start = PointType((0, 0))
    paths.append(
        PathWithLength(
            cost_total=grid[0][0],
            path=(point_start,),
            path_set={
                point_start,
            },
        )
    )
    path_cheapest: Optional[PathWithLength] = None
    i = 0
    while paths:
        path = paths.pop()
        point = path.path[-1]
        if point == PointType((len(grid[0]) - 1, len(grid) - 1)):
            if not path_cheapest:
                path_cheapest = path
            if path.cost_total < path_cheapest.cost_total:
                path_cheapest = path
        for o in offsets:
            pp = PointType((point[0] + o[0], point[1] + o[1]))
            if is_point_in_grid(grid, pp) and not pp in path.path_set:
                paths.append(
                    PathWithLength(
                        cost_total=path.cost_total + grid[pp[1]][pp[0]],
                        path=path.path + (pp,),
                        path_set=path.path_set
                        | {
                            pp,
                        },
                    )
                )
        i += 1
        if i % 10000 == 0:
            print(i, len(paths), path_cheapest)
    pass


def main():
    print(len(grid_real), len(grid_real[0]))
    solve_exhaustive(grid_example)


if __name__ == "__main__":
    main()
