# https://www.reddit.com/r/computerscience/comments/azbnoh/coding_interview_problem/

"""
There are 'n' people in a circle. Each person has an even number of rocks. At each 'tick', they simultaneously pass half their pile of rocks to the person to their left. After the tick, for any person that has an odd number of rocks, they will receive one additional rock to even out their new pile (so as to avoid fractions of rock to pass around).

Note: The additional rock given to odd piles do not come from any of the people in the circle. It just appears on their pile.

How many ticks does it take till all people have an equal number of rocks in their pile? (if the number of moves is more than 100, than we assume it is "impossible").

Example (this a list of people's stack of rocks at the beginning of simulation, going in clock-wise order):

8 32 10 2 48 34 (17 ticks)

1000 100 10 2 (19 ticks)

I can't seem to think of a way to optimize this, or any way of solving this without just simulating the process (which is a very inefficient way of finding the answer).
"""
from math import ceil
import random


def tick(l):
    """Return the next state of the simulation"""
    buffer = l[:]
    for index, item in enumerate(l):
        buffer[index] = ceil(item/2) + ceil(l[index-1]/2)
    return buffer


def check(l):
    """Check whether a simulation state is terminal."""
    return len(set(l)) == 1


def simulate(l):
    """Step through states until a terminal state is reached."""
    c = 0
    while True:
        yield c, l
        if check(l):
            break
        l = tick(l)
        c += 1


l = [random.randint(1, 100) for i in range(random.randint(3, 20))]
for state in simulate(l):
    print(*state, sep='\t')
