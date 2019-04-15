# https://www.reddit.com/r/learnpython/comments/b6iu6z/forest_fire_simulation_program_help/
import random
import enum
import copy
import math
import numpy as np


class CellStates(enum.Enum):
    pond = 0
    tree = 1
    ash = 3
    fire = 4


adjacent_offsets = [(-1, 1), (0, 1), (1, 1), (-1, 0), (0, 0), (1, 0), (-1, -1),
                    (0, -1), (1, -1)]


class SimulationState:
    def __init__(self, x: int = 10, y: int = 10, tree_density=0.5, **kwargs):
        self.state = set_fire(generate_forest(x, y, tree_density))
        self.touched_coordinates = set(generate_grid_coordinates(self.state))

    def step(self,
             spread_chance: float = 0.75,
             sustain_chance: float = 0.25,
             reignite_chance: float = 0.01,
             **kwargs):
        next_frame = np.copy(self.state)
        last_touched_coordinates = self.touched_coordinates
        self.touched_coordinates = set()
        # print((last_touched_coordinates))
        for x, y in last_touched_coordinates:
            did_touch_cell = False
            cell = self.state[y][x]
            neighbors = set()
            neighbor_coords = list()
            for offset in adjacent_offsets:
                if x + offset[0] < 0 or y + offset[1] < 0:
                    continue
                try:
                    neighbors.add(self.state[y + offset[1]][x + offset[0]])
                    neighbor_coords.append((x + offset[0], y + offset[1]))

                except IndexError:
                    continue
            if cell == CellStates.tree.value:
                if CellStates.fire.value in neighbors:
                    if random.random() <= spread_chance:
                        next_frame[y][x] = CellStates.fire.value

            elif cell == CellStates.ash.value:
                if (CellStates.fire.value in neighbors
                    ) and random.random() <= reignite_chance:
                    next_frame[y][x] = CellStates.fire.value
                    did_touch_cell = True

            elif cell == CellStates.fire.value:
                did_touch_cell = True
                # add all neighbors to touched coordinates
                for c in neighbor_coords:
                    self.touched_coordinates.add(c)
                if random.random() <= sustain_chance:
                    next_frame[y][x] = CellStates.fire.value

                else:
                    next_frame[y][x] = CellStates.ash.value
            if did_touch_cell:
                # cache coordinates of all updated cells
                self.touched_coordinates.add((x, y))
        self.state = next_frame

        return next_frame


def generate_grid_coordinates(arr: np.array):
    for y in range(arr.shape[0]):
        for x in range(arr.shape[1]):
            yield x, y


def generate_forest(x, y, tree_density=0.8, **kwargs):
    available_states = [CellStates.tree, CellStates.pond]
    forest = np.zeros((y, x))
    for x, y in generate_grid_coordinates(forest):
        forest[y][x] = random.choices(
            list(available_states), [tree_density, 1 - tree_density])[0].value
    return forest


def set_fire(forest):
    new_forest = np.copy(forest)
    num_fires = random.randint(1, math.ceil(len(forest)**(1 / 2)))
    for _ in range(num_fires):
        y = random.randrange(len(forest))
        x = random.randrange(len(forest[y]))
        new_forest[y][x] = CellStates.fire.value
    return new_forest


def print_state(f):
    for row in f:
        for cell in row:
            print(CellStates(cell).name, end='')
        print()


def next_state(forest,
               spread_chance: float = 0.75,
               sustain_chance: float = 0.25,
               reignite_chance: float = 0.01,
               **kwargs):

    next_frame = np.copy(forest)
    for y in range(len(forest)):
        for x in range(len(forest[0])):
            cell = forest[y][x]
            neighbors = set()
            for offset in adjacent_offsets:
                if x + offset[0] < 0 or y + offset[1] < 0:
                    continue
                try:
                    neighbors.add(forest[y + offset[1]][x + offset[0]])
                except IndexError:
                    continue

            if cell == CellStates.tree.value:
                if CellStates.fire.value in neighbors:
                    if random.random() <= spread_chance:
                        next_frame[y][x] = CellStates.fire.value

            elif cell == CellStates.ash.value:
                if (CellStates.fire.value in neighbors
                    ) and random.random() <= reignite_chance:
                    next_frame[y][x] = CellStates.fire.value

            elif cell == CellStates.fire.value:
                if (CellStates.tree.value in neighbors
                    ) and random.random() <= sustain_chance:
                    next_frame[y][x] = CellStates.fire.value
                else:
                    next_frame[y][x] = CellStates.ash.value

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
