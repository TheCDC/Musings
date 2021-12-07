from functools import reduce
from typing import List, Tuple


def sign(x: int):
    if x == 0:
        return 0
    return -1 if x < 0 else 1


with open("inputs/day5.txt") as f:
    lines = f.readlines()
linepoints = [
    tuple(tuple(list(map(int, x.split(",")))[:2])[:2] for x in line.split(" -> "))
    for line in lines
]

maxs = reduce(
    lambda a, b: (max(a[0], b[0]), max(a[1], b[1])),
    [j for i in linepoints for j in i],
    linepoints[0][0],
)

# print(linepoints)
print(maxs)

heightmap = [[0 for _ in range(maxs[0])] for _ in range(maxs[1])]


def apply_lines(
    heightmap: List[List[int]],
    lines: List[Tuple[Tuple[int, int], Tuple[int, int]]],
    depth=0,
):
    if len(lines) == 0:
        return heightmap
    line = lines[0]
    pos = line[0]
    diff = (
        sign(line[1][0] - pos[0]),
        sign(line[1][1] - pos[1]),
    )  # needs to include ends
    while [d for d in diff if d != 0]:
        heightmap[pos[1]][pos[0]] += 1
        pos = (pos[0] + diff[0], pos[1] + diff[1])
        diff = (
            sign(line[1][0] - pos[0]),
            sign(line[1][1] - pos[1]),
        )  # needs to include ends
    return apply_lines(heightmap, lines[1:], depth=depth + 1)


state_final = apply_lines(
    heightmap, [l for l in linepoints if l[0][0] == l[1][0] or l[0][1] == l[1][1]]
)
matching_cells = [col for row in state_final for col in row if col > 1]
print(len(matching_cells))

# 23222 high
# 5566 low
