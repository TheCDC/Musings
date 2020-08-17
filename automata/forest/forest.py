# https://www.reddit.com/r/learnpython/comments/b6iu6z/forest_fire_simulation_program_help/
import random
import enum
import copy
import math
import numpy as np


class CellStates ( enum.Enum ):
    pond = 0
    tree = 1
    ash = 3
    fire = 4


adjacent_offsets = [(-1, 1), (0, 1), (1, 1), (-1, 0), (0, 0), (1, 0), (-1, -1),
                    (0, -1), (1, -1)]



def generate_perlin_noise_2d(shape, res,frequency):
    """https://pvigier.github.io/2018/06/13/perlin-noise-numpy.html"""
    def f(t):
        t = t*frequency
        return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3
    
    delta = (res[0] / shape[0], res[1] / shape[1])
    d = (shape[0] // res[0], shape[1] // res[1])
    grid = np.mgrid[0:res[0]:delta[0],0:res[1]:delta[1]].transpose(1, 2, 0) % 1
    # Gradients
    angles = 2 * np.pi * np.random.rand(res[0] + 1, res[1] + 1)
    gradients = np.dstack((np.cos(angles), np.sin(angles)))
    g00 = gradients[0:-1,0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g10 = gradients[1:,0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g01 = gradients[0:-1,1:].repeat(d[0], 0).repeat(d[1], 1)
    g11 = gradients[1:,1:].repeat(d[0], 0).repeat(d[1], 1)
    # Ramps
    n00 = np.sum(grid * g00, 2)
    n10 = np.sum(np.dstack((grid[:,:,0] - 1, grid[:,:,1])) * g10, 2)
    n01 = np.sum(np.dstack((grid[:,:,0], grid[:,:,1] - 1)) * g01, 2)
    n11 = np.sum(np.dstack((grid[:,:,0] - 1, grid[:,:,1] - 1)) * g11, 2)
    # Interpolation
    t = f(grid)
    n0 = n00 * (1 - t[:,:,0]) + t[:,:,0] * n10
    n1 = n01 * (1 - t[:,:,0]) + t[:,:,0] * n11
    return np.sqrt(2) * ((1 - t[:,:,1]) * n0 + t[:,:,1] * n1)


class SimulationState:
    def __init__(self, x: int=10, y: int=10, tree_density=0.5, **kwargs):
        self.state = set_fire(generate_forest(x, y, tree_density))
        self.touched_coordinates = set(generate_grid_coordinates(self.state))

    def step(self,
             spread_chance: float=0.75,
             sustain_chance: float=0.25,
             reignite_chance: float=0.01,
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
                if (CellStates.fire.value in neighbors) and random.random() <= reignite_chance:
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
    noise_grid = generate_perlin_noise_2d((x,y),(15,15),1)
    for x, y in generate_grid_coordinates(forest):
        noise_is_high = (noise_grid[y][x] / 2 + 0.5) < (tree_density)
        if noise_is_high:
            forest[y][x] = CellStates.tree.value
        else:
            forest[y][x] = CellStates.pond.value
    return forest


def set_fire(forest):
    new_forest = np.copy(forest)
    num_fires = random.randint(1, math.ceil(len(forest) ** (1 / 2)))
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
               spread_chance: float=0.75,
               sustain_chance: float=0.25,
               reignite_chance: float=0.01,
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
                if (CellStates.fire.value in neighbors) and random.random() <= reignite_chance:
                    next_frame[y][x] = CellStates.fire.value

            elif cell == CellStates.fire.value:
                if (CellStates.tree.value in neighbors) and random.random() <= sustain_chance:
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
