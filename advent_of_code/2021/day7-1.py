from collections import Counter
from typing import Dict

with open("inputs/day7.txt") as f:
    nums = list(map(int, f.readline().split(",")))

counts = Counter(nums)


def score(position, counts: Dict[int, int]) -> int:
    return sum(abs(k - position) * v for k, v in counts.items())


def solve(nums):
    c = Counter(nums)
    mi = min(nums)
    ma = max(nums)
    ret = score(0, c)
    for i in range(mi, ma + 1):
        s = score(i, c)
        ret = min(s, ret)
    return ret


print(counts.most_common(10), min(nums), max(nums), solve(nums))
# 335271 Correct
