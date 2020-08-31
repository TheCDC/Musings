from cv2_utils import numpy_to_cv2
import time
import arcade
import forest
import random
import argparse
import cv2
from scipy.ndimage import convolve,zoom
import numpy as np
from time import sleep

#img = np.zeros([500,500,3])

#img[:,:,0] = np.ones([500,500]) * 64 / 255.0
#img[:,:,1] = np.ones([500,500]) * 128 / 255.0
#img[:,:,2] = np.ones([500,500]) * 192 / 255.0

#while True:
#    img = np.random.random_sample(img.shape)
#    cv2.imshow("image", img)
#    cv2.waitKey(20)
SIMULATION_DIMENSIONS = (50, 50)
CELL_HEIGHT = 15
WHITE = np.array(arcade.color.WHITE)
DRY_BROWN = np.array((176, 103, 0))
state_to_color = {
    forest.CellStates.ash.value: np.array(arcade.color.LIGHT_GRAY),
    forest.CellStates.fire.value: np.array(arcade.color.RED_ORANGE),
    forest.CellStates.tree.value: np.array(arcade.color.GREEN),
    forest.CellStates.pond.value: np.array((40, 122, 255)),
    0: arcade.color.YELLOW,
}

KERNEL_WATER_DEPTH = np.ones((7,7))

def generate_cell_shape(x, y, color, cell_height=CELL_HEIGHT):
    xx = x * cell_height + cell_height / 2
    yy = y * cell_height + cell_height / 2
    sprite = arcade.Sprite(filename='pixel.png',
        center_x=xx,
        center_y=yy,
        scale=cell_height,)
    sprite.color = color
    return sprite

def color_point_mean(colors:np.array,weights:np.array=None):
    if weights is None:
        weights = np.ones(colors.shape)
    else:
        weights = weights.reshape((weights.shape[0],1))

    return sum(colors * weights) / len(colors)


class Game():
    def __init__(self, window_height, cell_height):
        self.window_name = f"Forest Fire {window_height}x{window_height}"
        self.simulation_height = window_height
        self.cell_height = cell_height
        self.simulation_parameters = None
        self.simulation = None
        self.previous_state = None
        self.paused :bool = True
        self.color_buffer = np.zeros((self.simulation_height,self.simulation_height,3))
        self.is_lit = False
    def setup(self):
        self.paused :bool = True
        self.is_lit = False
        self.simulation_parameters = dict(tree_density=random.random() * 0.7,
            chance_spread_fire_to_tree=random.random() / 2 + 0.1,
            chance_fire_sustain=random.random(),
            chance_spread_fire_to_ash=random.random() * 0.9)
        self.simulation : forest.SimulationState = forest.SimulationState(self.simulation_height, self.simulation_height)
        self.previous_state : forest.SimulationState = self.simulation
        start_time :int = int(round(time.time() * 1000))
        self.state :np.array = self.simulation.state


        #for y, row in enumerate(self.simulation.state):
        #    for x, cell in enumerate(row):
        #        color = np.array(state_to_color[cell])
        #        sum_pond_neighbors = num_water_neighbors[y][x]
        #        cell_altitude = self.altitude_map[y][x]
        #        if(cell == forest.CellStates.pond.value):
        #            color = (color * 0.95 ** (sum_pond_neighbors)).astype(int)
        #            pass
        #        elif cell == forest.CellStates.tree.value:
        #            #make lighter based on altitude
        #            color = (color + cell_altitude * (WHITE -
        #            color)).astype(int)
        #            #make darker when near pond
        #            color = (color * 0.90 ** (sum_pond_neighbors * (1 -
        #            cell_altitude))).astype(int)
        #        elif cell == forest.CellStates.ash.value:
        #            color /= self.simulation.times_burned[y][x]
        #        color[color > 255] = 255

        end_time = int(round(time.time() * 1000))
        total_time = end_time - start_time
        # print('setup', total_time)

    def on_draw(self):

        start_time = int(round(time.time() * 1000))
        status_str = '\n'.join([f'density={self.simulation_parameters["tree_density"]:.2f}',
            f'P(spread)={self.simulation_parameters["chance_spread_fire_to_tree"]:.2f}',
            f'P(sustain)={self.simulation_parameters["chance_fire_sustain"]:.2f}',
            f'P(reignite)={self.simulation_parameters["chance_spread_fire_to_ash"]:.2f}',])

        color_map_scalar_shape = self.state.shape + (1,)

        self.color_buffer = np.zeros((self.state.shape) + (3,))

        trees = self.state == forest.CellStates.tree.value
        fire = self.state == forest.CellStates.fire.value
        ash = self.state == forest.CellStates.ash.value
        pond = self.state == forest.CellStates.pond.value

        num_tree_neighbors = convolve(trees.astype(int),KERNEL_WATER_DEPTH,mode="constant")
        num_pond_neighbors = convolve(pond.astype(int),KERNEL_WATER_DEPTH,mode="constant")

        altitude_color_map = (self.simulation.altitude_map.reshape(color_map_scalar_shape))
        snow_color_layer = altitude_color_map * np.full(self.color_buffer.shape,WHITE) 
        dry_tree_color_layer = self.simulation.temperature_map.reshape(color_map_scalar_shape) * np.full(self.color_buffer.shape,DRY_BROWN)
        tree_color_layer = np.full(self.color_buffer.shape,state_to_color[forest.CellStates.tree.value])
        water_color_layer = np.full(self.color_buffer.shape,state_to_color[forest.CellStates.pond.value])
        ash_color_layer = np.full(self.color_buffer.shape,state_to_color[forest.CellStates.ash.value])

        self.color_buffer[trees] = ((snow_color_layer * 0.4 + tree_color_layer * 0.2 + dry_tree_color_layer * 0.4))[trees]
        self.color_buffer[pond] = (water_color_layer * (0.98 ** num_pond_neighbors.reshape(color_map_scalar_shape)))[pond]
        self.color_buffer[fire] = state_to_color[forest.CellStates.fire.value]
        self.color_buffer[ash] = (ash_color_layer * (0.90 ** self.simulation.times_burned.reshape(color_map_scalar_shape)))[ash]



        img = zoom(self.color_buffer,(self.cell_height,self.cell_height,1),order=0) / 255
        img = cv2.cvtColor(img.astype('float32'), cv2.COLOR_RGB2BGR)
        s = img.shape

        #=========== Set up mouse click event handler ==========
        cv2.setMouseCallback(self.window_name, self.mouse_click) 
        cv2.imshow(self.window_name, img)
        cv2.waitKey(1)

        cv2.imshow("times_burned",(self.simulation.times_burned >= 1).astype('float32'))
        end_time = int(round(time.time() * 1000))
        total_time = end_time - start_time
        print('draw', total_time)

    def update(self, delta_time,force=False):
        if self.paused and not force:
            return
        if not self.is_lit:
            self.simulation.set_fire()
            self.is_lit = True
        self.previous_state = self.simulation.state
        self.simulation.step(**self.simulation_parameters)
        self.state = self.simulation.state

    def mouse_click(self, event, x, y,  
                flags, param): 
        # to check if left mouse
        # button was clicked
        if event == cv2.EVENT_LBUTTONDOWN: 
            self.paused = not self.paused
            pass
        elif event == cv2.EVENT_RBUTTONDOWN: 
            self.setup()
parser = argparse.ArgumentParser()
parser.add_argument('--height',
    type=int,
    help="Simulation height (cells)",
    default=200,)
parser.add_argument('--cell_height',
    type=int,
    help='Cell height (pixels)',
    default=2,)


def main():
    args = parser.parse_args()
    CELL_HEIGHT = args.cell_height
    SIMULATION_DIMENSIONS = (args.height, args.height)

    g = Game(args.height, args.cell_height)
    g.setup()
    while True:
        g.update(0)
        g.on_draw()



if __name__ == '__main__':
    main()