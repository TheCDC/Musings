with open('inputs/day1.txt') as f:
    readings = [int(l) for l in f.read().split()]
differentials = [pair[1] > pair[0] for pair in zip(readings, readings[1:])]
print(differentials[:5], sum(differentials))
