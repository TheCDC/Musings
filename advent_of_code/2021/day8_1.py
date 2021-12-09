from typing import List, Tuple
from collections import Counter

"""
length: digits
0:
1:
2: 1
3: 7
4: 4
5: 2,3,5
6:0,6,9
7:8"""

with open("inputs/day8.txt") as f:
    logs = [
        tuple([tuple(x.split()) for x in l.split(" | ")[:2]]) for l in f.readlines()
    ]


def score(log: Tuple[Tuple[str, ...], Tuple[str, ...]]):
    lens = Counter(len(i) for i in log[1])
    return lens.get(2, 0) + lens.get(3, 0) + lens.get(4, 0) + lens.get(7, 0)


def solve(logs: List[Tuple[Tuple[str, ...], Tuple[str, ...]]]):
    return sum(score(l) for l in logs)


print(solve(logs), sep="\n")
# 301
