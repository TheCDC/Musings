from collections import Counter
from typing import Dict

with open("inputs/day6.txt") as f:
    nums = list(map(int, f.readline().split(",")))

initial = Counter(nums)


def step(c: Dict):
    keys = c.keys()
    out = dict()
    for k, v in c.items():
        if k == 0:
            out.update({6: out.get(6, 0) + v})
            out.update({8: out.get(8, 0) + v})
        else:
            out.update({k - 1: out.get(k - 1, 0) + v})
    return out


def sim(state: Dict[int, int], steps=80) -> Dict[int, int]:
    if steps == 0:
        return state
    return sim(step(state), steps=steps - 1)


print(initial, step(initial))
print(sum(sim(initial, steps=256).values()))
