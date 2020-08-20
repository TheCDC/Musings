# https://www.reddit.com/r/learnpython/comments/b6iu6z/forest_fire_simulation_program_help/
import random
import enum
import copy
import math
import numpy as np
from opensimplex import OpenSimplex
from typing import Generator, Tuple
class CellStates(enum.Enum):
    pond = 0
    tree = 1
    ash = 3
    fire = 4


adjacent_offsets = [(-1, 1), (0, 1), (1, 1), (-1, 0), (0, 0), (1, 0), (-1, -1),
                    (0, -1), (1, -1)]

def generate_noise_2d(shape,feature_size=4) -> np.array:
    width = shape[1]
    height = shape[0]
    simplex = OpenSimplex(seed=random.randrange(0,2048))
    arr = np.ones((width,height))
    for y in range(height):
        for x in range(width):
            arr[y,x] = simplex.noise2d(x / feature_size,y / feature_size)
    return arr

class SimulationState:
    def __init__(self, x: int=10, y: int=10, tree_density=0.5,):
        self.state = set_fire(generate_forest(x, y, tree_density))
        self.touched_coordinates = set(generate_grid_coordinates(self.state))

    def step(self,
             chance_spread_fire_to_tree: float=0.75,
             chance_fire_sustain: float=0.25,
             chance_spread_fire_to_ash: float=0.01,):
        next_frame = np.copy(self.state)
        last_touched_coordinates = self.touched_coordinates
        self.touched_coordinates = set()
        # print((last_touched_coordinates))
        # Loop over each cell and check its neighbors to generate the next
        # state
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
                    if random.random() <= chance_spread_fire_to_tree:
                        next_frame[y][x] = CellStates.fire.value

            elif cell == CellStates.ash.value:
                if (CellStates.fire.value in neighbors) and random.random() <= chance_spread_fire_to_ash:
                    next_frame[y][x] = CellStates.fire.value
                    did_touch_cell = True

            elif cell == CellStates.fire.value:
                did_touch_cell = True
                # add all neighbors to touched coordinates
                for c in neighbor_coords:
                    self.touched_coordinates.add(c)
                if random.random() <= chance_fire_sustain:
                    next_frame[y][x] = CellStates.fire.value

                else:
                    next_frame[y][x] = CellStates.ash.value
            if did_touch_cell:
                # cache coordinates of all updated cells
                self.touched_coordinates.add((x, y))
        self.state = next_frame

        return next_frame


def generate_grid_coordinates(arr: np.array) -> Generator[Tuple[int],None,None]:
    for y in range(arr.shape[0]):
        for x in range(arr.shape[1]):
            yield x, y


def generate_forest(x, y, tree_density=0.8, **kwargs) -> np.array:
    available_states = [CellStates.tree, CellStates.pond]
    forest = np.zeros((y, x))
    noise_layers = [generate_noise_2d(forest.shape,4),
        generate_noise_2d(forest.shape,8),
        generate_noise_2d(forest.shape,64),]
    noise_grid = sum([((l + 1) / 2) ** 2 for l in noise_layers])
    for x, y in generate_grid_coordinates(forest):
        noise_is_high = (noise_grid[y][x]) > (tree_density)
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
            print(CellStates(cell).name, end = '')
        print()



def main():
    sim :SimulationState = SimulationState(10,10)
    
    for i in range(10):
        sim.step()
        print_state(sim.state)
        print('===========')


if __name__ == '__main__':
    main()
