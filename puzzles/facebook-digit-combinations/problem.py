from itertools import permutations
from time import time

digit_values = set([0, 1, 2, 4, 6, 8, 9])


def test_solution_candidate(a: int, b: int, c: int,
                            d: int, e: int, f: int, g: int):
    return 100*a + 10*c + b + 573 == 1000*d + 100*e + 10*f + g and (
        set([a, b, c, d, e, f, g]) == digit_values)


def pretty_solution(a: int, b: int, c: int,
                    d: int, e: int, f: int, g: int):
    s = f"""  {a}7{b}
+ 5{c}3
-----
 {d}{e}{f}{g}
"""
    return (s)


time_start = time()
index = None
for index, perm in enumerate(permutations(digit_values)):
    is_match = test_solution_candidate(*perm)
    if is_match:
        print(pretty_solution(*perm))
time_stop = time()
print('Checked', index+1, 'permutations in ', time_stop-time_start,
      'seconds')
