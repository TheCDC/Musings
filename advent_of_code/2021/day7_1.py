from collections import Counter
from typing import Callable, Dict

with open("inputs/day7.txt") as f:
    nums = list(map(int, f.readline().split(",")))

counts = Counter(nums)


def linear_cost(x: int) -> int:
    return x


def score(position, counts: Dict[int, int], distance_cost: Callable[[int], int]) -> int:
    return sum(distance_cost(abs(k - position) * v) for k, v in counts.items())


def solve(nums, distance_cost: Callable[[int], int]):
    c = Counter(nums)
    mi = min(nums)
    ma = max(nums)
    ret = score(0, c, distance_cost=distance_cost)
    for i in range(mi, ma + 1):
        s = score(i, c, distance_cost=distance_cost)
        ret = min(s, ret)
    return ret


if __name__ == "__main__":
    print(
        counts.most_common(10),
        min(nums),
        max(nums),
        solve(nums, distance_cost=linear_cost),
    )
# 335271 Correct
