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

class CellStates ( enum.Enum ):
    pond = 1
    tree = 2
    ash = 3
    fire = 4


adjacent_offsets = [(-1, 1), (0, 1), (1, 1), (-1, 0), (0, 0), (1, 0), (-1, -1),
                    (0, -1), (1, -1)]
def repeated_trials(p_trial,n_trials):
    return 1 - (1 - p_trial) ** n_trials
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
        self._age = 0
        self.times_burned = np.ones(self.state.shape)
        altitude_steps = 12
        altitude_components = [#((((forest.generate_noise_2d(self.simulation.state.shape,8) + 1) /
        #2) ** 4) * 2) - 1,
        #generate_noise_2d(self.state.shape,8) / 2 + 1 / 2,
((generate_noise_2d(self.state.shape,16) + 1) / 8),
        (generate_noise_2d(self.state.shape,128) / 2 + 1 / 2) ,]
        self.altitude_map = (np.ceil(sum(altitude_components) * altitude_steps) / altitude_steps)
        pass
    @property
    def age(self):
        return self._age
    @age.setter
    def age(self, value):
        self._age = value
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

        num_fire_neighbors = convolve(fire,KERNEL_IMMEDIATE_NEIGHBORS,mode="constant") 
        tree_becomes_fire = (np.random.random_sample(self.state.shape) <= repeated_trials(chance_spread_fire_to_tree, num_fire_neighbors)) * trees
        ash_becomes_fire = num_fire_neighbors * (np.random.random_sample(self.state.shape) <= (chance_spread_fire_to_ash / self.times_burned)) * ash

        fire_becomes_ash = np.logical_and(fire, tree_becomes_fire == 0) #was fire and is not about to become fire
        final = (trees ^ tree_becomes_fire) + tree_becomes_fire * CellStates.fire.value
        
        fire_becomes_fire = num_fire_neighbors * fire * (np.random.random_sample(self.state.shape) <= chance_fire_sustain / self.times_burned)
        overwrite_with_nonzero(next_frame_buffer, tree_becomes_fire * CellStates.fire.value)
        overwrite_with_nonzero(next_frame_buffer, fire_becomes_ash * CellStates.ash.value)
        overwrite_with_nonzero(next_frame_buffer, fire_becomes_fire * CellStates.fire.value)
        overwrite_with_nonzero(next_frame_buffer, ash_becomes_fire * CellStates.fire.value)

        self.times_burned += next_frame_buffer == CellStates.fire.value
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
    forest = np.zeros((y, x))
    noise_layers = [generate_noise_2d(forest.shape,4),
        generate_noise_2d(forest.shape,8),
        generate_noise_2d(forest.shape,64),]
    # ===== Normal Trees Layer =====
    trees_base_layer = sum([((l + 1) / 2) ** 2  for l in noise_layers]) - (generate_noise_2d(forest.shape,32))
    # ===== Land Bridges =====
    land_bridge_thresh = 0.05
    land_bridge_layer = generate_noise_2d(forest.shape,256)
    land_bridge_layer = np.sign(land_bridge_layer) * np.abs(land_bridge_layer) 
    land_bridge_layer[np.logical_and(land_bridge_layer < land_bridge_thresh, land_bridge_layer > - land_bridge_thresh)] = 1
    # =====Rivers =====
    rivers_thresh = 0.1
    rivers_layer = generate_noise_2d(forest.shape,32)
    rivers_layer = np.sign(rivers_layer) * np.abs(rivers_layer) 
    rivers_layer[np.logical_and(rivers_layer < rivers_thresh, rivers_layer > - rivers_thresh)] = 1


    forest[trees_base_layer >= tree_density] = CellStates.tree.value
    forest[trees_base_layer < tree_density] = CellStates.pond.value
    forest[land_bridge_layer == 1] = CellStates.tree.value
    forest[land_bridge_layer == 1] = CellStates.pond.value
    return forest

def set_fire(forest):
    new_forest = np.copy(forest)
    num_fires = random.randint(1, math.ceil(len(forest) ** (1 / 2)))
    trees = np.where(new_forest == CellStates.tree.value)
    possible_coordinates = list(zip(*trees)) #convert coordinates from ((x0,x1,...),(y0,y2,...)) to ((x0,y0),(x1,y1))
    random.shuffle(possible_coordinates)
    to_set_fire = possible_coordinates[:num_fires]
    r = tuple(zip(*to_set_fire)) #wrangle coordinates back from ((x0,y0),(x1,y1)) to ((x0,x1,...),(y0,y2,...))
    if len(r) > 0:
        new_forest[r] = CellStates.fire.value
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
