with open('inputs/day1.txt') as f:
    readings = [int(l) for l in f.read().split()]
windows = [pair
           for pair in zip(readings, readings[1:], readings[2:])]
sums = list(map(sum, windows))
differentials = [sum(pair[0]) < sum(pair[1])
                 for pair in zip(windows, windows[1:])]
print(len(readings), windows[:5], sums[:5],
      differentials[:5], sum(differentials), sep='\n')
