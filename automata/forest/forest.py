# https://www.reddit.com/r/learnpython/comments/b6iu6z/forest_fire_simulation_program_help/
import random
import enum
import copy


class CellStates(enum.Enum):
    # pond='🌊'
    # tree='🌳'
    # ash='💀'
    # fire='🔥'
    pond = 'p'
    tree = 't'
    ash = 'a'
    fire = 'f'


def generate_forest(x, y):
    available_states = [CellStates.tree, CellStates.pond]
    forest = [[random.choice(list(available_states))
               for _ in range(x)] for _ in range(y)]
    return forest


def set_fire(forest):
    new_forest = copy.deepcopy(forest)
    y = len(forest)//2
    x = len(forest[0])//2
    new_forest[y][x] = CellStates.fire
    return new_forest


def print_state(f):
    for row in f:
        for cell in row:
            print(cell.value, end='')
        print()


def next_state(forest):
    adjacent_offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    next_frame = copy.deepcopy(forest)
    for y in range(len(forest)):
        for x in range(len(forest[0])):
            cell = forest[y][x]
            if cell == CellStates.tree:
                for offset in adjacent_offsets:
                    try:
                        neighbor = forest[y+offset[1]][x+offset[0]]
                    except IndexError:
                        continue

                    if neighbor == CellStates.fire:
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