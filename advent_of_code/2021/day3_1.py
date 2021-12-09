from collections import Counter

with open("inputs/day3.txt") as f:
    lines = f.read().strip().split()
    nums = [int(l) for l in lines]

t = list(zip(*lines))
counters = [Counter(i) for i in t]
digits_least = [Counter(i).most_common()[1][0] for i in t]
digits_most = [Counter(i).most_common()[0][0] for i in t]
gamma = int("".join(digits_most), 2)
epsilon = int("".join(digits_least), 2)
print(
    len(lines),
    lines[:5],
    len(t),
    t[0],
    digits_least,
    gamma,
    digits_most,
    epsilon,
    gamma * epsilon,
    sep="\n",
)
