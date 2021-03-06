# https://www.reddit.com/r/learnpython/comments/b6iu6z/forest_fire_simulation_program_help/
import random
import enum
import math
import numpy as np
import cv2
from cv2_utils import numpy_to_cv2
from opensimplex import OpenSimplex
from typing import Generator, Tuple
from scipy.ndimage import convolve
import colors
from noise import pnoise2, snoise2
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

def ones_to_color(arr:np.array, color:Tuple[int,int,int]):
    rs = np.repeat(arr[:,:,np.newaxis],3,axis=2) #repeat the value on the second axis into the third dimension three times
    #rs = arr.reshape((arr.shape[0],arr.shape[1],3))
    mask = arr == 1
    rs[mask] = color
    return rs

def repeated_trials(p_trial,n_trials):
    return 1 - (1 - p_trial) ** n_trials

def generate_noise_2d(shape,feature_size=4,octaves=1) -> np.array:
    freq = 16.0 * octaves
    offsets = (random.randrange(4096),random.randrange(4096))
    width = shape[1]
    height = shape[0]
    simplex = OpenSimplex(seed=random.randrange(0,2048 ** 2))
    arr = np.ones((width,height))
    for y in range(height):
        for x in range(width):
            #arr[y,x] = simplex.noise2d((x + offsets[0]) / feature_size,(y +
            #offsets[1]) / feature_size)
            arr[y,x] = pnoise2((x + offsets[0]) / feature_size,(y + offsets[1]) / feature_size,octaves)
    return arr

def quantize_layer(arr:np.array,steps:int):
    return  (np.ceil(np.abs(arr) * steps) / steps)

class SimulationState:
    def __init__(self, x: int=10, y: int=10, tree_density=0.5,):
        self.state :np.array = generate_forest(x, y, tree_density)
                                        
        self._age = 0
        self.times_burned = np.zeros(self.state.shape)
        altitude_steps = 12
        altitude_components = [#((((forest.generate_noise_2d(self.simulation.state.shape,8) + 1) /
        #2) ** 4) * 2) - 1,
        #generate_noise_2d(self.state.shape,8) / 2 + 1 / 2,
        ((generate_noise_2d(self.state.shape,16) + 1) / 8),
        (generate_noise_2d(self.state.shape,128) / 2 + 1 / 2) ,]
        #self.altitude_map = (np.ceil(sum(altitude_components) *
        #altitude_steps) / altitude_steps)
        self.altitude_map = quantize_layer(sum(altitude_components),altitude_steps)
        self.temperature_map = generate_noise_2d(self.state.shape,128)

    def set_fire(self):
        self.state :np.array = set_fire(self.state)

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


def generate_forest(x, y, tree_density=0.5, **kwargs) -> np.array:
    forest = np.full((y, x),CellStates.tree.value)
  
    # ===== Land Bridges =====
    land_bridge_thresh = 0.3
    land_bridge_layer = np.abs(generate_noise_2d(forest.shape,128)) + generate_noise_2d(forest.shape,16) ** 2 / 8 - generate_noise_2d(forest.shape,16) ** 2

    land_bridge_layer[land_bridge_layer > land_bridge_thresh] = 1
    # ===== Rivers =====
    river_obstacles_layer = generate_noise_2d(forest.shape,64)

    rivers_thresh = 0.05

    rivers_layer = generate_noise_2d(forest.shape,32) + generate_noise_2d(forest.shape,32)
    rivers_layer_mask = np.logical_and(rivers_layer < rivers_thresh, rivers_layer > - rivers_thresh)
    rivers_tiny_layer = generate_noise_2d(forest.shape,16,octaves=1) + generate_noise_2d(forest.shape,16,octaves=1)
    rivers_tiny_layer_mask = np.logical_and(rivers_tiny_layer < rivers_thresh , rivers_tiny_layer > - rivers_thresh)
    # Apply normal size rivers
    rivers_layer[np.logical_and(rivers_layer_mask, #slice the noise to select blobby circularish regions
                                river_obstacles_layer < 0)] = 1
    # Apply tiny rivers
    rivers_tiny_layer[np.logical_and(rivers_tiny_layer_mask, #slice the noise to select blobby circularish regions
        generate_noise_2d(forest.shape,32) < 0)] = 1
    # ===== Oceans =====
    oceans_thresh = 0.2
    oceans_layer = np.abs(generate_noise_2d(forest.shape,256)) + (generate_noise_2d(forest.shape,8) ** 2) / 8
    oceans_layer[oceans_layer > oceans_thresh] = 1

    # ===== Apply Layers =====
    layers_and_colors = [(oceans_layer,colors.LIGHTBLUE),
        (land_bridge_layer,colors.GREEN),
        (rivers_layer,colors.LIGHTBLUE),
        (rivers_tiny_layer,colors.LIGHTBLUE)]
    #colored_layers = [ones_to_color(*args) for args in layers_and_colors]
    colored_layers = [oceans_layer,
        land_bridge_layer,
        rivers_layer,
        rivers_tiny_layer]
    cv2.imshow("layers", 
        cv2.cvtColor(np.concatenate(colored_layers,axis=1).astype('float32'), cv2.COLOR_RGB2BGR))
    forest[oceans_layer == 1] = CellStates.pond.value
    forest[land_bridge_layer == 1] = CellStates.tree.value
    forest[rivers_layer == 1] = CellStates.pond.value
    forest[rivers_tiny_layer == 1] = CellStates.pond.value
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
