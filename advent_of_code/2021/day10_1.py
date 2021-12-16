from typing import List, Optional, Tuple


with open("inputs/day10.txt") as f:
    lines = f.read().split()

openers = "([{<"
closers = ")]}>"
points_corruption = {")": 3, "]": 57, "}": 1197, ">": 25137}


def complete(opens: List[str]):
    to_complete = opens[:]
    completion: List[str] = []
    while to_complete:
        c = to_complete.pop()
        completion.append(closers[openers.find(c)])
    return completion


def score_corruption(s: str):
    return points_corruption[s]


def is_matched_pair(a: str, b: str):
    assert len(a) == 1 and len(b) == 1
    assert a in openers
    assert b in closers
    matching = openers.find(a) == closers.find(b)
    return matching


def doline(line: str):
    chars = list(reversed(list(enumerate(line))))
    left: List[str] = []
    right: List[str] = []
    corrupted: Optional[Tuple[int, str]] = None
    while chars:
        i, c = chars.pop()
        if c in openers:
            left.append(c)
        else:
            right.append(c)
            if not is_matched_pair(left[-1], c):
                corrupted = (i, c) if corrupted is None else corrupted
        while len(left) and len(right) and is_matched_pair(left[-1], right[-1]):
            left.pop()
            right.pop()
    completion = complete(left)
    return (left, right, completion, corrupted)


def solve(lines):
    score_total = 0
    results = [doline(line) for line in lines]
    score_total = sum(score_corruption(cor[1]) for l, r, comp, cor in results if cor)

    return (score_total, results)


def main():
    solved = solve(lines)
    print(
        solved[0],
        *[tuple("".join(x) for x in (t[0], t[1], t[2])) + (t[3],) for t in solved[1]],
        sep="\n"
    )


if __name__ == "__main__":
    main()
