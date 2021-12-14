with open("inputs/day10.txt") as f:
    lines = f.read().split()

openers = "([{<"
closers = ")]}>"
points = {")": 3, "]": 57, "}": 1197, ">": 25137}


def main():
    score_total = 0
    for iline, line in enumerate(lines):
        chars = list(reversed(line))
        s = [chars.pop()]
        score_line = 0
        while chars:
            c = chars.pop()
            if c in openers:
                s.append(c)
            else:
                if closers.find(c) == openers.find(s[-1]):
                    s.pop()
                else:
                    score_line += points[c]
                    print(iline, c, s[-1])
                    break
                    # error state
        score_total += score_line
    print(score_total)


if __name__ == "__main__":
    main()
