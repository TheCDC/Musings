from typing import Deque, Dict, List, NewType, Optional, Set, Tuple
from collections import deque
from day13_1 import PointType
from dataclasses import dataclass
from util import AdventTimer


@dataclass
class PathWithLength:
    cost_total: int
    path: Tuple[PointType, ...]
    path_set: Set[PointType]


@dataclass
class ProfileStats:
    outside_grid: int = 0
    point_already_traversed: int = 0
    worse_than_best_so_far: int = 0
    worse_than_naive: int = 0
    update_best_known_cost_to_point: int = 0
    new_best_path: int = 0


with open("inputs/day15.txt") as f:
    grid_real = [[int(i) for i in line.strip()] for line in f.readlines() if line]

with open("inputs/day15_example.txt") as f:
    grid_example = [[int(i) for i in line.strip()] for line in f.readlines() if line]


def draw_points_on_grid(grid: List[List[int]], points: Set[PointType]):
    return [
        [
            grid[irow][icol] if (icol, irow) in points else " "
            for icol, col in enumerate(row)
        ]
        for irow, row in enumerate(grid)
    ]


def print_points_in_grid(grid: List[List[int]], points: Set[PointType]):
    print(
        *["".join([str(i) for i in x]) for x in draw_points_on_grid(grid, points)],
        sep="\n",
    )


def is_point_in_grid(grid: List[List[int]], point: PointType):
    return (
        point[1] >= 0
        and point[1] < len(grid)
        and point[0] >= 0
        and point[0] < len(grid[0])
    )


def min_cost_between_points(a: PointType, b: PointType):
    """Min cost of a cell is 1.
    Min cost of a path is min cell cost times path length."""
    return sum(abs(aa - bb) for aa, bb in zip(a, b))


def max_cost_between_points(a: PointType, b: PointType):
    return 9 * min_cost_between_points(a, b)


def solve_exhaustive(grid: List[List[int]], difficulty=None):
    difficulty = difficulty if difficulty is not None else len(grid) - 1
    profile = ProfileStats()
    offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    paths: Deque[PathWithLength] = deque()
    point_start = PointType((len(grid[0]) - 1 - difficulty, len(grid) - 1 - difficulty))
    point_finish = PointType((len(grid[0]) - 1, len(grid) - 1))
    paths.append(
        PathWithLength(
            cost_total=grid[point_start[1]][point_start[0]],
            path=(point_start,),
            path_set={
                point_start,
            },
        )
    )
    path_cheapest: Optional[PathWithLength] = None
    known_cost_start_to_point: Dict[PointType, int] = dict()
    i = 0
    with AdventTimer() as timer:
        while paths:
            path = paths.pop()
            path_tip = path.path[-1]
            ss = 0
            for node in path.path:
                ss += grid[node[1]][node[0]]
                if (
                    ss not in known_cost_start_to_point
                    or ss < known_cost_start_to_point[node]
                ):
                    known_cost_start_to_point[node] = ss
                    profile.update_best_known_cost_to_point += 1
            if path_tip == point_finish:

                if not path_cheapest or path.cost_total < path_cheapest.cost_total:
                    path_cheapest = path
                    print(
                        "new cheapest of length",
                        len(path_cheapest.path),
                        "costs",
                        path_cheapest.cost_total,
                        path_cheapest,
                        "profile",
                        profile,
                    )
                    print_points_in_grid(grid, path_cheapest.path_set)
                    profile.new_best_path += 1
            points_offset = sorted(
                [PointType((path_tip[0] + o[0], path_tip[1] + o[1])) for o in offsets],
                key=lambda p: min_cost_between_points(p, point_finish),
                reverse=True,
            )
            for point_offset in points_offset:
                pp = point_offset
                if not is_point_in_grid(grid, pp):  # point outside grid
                    profile.outside_grid += 1
                    continue
                if pp in path.path_set:  # point already traversed
                    profile.point_already_traversed += 1
                    continue

                path_new = PathWithLength(
                    cost_total=path.cost_total + grid[pp[1]][pp[0]],
                    path=path.path + (pp,),
                    path_set=path.path_set
                    | {
                        pp,
                    },
                )
                if (
                    pp in known_cost_start_to_point
                    and path_new.cost_total > known_cost_start_to_point[pp]
                ):  # worse than the best path from here so far
                    profile.worse_than_best_so_far += 1
                    continue
                if path_new.cost_total > max_cost_between_points(
                    point_start, point_finish
                ):  # this path already costs more than a direct one of all 9s
                    profile.worse_than_naive += 1
                    continue
                if path.cost_total + min_cost_between_points(
                    pp, point_finish
                ) > max_cost_between_points(
                    point_start, point_finish
                ):  # this path can't possibly cost less than the naive one
                    continue
                paths.append(path_new)
            i += 1
            if i % 100000 == 0 or len(paths) == 0:
                print(
                    i,
                    f"{timer.duration:.1f}",
                    len(paths),
                    "cache size",
                    len(known_cost_start_to_point),
                    profile,
                )
    return path_cheapest


def main():
    print(len(grid_real), len(grid_real[0]))
    for g in [grid_example, grid_real]:
        s = solve_exhaustive(g, difficulty=None)
        print(s)
        if s:
            print_points_in_grid(grid_real, s.path_set)


if __name__ == "__main__":
    main()
