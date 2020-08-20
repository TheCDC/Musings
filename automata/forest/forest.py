# https://www.reddit.com/r/learnpython/comments/b6iu6z/forest_fire_simulation_program_help/
import random
import enum
import copy
import math
import numpy as np

from opensimplex import OpenSimplex
from typing import Generator, Tuple, Set
from scipy.ndimage import convolve

KERNEL_IMMEDIATE_NEIGHBORS = np.array([[1,1,1],
                                       [1,0,1],
                                       [1,1,1]])

class CellStates(enum.Enum):
    pond = 1
    tree = 2
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
        self.state :np.array = set_fire(generate_forest(x, y, tree_density))
    @property
    def state(self):
        return self._state
    @state.setter
    def state(self,value):
        self._state = value
    def step(self,
             chance_spread_fire_to_tree: float=0.75,
             chance_fire_sustain: float=0.25,
             chance_spread_fire_to_ash: float=0.01,
             **kwargs):
        next_frame_buffer = np.copy(self.state)
        # print((last_touched_coordinates))
        # Loop over each cell and check its neighbors to generate the next
        # start by decomposing the state into layers
        trees = self.state == CellStates.tree.value
        fire = self.state == CellStates.fire.value
        ash = self.state == CellStates.ash.value
        pond = self.state == CellStates.pond.value

        has_fire_neighbors = convolve(fire,KERNEL_IMMEDIATE_NEIGHBORS,mode="constant")
        tree_becomes_fire = has_fire_neighbors * (np.random.random_sample(self.state.shape) <= chance_spread_fire_to_tree) * trees
        ash_becomes_fire = has_fire_neighbors * (np.random.random_sample(self.state.shape) <= chance_spread_fire_to_ash) * ash

        fire_becomes_ash = np.logical_and(fire, tree_becomes_fire == 0) #was fire and is not about to become fire
        final = (trees ^ tree_becomes_fire) + tree_becomes_fire * CellStates.fire.value
        
        fire_becomes_fire = fire * (np.random.random_sample(self.state.shape) <= chance_fire_sustain)
        overwrite_with_nonzero(next_frame_buffer, tree_becomes_fire * CellStates.fire.value)
        overwrite_with_nonzero(next_frame_buffer, fire_becomes_ash * CellStates.ash.value)
        overwrite_with_nonzero(next_frame_buffer, fire_becomes_fire * CellStates.fire.value)
        overwrite_with_nonzero(next_frame_buffer, ash_becomes_fire * CellStates.fire.value)
        self.state = next_frame_buffer
        return self.state

def overwrite_with_nonzero(bottom:np.array,top:np.array) -> None:
    to_change = top > 0
    bottom[to_change] = 0
    bottom += top
    return bottom

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
    noise_grid = sum([((l + 1) / 2) ** 2 for l in noise_layers]) - (generate_noise_2d(forest.shape,32))
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
