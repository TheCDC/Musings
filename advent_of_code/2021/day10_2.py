from typing import Iterable
from day10_1 import openers, closers, points_corruption, solve, lines, score_corruption

points_completion = {")": 1, "]": 2, "}": 3, ">": 4}


def score_completion_string(s: Iterable[str]):
    score = 0
    for c in s:
        m = score * 5
        p = points_completion[c]
        score = m + p
    return score


def main():
    print(score_completion_string("])}>"))
    scores = sorted(
        [
            (score_completion_string(comp), comp)
            for l, r, comp, cor in solve(lines)[1]
            if not cor
        ],
        key=lambda t: t[0],
    )
    idx_middle = (len(scores)) // 2
    print(
        len(scores),
        idx_middle,
        scores[0][0],
        scores[-1][0],
        scores[idx_middle],
        scores[idx_middle][0],
    )


# 31512 low
# 112462872 low
# 2473213032888 high
# 5700215539 wrong
# 4001832844
if __name__ == "__main__":
    main()
