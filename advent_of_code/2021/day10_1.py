from typing import List


with open("inputs/day10.txt") as f:
    lines = f.read().split()

openers = "([{<"
closers = ")]}>"
points = {")": 3, "]": 57, "}": 1197, ">": 25137}


def doline(line: str):
    chars = list(reversed(line))
    left = [chars.pop()]
    right = []
    score_line = None
    while chars:
        c = chars.pop()
        if c in openers:
            left.append(c)
        else:
            if closers.find(c) == openers.find(left[-1]):
                left.pop()
            else:
                score_line = points[c] if score_line is None else score_line
                break
    return (left, right)


def solve(lines):
    score_total = 0
    completion_strings: List[str] = []
    for iline, line in enumerate(lines):
        l, r = doline(line)
        completion_strings.append("".join(r))

    return (score_total, completion_strings)


def main():
    print(solve(lines))


if __name__ == "__main__":
    main()
