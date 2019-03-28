# https://www.reddit.com/r/learnpython/comments/b6iu6z/forest_fire_simulation_program_help/
import random
import enum
import copy
import math

class CellStates(enum.Enum):
    pond = 'p'
    tree = 't'
    ash = 'a'
    fire = 'f'

adjacent_offsets = [
    (-1, 1), (0, 1), (1, 1),
    (-1, 0), (0, 0), (1, 0),
    (-1, -1), (0, -1), (1, -1)
]

def generate_forest(x, y, tree_density=0.8):
    available_states = [CellStates.tree, CellStates.pond]
    forest = [[random.choices(list(available_states), [tree_density, 1-tree_density])[0]
               for _ in range(x)] for _ in range(y)]
    return forest


def set_fire(forest):
    new_forest = copy.deepcopy(forest)
    num_fires  = random.randint(1,math.ceil(len(forest)**(1/2)))
    for i in range(num_fires):
        y = random.randrange(len(forest))
        x = random.randrange(len(forest[y]))
        new_forest[y][x] = CellStates.fire
    return new_forest


def print_state(f):
    for row in f:
        for cell in row:
            print(cell.value, end='')
        print()


def next_state(forest, spread_chance=0.75):

    next_frame = copy.deepcopy(forest)
    for y in range(len(forest)):
        for x in range(len(forest[0])):
            cell = forest[y][x]
            if cell == CellStates.tree:
                for offset in adjacent_offsets:
                    if x+offset[0] < 0 or y+offset[1] < 0:
                        continue
                    try:
                        neighbor = forest[y+offset[1]][x+offset[0]]
                    except IndexError:
                        continue

                    if neighbor == CellStates.fire and random.random() <= spread_chance:
                        next_frame[y][x] = CellStates.fire
                        break
            if cell == CellStates.fire:
                next_frame[y][x] = CellStates.ash

    return next_frame


def main():
    f = generate_forest(10, 10)
    print_state(f)
    f = set_fire(f)
    print_state(f)
    for i in range(10):
        f = next_state(f)
        print_state(f)
        print('===========')


if __name__ == '__main__':
    main()
