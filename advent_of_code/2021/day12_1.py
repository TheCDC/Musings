from collections import Counter
from typing import Dict, List, NewType, Tuple


EdgeType = NewType("EdgeType", Tuple[str, str])
PathType = NewType(
    "PathType",
    Tuple[str, ...],
)
mapping: Dict[str, List[str]] = {}
with open("inputs/day12.txt") as f:
    lines = f.read().split()
    edges = [frozenset(line.split("-")[:2]) for line in lines]
    for line in lines:
        es = line.split("-")[:2]
        mapping.update(
            {
                es[1]: mapping.get(es[1], []) + [es[0]],
                es[0]: mapping.get(es[0], []) + [es[1]],
            }
        )


def node_is_legal(
    path: PathType,
    neighbor: str,
    unique_steps: Counter[str] = None,
    allowed_num_small_cave=1,
):
    path_unique_steps = unique_steps if unique_steps else Counter(path)

    if neighbor == "start":
        return False
    if neighbor == "end":
        return True
    if neighbor.islower():

        return path_unique_steps[neighbor] == 0 or (
            max(v for k, v in path_unique_steps.items() if k.islower())
            < allowed_num_small_cave
        )
        # return path_unique_steps[neighbor] < allowed_num_small_cave
    if neighbor.isupper():
        return True


def solve(neighbor_mapping: Dict[str, List[str]], neighbor_legality=node_is_legal):
    paths_intermediate: List[PathType] = [(("start",))]
    paths_final: List[PathType] = []
    while paths_intermediate:
        current_path = paths_intermediate.pop()
        tip = current_path[-1]
        if tip == "end":
            paths_final.append(current_path)
            continue
        neighbors = neighbor_mapping[tip]
        path_unique_steps = Counter(current_path)
        paths_next = [
            (current_path + (n,))
            for n in neighbors
            # if (n.upper() == n) or n not in path_unique_steps
            if neighbor_legality(current_path, n, unique_steps=path_unique_steps)
        ]
        paths_intermediate.extend(paths_next)
    return paths_final


def main():
    paths_final = solve(mapping)
    print(len(paths_final))


# 4720 correct first try
if __name__ == "__main__":
    main()
