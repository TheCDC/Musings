import arcade
import forest
import time
import copy
import random
import argparse
from collections import Counter
from scipy.ndimage import convolve
import numpy as np
from typing import Tuple,List
SIMULATION_DIMENSIONS = (50, 50)
CELL_HEIGHT = 15
WHITE = np.array(arcade.color.WHITE)
state_to_color = {
    forest.CellStates.ash.value: np.array(arcade.color.LIGHT_GRAY),
    forest.CellStates.fire.value: np.array(arcade.color.RED_ORANGE),
    forest.CellStates.tree.value: np.array(arcade.color.FOREST_GREEN),
    forest.CellStates.pond.value: np.array((40, 122, 255)),
    0: arcade.color.YELLOW,
}

KERNEL_WATER_DEPTH = np.array([[0,1,1,1,0],
    [1,1,1,1,1],
    [1,1,0,1,1],
    [1,1,1,1,1],
    [0,1,1,1,0],])

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

class Game(arcade.Window):
    def __init__(self, window_height, cell_height):
        super().__init__(width=window_height * cell_height,
            height=window_height * cell_height,
            title=f'Forest Fire {window_height}x{window_height}',
            resizable=False,
            antialiasing=False,)
        self.set_update_rate(1 / 30)
        self.simulation_height = window_height
        self.cell_height = cell_height
        self.simulation_parameters = None
        self.simulation = None
        self.previous_state = None
        self.paused :bool = False

    def setup(self):
        self.paused :bool = True
        self.simulation_parameters = dict(tree_density=random.random(),
            chance_spread_fire_to_tree=random.random() / 2,
            chance_fire_sustain=random.random(),
            chance_spread_fire_to_ash=random.random() / 2)
        self.simulation : forest.SimulationState = forest.SimulationState(self.simulation_height, self.simulation_height)
        self.previous_state = self.simulation

        self.shapes_grid = list()
        self.sprites_list = arcade.SpriteList()
        num_water_neighbors = convolve((self.simulation.state == forest.CellStates.pond.value).astype(int), KERNEL_WATER_DEPTH,mode='constant')
        altitude_steps = 8
        altitude_components = [#((((forest.generate_noise_2d(self.simulation.state.shape,8) + 1) /
            #2) ** 4) * 2) - 1,
            forest.generate_noise_2d(self.simulation.state.shape,8),
            forest.generate_noise_2d(self.simulation.state.shape,32),
            forest.generate_noise_2d(self.simulation.state.shape,64)]
        self.altitude_map = (np.ceil(((sum(altitude_components) + 1) / 2) ** 2 * altitude_steps) / altitude_steps)
        amax = self.altitude_map.max()
        arcade.set_background_color(arcade.color.WHITE)

        start_time = int(round(time.time() * 1000))

        for y, row in enumerate(self.simulation.state):
            newrow = list()
            for x, cell in enumerate(row):
                color = np.array(state_to_color[cell])
                sum_pond_neighbors = num_water_neighbors[y][x]
                cell_altitude = self.altitude_map[y][x]
                if(cell == forest.CellStates.pond.value):
                    color = (color * 0.95 ** (sum_pond_neighbors)).astype(int)
                    pass
                elif cell == forest.CellStates.tree.value:
                    #make lighter based on altitude
                    color = (color + cell_altitude * (WHITE - color)).astype(int)
                    #make darker when near pond
                    color = (color * 0.90 ** (sum_pond_neighbors * (1 - cell_altitude))).astype(int)
                elif cell == forest.CellStates.ash.value:
                    color /= self.simulation.times_burned[y][x]
                color[color > 255] = 255
                


                shape = generate_cell_shape(x, y, tuple(color),
                                            self.cell_height)
                newrow.append(shape)
                self.sprites_list.append(shape)
            self.shapes_grid.append(newrow)
        end_time = int(round(time.time() * 1000))
        total_time = end_time - start_time
        # print('setup', total_time)

    def on_draw(self):

        start_time = int(round(time.time() * 1000))
        arcade.start_render()
        self.sprites_list.draw()
        status_str = '\n'.join([f'density={self.simulation_parameters["tree_density"]:.2f}',
            f'P(spread)={self.simulation_parameters["chance_spread_fire_to_tree"]:.2f}',
            f'P(sustain)={self.simulation_parameters["chance_fire_sustain"]:.2f}',
            f'P(reignite)={self.simulation_parameters["chance_spread_fire_to_ash"]:.2f}',])
        arcade.draw_text(status_str,
            10,
            20,
            arcade.color.BLACK,
            18,
            bold=False,)
        end_time = int(round(time.time() * 1000))
        total_time = end_time - start_time
        # print('draw', total_time)

    def update(self, delta_time):
        if self.paused:
            return
        self.previous_state = self.simulation.state
        self.simulation.step(**self.simulation_parameters)
        self.state = self.simulation.state
        counts = Counter()
        for y, row in enumerate(self.simulation.state):
            counts.update(row)
            for x, cell in enumerate(row):
                prev_val = self.previous_state[y][x]
                new_val = self.simulation.state[y][x]
                if new_val != prev_val:
                    # changing colors is expensive, so only do it when
                    # necessary
                    new_color = state_to_color[cell]
                    if(cell == forest.CellStates.ash.value):
                        c_darkness = np.array(arcade.color.ASH_GREY) * 0.90 ** (1 * (self.simulation.times_burned[y][x]))
                        c_lightness = np.array(arcade.color.ASH_GREY) * (self.altitude_map[y][x])
                        new_color = color_point_mean(np.array([c_lightness,c_darkness]),weights =np.array([0.4,0.6]))
                        
                    #constrain max color channel value to 255
                    new_color[new_color > 255] = 255
                    self.shapes_grid[y][x].color = new_color.astype(int)

                else:
                    # cell state unchanged
                    if new_val == forest.CellStates.fire.value:
                        self.shapes_grid[y][x].color = tuple(int(channel * 0.75) for channel in self.shapes_grid[y][x].color)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.paused = not self.paused
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.setup()


parser = argparse.ArgumentParser()
parser.add_argument('--height',
    type=int,
    help="Simulation height (cells)",
    default=80,)
parser.add_argument('--cell_height',
    type=int,
    help='Cell height (pixels)',
    default=10,)


def main():
    args = parser.parse_args()
    CELL_HEIGHT = args.cell_height
    SIMULATION_DIMENSIONS = (args.height, args.height)

    g = Game(args.height, args.cell_height)
    g.setup()
    arcade.run()


if __name__ == '__main__':
    main()
