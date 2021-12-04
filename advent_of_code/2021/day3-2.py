from collections import Counter

with open("inputs/day3.txt") as f:
    lines = f.read().strip().split()
    nums = [int(l) for l in lines]
lines_most = lines[:]
lines_least = lines[:]


def thing2(index, nums, rank):
    c = Counter([n[index] for n in nums])
    ranking = c.most_common()
    if len(ranking) == 2 and ranking[0][1] == ranking[1][1]:
        if rank == 0:
            return "1"
        else:
            return "0"

    return nums[0][index] if len(nums) == 1 else ranking[rank][0]


def thing(index, list_most, list_least):

    most = thing2(index, list_most, 0)
    least = thing2(index, list_least, 1)
    lines_most = [l for l in list_most if l[index] == most]
    lines_least = [l for l in list_least if l[index] == least]
    return lines_most, lines_least


index = 0
while index < len(lines[0]):
    lines_most, lines_least = thing(index, lines_most, lines_least)
    index += 1

m = int(lines_most[0], 2)
l = int(lines_least[0], 2)
print(
    lines_most,
    lines_least,
    m,
    l,
    m * l,
)
